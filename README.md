## Project Overview
This project contains a Discord bot that is built and deployed using the AWS Serverless Application Model (SAM). The bot's source code runs on AWS Lambda, and it utilizes listener servers as intermediaries between the Lambda function and messaging services like Discord.

The listener servers receive events and messages from Discord and forward them to the AWS Lambda function, which processes the data and sends responses back through the listener servers to Discord. This architecture allows for a scalable and efficient bot that can handle a large number of events and messages.

## Start
1. `python3 install-requirements.py` to install all the dependencies required for the project.
2. `sam build` to build the AWS SAM project, which will package and prepare the Lambda function and related resources.
3. `sam deploy` to create or update the stack in AWS, deploying the Lambda function and configuring the required resources and permissions.

## Environment variables
Create a `.env` file in the root directory to store environment variables. Add the following variables:

- BOT_TOKEN: The Discord bot token for authenticating your bot with the Discord API
- POLYBOT_ENDPOINT: The endpoint for your Polybot API

For example:
BOT_TOKEN=your_discord_bot_token_here
POLYBOT_ENDPOINT=https://your_polybot_endpoint_here


Make sure to replace the placeholders with your actual bot token and Polybot API endpoint.

## Start listeners
`cd listenerServers && python3 discordListener.py` to start the bot listener in Discord