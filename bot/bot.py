from dotenv import load_dotenv, find_dotenv
import os
import discord
import ai
import database

env_dir = find_dotenv('secrets.env', True)
load_dotenv(env_dir)

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
VALID_API_KEY = 'Key validated and set.'
INVALID_API_KEY = 'The key provided is invalid. You can find your API key at https://beta.openai.com/account/api-keys.'
NO_PERMISSION = 'You do not have permission to use this command.'


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content

    
    server_id = message.guild.id
    server_name = message.guild.name

    server_prefix = database.get_cmd_prefix(server_id)

    if server_prefix == None and not database.server_in_database(server_id):
        database.add_server(server_id, server_name)
        server_prefix = '$'

    if content.startswith(server_prefix):
        content = content[1:].lstrip()
        await execute_cmd(content, message)


async def execute_cmd(command: str, message = None):
    server_id = message.guild.id
    match command.split():

        # AI COMMAND
        case ["ai", *args]:
            prompt = lst_to_string(args)
            ai_response = await ai.query_ai(prompt, server_id)
            for section in range(0, len(ai_response), 2000):
                await message.reply(ai_response[section:section + 2000])

        # SET COMMAND PREFIX
        case ["setprefix", prefix]:
            if message.author.guild_permissions.administrator:
                if len(prefix) == 1:
                    database.update_prefix(server_id, prefix)
            else:
                await message.reply(NO_PERMISSION)

        # SET OPENAI API KEY
        case ["setkey", key]:
            if message.author.guild_permissions.administrator:
                if await ai.is_valid_key(key):
                    database.update_openai_key(server_id, key)
                    await message.reply(VALID_API_KEY)
                else:
                    await message.reply(INVALID_API_KEY)
            else:
                await message.reply(NO_PERMISSION)


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
