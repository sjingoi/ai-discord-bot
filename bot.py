from chronological import *
from dotenv import load_dotenv
import os
import discord
load_dotenv('keys.env')

openai.api_key = os.environ["OPEN_AI_KEY"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
COMMAND_PREFIX = '$'
AI_COMMAND = 'ai'
AI_ERROR_MESSAGE = 'An internal error has occured. Please try again in a few moments.'


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

async def get_ai_response(input_txt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        max_tokens=1000,
        prompt=input_txt,
        temperature=0.5
    )

    return response['choices'][0]['text']

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_message = message.content
    
    if message.content.startswith(COMMAND_PREFIX):
        user_message = user_message[1:].lstrip()
        if user_message.startswith(AI_COMMAND):
            user_message = user_message[len(AI_COMMAND):].lstrip()
            try:
                ai_response = await get_ai_response(user_message)
            except:
                ai_response = AI_ERROR_MESSAGE
            print("Response length:", len(ai_response))
            if len(ai_response) > 2000:
                for section in range(0, len(ai_response), 2000):
                    await message.reply(ai_response[section:section + 2000])
            else:
                await message.reply(ai_response)

@client.event
async def on_ready():
    print("Bot is ready.")


if __name__ == "__main__":

    client.run(DISCORD_TOKEN)

