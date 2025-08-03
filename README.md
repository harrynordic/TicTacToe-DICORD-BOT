🤖 Bot de Jogo da Velha para Discord
Um bot simples para Discord que permite que dois jogadores joguem Jogo da Velha (Tic-Tac-Toe) diretamente em um canal do Discord.

✨ Funcionalidades
#start: Inicia uma nova partida de Jogo da Velha no canal. Dois jogadores precisam digitar este comando para entrar na partida.

#play <posição>: Faz uma jogada no tabuleiro. Substitua <posição> por um número de 1 a 9 para escolher a casa desejada.

#show: Exibe o tabuleiro atual e informa de quem é a vez.

#stop: Encerra a partida atual.

🚀 Como Rodar o Bot
Siga estas instruções para configurar e executar o bot em seu próprio servidor Discord.

Pré-requisitos
Python 3.8+ instalado.

Acesso ao Discord Developer Portal para criar e configurar seu bot.

📦 Instalação das Dependências
Clone este repositório para o seu computador:

git clone https://github.com/harrynordic/TicTacToe-DICORD-BOT.git
cd TicTacToe-DICORD-BOT

Instale as bibliotecas necessárias:

pip install discord.py python-dotenv

⚙️ Configuração do Token do Bot (Crucial!)
Para que o bot se conecte ao Discord, ele precisa de um token de autenticação. Este token é secreto e nunca deve ser compartilhado publicamente em seu código ou repositório.

Crie seu Bot no Discord Developer Portal: https://discord.com/developers/

Acesse o Discord Developer Portal.

Crie uma nova aplicação e, em seguida, adicione um bot a ela.

Copie o Token do seu Bot: Na seção "Bot", clique em "Reset Token" e copie o token gerado.

Habilite os Intents: Na seção "Privileged Gateway Intents", ative "MESSAGE CONTENT INTENT", "PRESENCE INTENT" e "SERVER MEMBERS INTENT". Salve as alterações.

Crie o Arquivo .env:

Na pasta raiz do seu projeto (a mesma onde está o arquivo principal do bot), crie um novo arquivo chamado .env.

Dentro do arquivo .env, adicione a seguinte linha, substituindo YOUR_TOKEN_HERE pelo token que você copiou:

DISCORD_TOKEN=YOUR_TOKEN_HERE

🤝 Adicione o Bot ao seu Servidor Discord
No Discord Developer Portal, vá em "OAuth2" > "URL Generator".

Em "SCOPES", marque a caixa bot.

Em "BOT PERMISSIONS", selecione as permissões necessárias para o bot funcionar (ex: Send Messages, Read Message History, Use External Emojis, Manage Messages).

Copie o URL gerado na parte inferior e cole-o no seu navegador para adicionar o bot ao seu servidor.

▶️ Executando o Bot
Abra um terminal ou prompt de comando na pasta do seu projeto.

Execute o script Python no Terminal:

python TicTacToe-Discord-Bot.py

O bot deverá aparecer online no seu servidor Discord!

📸 Demonstração
![Exemplo de jogabilidade do Jogo da Velha no Discord](img/example.png)