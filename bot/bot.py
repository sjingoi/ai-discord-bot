import openai
from dotenv import load_dotenv, find_dotenv
import os
import discord

env_dir = find_dotenv('keys.env', True)
load_dotenv(env_dir)

openai.api_key = os.environ["OPEN_AI_KEY"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
COMMAND_PREFIX = '%'
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

    content = message.content
    
    if message.content.startswith(COMMAND_PREFIX):
        content = content[1:].lstrip()
        await execute_cmd(content, message)


async def execute_cmd(command: str, message = None):
    match command.split():
        case [AI_COMMAND, *args]:
            prompt = lst_to_string(args)
            ai_response = await query_ai(prompt)
            for section in range(0, len(ai_response), 2000):
                await message.reply(ai_response[section:section + 2000])


async def query_ai(prompt: str) -> str:
    try:
        ai_response = await get_ai_response(prompt)
    except:
        ai_response = AI_ERROR_MESSAGE
    return ai_response


def lst_to_string(lst: list[str]) -> str:
    words = ""
    for word in lst:
        words += word + " "
    return words[:-1]


@client.event
async def on_ready():
    print("Bot is ready.")


if __name__ == "__main__":

    client.run(DISCORD_TOKEN)
