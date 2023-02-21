import json
import os
import openai
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token='6111266051:AAGb86onJ5-gZb3Nl3szouf7OvaCkjV7SFc')
dispatcher = Dispatcher(bot)

openai.api_key = "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"

data_dir = "./data"

async def get_response(user_message):
    user_id = str(user_message.chat.id)
    filename = f"{data_dir}/{user_id}.json"

    if os.path.exists(f"{user_id}.json"):
        with open(f"{user_id}.json", "r") as f:
            data = json.load(f)
            if user_message.text in data:
                return data[user_message.text]
    
    prompt = f"{user_message.text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response.choices[0].text.strip()
    if os.path.exists(f"{user_id}.json"):
        with open(f"{user_id}.json", "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[user_message.text] = answer
    with open(f"{user_id}.json", "w") as f:
        json.dump(data, f)
    return answer

@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = str(message.chat.id)
    if os.path.exists(f"{user_id}.json"):
        os.remove(f"{user_id}.json")
    await message.reply("Hi, I'm an AI language model. Send me a message and I'll try to continue the conversation!")

@dispatcher.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    user_id = str(message.chat.id)
    if os.path.exists(f"{user_id}.json"):
        os.remove(f"{user_id}.json")
    await message.reply("Goodbye!")

@dispatcher.message_handler()
async def chat_command(message: types.Message):
    user_message = message.text
    response = await get_response(message)

    if response is not None and len(response.strip()) > 0:
        await message.reply(response)
    else:
        await message.reply("I'm sorry, I don't know what to say.")

if __name__ == '__main__':
    executor.start_polling(dispatcher)