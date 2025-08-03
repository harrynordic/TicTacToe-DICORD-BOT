import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Linguagem do Bot em pt-BR

# Configuração do Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

prefix = "#"

token = os.getenv("DISCORD_TOKEN")

if token is None:
    print("ERRO: O token do Discord não foi encontrado nas variáveis de ambiente ou no arquivo .env.")
    print("Certifique-se de ter um arquivo .env na mesma pasta com a linha: DISCORD_TOKEN=YOUR_TOKEN_HERE")
    print('EXEMPLO: DISCORD_TOKEN=MTEwODgxNzQ2NTgyNTMw')
    exit() # Encerra o programa se o token não for encontrado

bot = commands.Bot(command_prefix=prefix, intents=intents)

# Variáveis Globais para Gerenciar Múltiplas Partidas
active_games = {}

# Classe do Jogo da Velha
class TicTacToeGame:
    def __init__(self, channel):
        self.channel = channel
        self.board = self.create_board()
        self.players = {}
        self.player_names = {}
        self.current_player_id = None
        self.game_active = False
        self.moves_made = 0

    def create_board(self):
        return [[' ' for _ in range(3)] for _ in range(3)]

    def print_board(self):
        line = '-------------'
        numbered_board = []
        k = 0
        for r in range(3):
            row_display = []
            for c in range(3):
                k += 1
                if self.board[r][c] == ' ':
                    row_display.append(str(k))
                else:
                    row_display.append(self.board[r][c])
            numbered_board.append(row_display)

        output = line + '\n'
        for row in numbered_board:
            output += '|'
            for cell in row:
                output += f' {cell} |' if len(cell) == 1 else f'{cell} |'
            output += '\n' + line + '\n'
        return output

    def check_win(self, player_mark):
        for row in self.board:
            if all(cell == player_mark for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player_mark for row in range(3)):
                return True
        if (self.board[0][0] == player_mark and self.board[1][1] == player_mark and self.board[2][2] == player_mark) or \
           (self.board[0][2] == player_mark and self.board[1][1] == player_mark and self.board[2][0] == player_mark):
            return True
        return False

    def check_tie(self):
        return self.moves_made == 9 and not self.check_win('X') and not self.check_win('O')

    def add_player(self, player_member):
        if len(self.players) < 2:
            if player_member.id not in self.players:
                mark = 'X' if not self.players else 'O'
                self.players[player_member.id] = mark
                self.player_names[player_member.id] = player_member.mention
                return True, mark
            return False, "already_joined"
        return False, "full"
    
    def get_player_mark(self, user_id):
        return self.players.get(user_id)

    def get_other_player_id(self, current_player_id):
        for player_id in self.players:
            if player_id != current_player_id:
                return player_id
        return None

    def make_move(self, user_id, position):
        if not self.game_active:
            return False, "game_not_active"
        if user_id != self.current_player_id:
            return False, "not_your_turn"

        if not (1 <= position <= 9):
            return False, "invalid_position"

        row = (position - 1) // 3
        col = (position - 1) % 3

        if self.board[row][col] != ' ':
            return False, "position_occupied"

        player_mark = self.players[user_id]
        self.board[row][col] = player_mark
        self.moves_made += 1
        return True, "success"

    def switch_turn(self):
        other_player_id = self.get_other_player_id(self.current_player_id)
        if other_player_id:
            self.current_player_id = other_player_id
            return True
        return False

    def reset_game(self):
        self.board = self.create_board()
        self.players = {}
        self.player_names = {}
        self.current_player_id = None
        self.game_active = False
        self.moves_made = 0


# Eventos do Bot
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name} (ID: {bot.user.id})')
    print('------')
    print(f'Use o prefixo "{prefix}" para os comandos.')
    print('------')


