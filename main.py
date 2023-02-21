import json
import os
import openai
import aiogram

# Importing necessary modules from aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ParseMode

# Importing necessary modules from your project
from database import session, User, Base, engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Create tables in the database (if they don't already exist)
Base.metadata.create_all(bind=engine)

# Configure the SQLAlchemy registry
scoped_session(sessionmaker(bind=engine)).configure(bind=engine)

# Initializing the bot object with its API token
bot = Bot(token='BOT_API')

# Initializing the dispatcher object to handle incoming messages
dispatcher = Dispatcher(bot)

# Initializing the OpenAI API key
openai.api_key = "OPEN_AI_API_KEY"

# The function to get the response from OpenAI's GPT-3 API
async def get_response(user_message):
    user_id = str(user_message.chat.id)

    # Constructing the filename for the user data
    filename = f"{data_dir}/{user_id}.json"

    # Check if the user data file exists and if the user's message is in it
    if os.path.exists(f"{user_id}.json"):
        with open(f"{user_id}.json", "r") as f:
            data = json.load(f)
            if user_message.text in data:
                return data[user_message.text]

    # If the user data file doesn't exist or doesn't contain the user's message, use GPT-3 to generate a response
    prompt = f"{user_message.text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the response from GPT-3
    answer = response.choices[0].text.strip()

    # Update the user data file with the new message and its generated response
    if os.path.exists(f"{user_id}.json"):
        with open(f"{user_id}.json", "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[user_message.text] = answer
    with open(f"{user_id}.json", "w") as f:
        json.dump(data, f)

    # Return the generated response
    return answer

# The function to handle the '/start' command
@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.chat.id

    # Check if the user already exists in the database
    user = session.query(User).filter(User.chat_id == user_id).first()

    if not user:
        # If the user doesn't exist, create a new entry in the database
        user = User(chat_id=user_id, username=message.chat.username)
        session.add(user)
        session.commit()

        # Send a welcome message and an inline keyboard with two buttons
        await message.reply("Hi, I'm an AI language model. Send me a message and I'll try to continue the conversation!")

        # create the inline keyboard
        inline_kb = InlineKeyboardMarkup()

        # create the first button with its callback data
        btn1 = InlineKeyboardButton('Yes, i do! 🤨', callback_data='faq')
        inline_kb.add(btn1)

        # create the second button with its callback data
        btn2 = InlineKeyboardButton("No, i don't! 💩", callback_data='pro_user')
        inline_kb.add(btn2)

        # Send the message with the inline keyboard
        await bot.send_message(message.chat.id, "You want to understand how it all works here?:", reply_markup=inline_kb)
    else:
        # If the user already exists in the database, send a welcome back message
        prompt = f"Hi, I'm back in touch!"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        ).choices[0].text.strip()
        await message.reply(response)    

# The function to handle the '/stop' command
@dispatcher.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    user_id = str(message.chat.id)

    # If the user data file exists, remove it
    if os.path.exists(f"{user_id}.json"):
        os.remove(f"{user_id}.json")

    # Send a goodbye message
    await message.reply("Goodbye!")

# The function to handle incoming chat messages
@dispatcher.message_handler()
async def chat_command(message: types.Message):
    user_message = message.text

    # Use GPT-3 to generate a response to the user's message
    response = await get_response(message)

    if response is not None and len(response.strip()) > 0:
        # If a response was generated, send it back to the user
        await message.reply(response)
    else:
        # If no response was generated, send an apology message
        await message.reply("I'm sorry, I don't know what to say.")

if __name__ == '__main__':
    # Start the bot
    executor.start_polling(dispatcher)
