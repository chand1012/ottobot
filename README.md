# OttoBot - Self-hosted ChatGPT Discord Bot

Welcome to OttoBot, a self-hosted [ChatGPT](https://chat.openai.com/) Discord bot designed for users who want to host their own powerful AI-assistant on their Discord server.

## Prerequisites

In order to run the OttoBot, you need the following:

1. A Discord Bot Token. You can create one by following [these instructions](https://www.writebots.com/discord-bot-token/).
2. An OpenAI API key. You can obtain one by signing up for an account at [OpenAI](https://platform.openai.com/signup/).
3. [Docker](https://www.docker.com/) installed on your system for building and running the bot.

## Running the bot using Docker

To run the bot with Docker, follow these steps:

1. Clone the repository: `git clone https://github.com/chand1012/ottobot.git`.
2. `cd` into the directory: `cd ottobot`.
3. Create a `.env` file in the project directory with the following values:

```
TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_discord_bot_token` and `your_openai_api_key` with your actual Discord bot token and OpenAI API key respectively.

4. Build the Docker image: `docker build -t ottobot .`.
5. Run the Docker container: `docker run -d --name ottobot --env-file .env ottobot`.

Now the bot should be up and running, and you can invite it to your Discord server by following the [instructions provided here](https://www.writebots.com/discord-bot-token/).

## Usage

To start a conversation with the bot, use the `/chat` slash command in any text channel. This will create a thread that you can use to chat with the AI assistant, Otto. Specify the model to use by appending it as a parameter, like `/chat gpt-3.5-turbo` , or use the default model by simply typing `/chat` .

To end the conversation and delete the thread, use the `/delete` slash command while inside the thread.

## Contributing

Feel free to contribute, report bugs, or provide feedback by opening an issue or submitting a pull request on [GitHub](https://github.com/chand1012/ottobot).