# Comandos do Bot
@bot.command(name='start', help='Inicia uma nova partida de Jogo da Velha.')
async def start_game(ctx):
    channel_id = ctx.channel.id

    if channel_id not in active_games:
        active_games[channel_id] = TicTacToeGame(ctx.channel)
        await ctx.send(f'Jogo da Velha iniciado neste canal! Digite `{prefix}start` para entrar na partida.')

    game = active_games[channel_id]

    if not game.game_active:
        added, status = game.add_player(ctx.author)

        if added:
            await ctx.send(f'{ctx.author.mention} entrou na partida como **{status}**!')
            if len(game.players) == 2:
                game.game_active = True
                for p_id, mark in game.players.items():
                    if mark == 'X':
                        game.current_player_id = p_id
                        break
                
                player_x_mention = game.player_names[game.current_player_id]
                
                await ctx.send(f'Dois jogadores encontrados! A partida vai começar.\n'
                               f'```\n{game.print_board()}\n```\n'
                               f'É a vez de {player_x_mention} (X)! Use `{prefix}play <número>` para fazer sua jogada.')
            else:
                await ctx.send('Aguardando o segundo jogador. Digite `#start` para entrar.')
        elif status == "already_joined":
            await ctx.send(f'{ctx.author.mention}, você já está participando desta partida.')
        elif status == "full":
            await ctx.send(f'A partida neste canal já tem dois jogadores. Por favor, espere a partida terminar ou inicie uma nova em outro canal.')
    else:
        await ctx.send(f'Já existe uma partida em andamento neste canal. Use `{prefix}stop` para encerrá-la ou `{prefix}play` para jogar.')


@bot.command(name='play', help='Faz uma jogada no Jogo da Velha. Ex: #play 5')
async def play_move(ctx, position: int):
    channel_id = ctx.channel.id

    if channel_id not in active_games or not active_games[channel_id].game_active:
        await ctx.send(f'{ctx.author.mention}, não há uma partida ativa neste canal. Use `{prefix}start` para começar uma.')
        return

    game = active_games[channel_id]

    if ctx.author.id not in game.players:
        await ctx.send(f'{ctx.author.mention}, você não está participando desta partida. Use `{prefix}start` para entrar.')
        return
    
    if ctx.author.id != game.current_player_id:
        current_player_mention = game.player_names.get(game.current_player_id, "o outro jogador")
        await ctx.send(f'{ctx.author.mention}, não é a sua vez! É a vez de {current_player_mention}.')
        return

    success, status_message = game.make_move(ctx.author.id, position)

    if success:
        player_mark = game.get_player_mark(ctx.author.id)
        await ctx.send(f'```\n{game.print_board()}\n```')

        if game.check_win(player_mark):
            await ctx.send(f'🎉 Parabéns, {ctx.author.mention}! Você venceu a partida!')
            del active_games[channel_id]
            await ctx.send(f'A partida foi encerrada. Use `{prefix}start` para uma nova partida.')
        elif game.check_tie():
            await ctx.send('🤝 Empate! O tabuleiro está cheio e ninguém venceu.')
            del active_games[channel_id]
            await ctx.send(f'A partida foi encerrada. Use `{prefix}start` para uma nova partida.')
        else:
            game.switch_turn()
            next_player_mention = game.player_names.get(game.current_player_id, "Erro no jogador")
            await ctx.send(f'É a vez de {next_player_mention} ({game.get_player_mark(game.current_player_id)})!')
    else:
        if status_message == "invalid_position":
            await ctx.send(f'{ctx.author.mention}, posição inválida. Use um número de 1 a 9.')
        elif status_message == "position_occupied":
            await ctx.send(f'{ctx.author.mention}, essa posição já está ocupada. Escolha outra.')
        elif status_message == "game_not_active":
             await ctx.send(f'{ctx.author.mention}, a partida ainda não começou ou não está ativa. Use `{prefix}start` para iniciar.')
        elif status_message == "not_your_turn":
            current_player_mention = game.player_names.get(game.current_player_id, "o outro jogador")
            await ctx.send(f'{ctx.author.mention}, não é a sua vez! É a vez de {current_player_mention}.')


@bot.command(name='stop', help='Encerra a partida de Jogo da Velha atual.')
async def stop_game(ctx):
    channel_id = ctx.channel.id

    if channel_id in active_games:
        del active_games[channel_id]
        await ctx.send(f'A partida de Jogo da Velha neste canal foi encerrada. Use `{prefix}start` para começar uma nova.')
    else:
        await ctx.send(f'Não há nenhuma partida de Jogo da Velha ativa neste canal para parar.')

@bot.command(name='show', help='Mostra o tabuleiro atual do Jogo da Velha.')
async def show_board(ctx):
    channel_id = ctx.channel.id
    if channel_id in active_games and active_games[channel_id].game_active:
        game = active_games[channel_id]
        await ctx.send(f'Tabuleiro atual:\n```\n{game.print_board()}\n```')
        current_player_mention = game.player_names.get(game.current_player_id, "Erro no jogador")
        await ctx.send(f'É a vez de {current_player_mention} ({game.get_player_mark(game.current_player_id)})!')
    else:
        await ctx.send(f'Não há uma partida ativa neste canal. Use `{prefix}start` para começar uma.')

# Execução do Bot
bot.run(token)