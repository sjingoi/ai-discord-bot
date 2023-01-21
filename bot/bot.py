from dotenv import load_dotenv, find_dotenv
import os
import discord
import traceback

# PROJECT FILES
import ai
import database


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

env_dir = find_dotenv('secrets.env', True)
load_dotenv(env_dir)

# CONSTANT DECLARATIONS
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
BOT_ADMIN_ID = int(os.environ["BOT_ADMIN_ID"])
JOIN_MESSAGE = "Hi, it seems like you or one of your members has added me to your lovely server!\n\nHere are some commands to get started:\n\n```\n$ai [your message here] - Use this to talk with the bot!\n\n$setprefix [Your custom prefix here] - Allows you to change character in front of message (Default is $)\n\n$setkey [Your key pasted from the OpenAI website] - Allows you to use your own key for the bot, letting you use it for longer. (HIGHLY RECOMMENDED) \n\n$help - When you need a reminder of the commands for the bot```"
VALID_API_KEY = 'Key validated and set.'
INVALID_API_KEY = 'The key provided is invalid. You can find your API key at https://beta.openai.com/account/api-keys.'
NO_PERMISSION = 'You do not have permission to use this command.'
HELP_MSG = 'Commands:\n$ai - talk to ai\n$setkey - set api key\n$setprefix - Change the command prefix (default = $)\nMessage <@' + str(BOT_ADMIN_ID) + '> for more help'

from database import SERVERS_TABLE, SERVER_ID_COL, SERVER_NAME_COL, SERVER_CMD_PFX_COL, SERVER_AI_KEY_COL, SERVER_OWNER_COL
from database import USERS_TABLE, USER_ID_COL, USER_NAME_COL, USER_NUM_OF_REQ_COL, USER_CMD_PFX_COL, USER_AI_KEY_COL

### BOT ##########################################################################

@client.event
async def on_guild_join(guild):
    await guild.owner.send(JOIN_MESSAGE)


@client.event
async def on_message(message):

    # CHECKS IF MESSAGE IS FROM THIS BOT
    if message.author == client.user:
        return

    try:
        user = message.author
        update_user(user)

        if message.guild != None:
            server_id = message.guild.id
            update_server(message.guild)

            prefix = database.get_from_table(SERVERS_TABLE, SERVER_ID_COL, server_id, SERVER_CMD_PFX_COL)
        
        else:
            server_id = None

            prefix = database.get_from_table(USERS_TABLE, USER_ID_COL, user.id, USER_CMD_PFX_COL)

        # CHECKS IF MESSAGE IS A COMMAND
        content = message.content 
        if content.startswith(prefix):
            command = content[1:].lstrip()
            await execute_cmd(command, message)

    except Exception as e:
        # SENDS A MESSAGE TO BOT ADMIN IN CASE OF ERROR
        bot_admin = client.get_user(BOT_ADMIN_ID)
        await bot_admin.send("Bot encountered an error: \n`" + str(e) + "`")
        # await bot_admin.send("\n Server: " + server_name + "\n")

        traceback.print_exc()


async def execute_cmd(command: str, message = None):
    user_id = message.author.id

    if message.guild != None:
        server_id = message.guild.id

    else:
        server_id = None
    
    user_id = message.author.id
    match command.split():


        # AI COMMAND
        case ["ai", *args]:
            database.increment(USERS_TABLE, USER_ID_COL, user_id, USER_NUM_OF_REQ_COL)

            if server_id is None:
                api_key = database.get_from_table(USERS_TABLE, USER_ID_COL, user_id, USER_AI_KEY_COL)
            else:
                api_key = database.get_from_table(SERVERS_TABLE, SERVER_ID_COL, server_id, SERVER_AI_KEY_COL)

            prompt = lst_to_string(args)
            ai_response = await ai.query_ai(prompt, api_key)
            
            for section in range(0, len(ai_response), 2000):
                await message.reply(ai_response[section:section + 2000])


        # SET COMMAND PREFIX
        case ["setprefix", prefix]:
            if len(prefix) == 1:
                if server_id is None:
                    database.update_table(USERS_TABLE, USER_ID_COL, user_id, USER_CMD_PFX_COL, prefix)
                else:
                    if message.author.guild_permissions.administrator:
                        database.update_table(SERVERS_TABLE, SERVER_ID_COL, server_id, SERVER_CMD_PFX_COL, prefix)
                    else:
                        await message.reply(NO_PERMISSION)
                await message.reply('Prefix set to ' + prefix + '.')
            else:
                await message.reply('Prefix must be exactly 1 character long.')
            
                


        # SET OPENAI API KEY
        case ["setkey", key]:
            if await ai.is_valid_key(key):
                if server_id is None:
                    database.update_table(USERS_TABLE, USER_ID_COL, user_id, USER_AI_KEY_COL, key)
                else:
                    if message.author.guild_permissions.administrator:
                        database.update_table(SERVERS_TABLE, SERVER_ID_COL, server_id, SERVER_AI_KEY_COL, key)
                    else:
                        await message.reply(NO_PERMISSION)
                await message.reply(VALID_API_KEY)
            else:
                await message.reply(INVALID_API_KEY)
            


        # HELP MESSAGE
        case ["help", *args]:
            await message.channel.send(HELP_MSG)



def update_user(user):
    user_id = user.id
    user_name = user.name
    user_discriminator = user.discriminator
    discord_name = user_name + "#" + user_discriminator

    if not database.in_table(USERS_TABLE, USER_ID_COL, user_id):
        database.add_user(user_id, discord_name)
    else:
        database.update_table(USERS_TABLE, USER_ID_COL, user_id, USER_NAME_COL, discord_name)


def update_server(guild):
    # SERVER PROPERTIES
    server_id = guild.id
    server_name = guild.name
    server_owner_id = guild.owner_id

    # ADDS SERVER IF IT IS NOT IN DATABASE
    if not database.in_table(SERVERS_TABLE, SERVER_ID_COL, server_id):
        database.add_server(server_id, server_name, server_owner_id)
        # server_prefix = '$'
    else:
        database.update_table(SERVERS_TABLE, SERVER_ID_COL, server_id, SERVER_NAME_COL, server_name)
        database.update_table(SERVERS_TABLE, SERVER_ID_COL, server_id, SERVER_OWNER_COL, server_owner_id)

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
