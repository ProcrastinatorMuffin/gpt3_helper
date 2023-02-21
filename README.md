# gpt3_helper
GPT-3 Telegram Bot
This is a Telegram bot that uses the OpenAI GPT-3 API to generate responses to user messages. The bot is built using the Python Aiogram library and the SQLAlchemy ORM to store user information and message history in a SQLite database.

## Features
Users can send messages to the bot and receive generated responses from GPT-3
User information is stored in a database, including their Telegram username and chat ID
The bot provides a FAQ feature, which can be accessed by clicking the "What can you do?" button
Users who start the bot for the first time will see a greeting message and a button to learn more about the bot's features
The bot can be easily deployed to Heroku

### Requirements
* Python 3.6+
* OpenAI API key
* Telegram Bot API token
* Heroku CLI (if deploying to Heroku)

#### Installation
1. Clone this repository to your local machine
2. Install the required Python packages by running pip install -r requirements.txt in the project directory
3. Set the OPENAI_API_KEY and TELEGRAM_BOT_TOKEN environment variables to your OpenAI API key and Telegram Bot API token, respectively
4. Run the bot using python main.py

##### Usage
* Start a conversation with the bot on Telegram
* Send a message to the bot
* The bot will respond with a generated message from GPT-3
* Click the "What can you do?" button to learn more about the bot's features


###### Deployment
The bot can be deployed to Heroku using the following steps:

1. Create a new Heroku app
2. Set the OPENAI_API_KEY and TELEGRAM_BOT_TOKEN environment variables in the Heroku app's settings
3. Add the Procfile and runtime.txt files to the project directory
4. Push the code to the Heroku app's Git repository using git push heroku main


###### License
This project is licensed under the MIT License - see the LICENSE file for details.
