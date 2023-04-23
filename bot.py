import random 
from dotenv import load_dotenv
import discord 
import os 

load_dotenv() 
token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def handle_response(message) -> str: 
    p_message = message.lower() 
    if p_message == '!help': 
        return '''Hello, I'm twitch-bot, your personal assistant for all things Twitch! Here are a few commands you can use to get started:

`!games` - I'll show you the top 10 games currently being played on Twitch.

`!user [username]` - I'll give you information about a specific Twitch user.

`!channel_info [query]` - I'll help you find Twitch channels that match your search query.

Give these commands a try, and if you would like any new features added, contact the developer. You know who that is.'''

    if p_message.startswith('!games'):
        return 'TODO(games)'
    elif p_message.startswith('!user '):
        splt = p_message.split(' ')
        if len(splt) >= 2:
            username = ' '.join(splt[1:])
            return f'TODO(!user {username})'
        else: 
            return f'You did not provide a username'
    elif p_message.startswith('!channel_info '):
        splt = p_message.split(' ')
        if len(splt) >= 2: 
            channel_query = ' '.join(splt[1:])
            return f'TODO(!channel_info {channel_query})'
        return 'You did not provide a channel query'
    return f'Could not process message {message}'


    return f'Could not parse `{p_message}`.'

async def send_message(message, user_message, is_private): 
    try: 
        if user_message.startswith('!'):
            response = handle_response(user_message)
            if is_private:
                await message.author.send(response) 
            else: 
                await message.channel.send(response)
    except Exception as e: 
        print(e)

@client.event 
async def on_ready(): 
    print(f'{client.user} is now running')

from pprint import pprint 
@client.event
async def on_message(message): 
    if message.author == client.user: 
        return 
    
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    
    print(f'{username=} {user_message=} {channel}')
    if len(user_message) == 0: 
        return 
    private_message = '?'
    is_private_message = user_message[0] == private_message
    formatted_message = user_message[1:] if is_private_message else user_message
    await send_message(message, formatted_message, is_private=is_private_message)
        



def run_discord_bot(): 
    client.run(token)


if __name__ == '__main__':
    run_discord_bot() 

