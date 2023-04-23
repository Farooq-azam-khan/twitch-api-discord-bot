import random 
from dotenv import load_dotenv
import discord 
import os 

load_dotenv() 
discord_token = os.getenv('DISCORD_BOT_TOKEN')

# Twitch Setup 
twitch_client_id = os.getenv('CLIENT_ID')

grant_type = 'client_credentials'
twitch_access_token = os.getenv('ACCESS_TOKEN') 

headers = {'Authorization': f'Bearer {twitch_access_token}', 
                    'Client-Id': twitch_client_id }

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

import requests 
import json 

def get_games() -> str: 
    params = {'first': 10} 
    top_games_res = requests.get('https://api.twitch.tv/helix/games/top',
                        params=params, 
                        headers=headers
                ).json()
    if 'data' in top_games_res: 
        ret_format = '' 
        for i, game_obj in enumerate(top_games_res['data']):
            ret_format += f'{i+1}. `{game_obj["name"]}`\n'
        return ret_format
    return 'My apologies, there was an error when I tried to fetch the top games.'


def get_user(username: str) -> str: 
    params = {'login': username}
    res = requests.get(f'https://api.twitch.tv/helix/users',
                        params, 
                        headers=headers)
    data = res.json()['data'] 
    if len(data) < 1: 
        return f'Could not find user with username `{username}`'
    return f'`{json.dumps(data[0], indent=2)}`'

def get_channel_info(query:str) -> str: 
    params = {'broadcaster_id': query, 'first': 10, 'live_only': False} 
    broadcasters_res = requests.get('https://api.twitch.tv/helix/channels',
                        params=params, 
                        headers=headers
                ).json()
    if 'data' in broadcasters_res: 
        if len(broadcasters_res['data']) == 0: 
            return f'No user with query `{query}` exits' 

        resp_format = '' 
        for broadcaster in broadcasters_res['data']:
            lang = broadcaster['broadcaster_language'] 
            name = broadcaster['broadcaster_name']
            game = broadcaster['game_name']
            #is_live = broadcaster['is_live']
            #live_message = 'not live.' if not is_live else f'live'
            delay = broadcaster['delay']
            title = broadcaster['title']
            tags = ', '.join(broadcaster['tags'])
            resp_format += f'**{name}** speaks {lang} and plays {game}. The stream title is **{title}** with a delay of {delay}. The tags are {tags}.\n\n'
        return resp_format
    print(broadcasters_res) 
    return f'An error occured when parsing the channel info for query `{query}`.'



def handle_response(message) -> str: 
    p_message = message.lower() 
    if p_message == '!help': 
        return '''Hello, I'm twitch-bot, your personal assistant for all things Twitch! Here are a few commands you can use to get started:

`!games` - I'll show you the top 10 games currently being played on Twitch.

`!user [username]` - I'll give you information about a specific Twitch user.

`!channel_info [id]` - I'll give you information about a specific twitch channel if you provide me it's id. You get get the id by running `!user [username]` command. 

To receive the response via private message, simply add a question mark before the command (e.g. ?!games instead of !games).

Give these commands a try, and if you would like any new features added, contact the developer. You know who that is.'''

    if p_message.startswith('!games'):
        return get_games() 
    elif p_message.startswith('!user '):
        splt = p_message.split(' ')
        if len(splt) >= 2:
            username = ' '.join(splt[1:])
            return get_user(username) # f'TODO(!user {username})'
        else: 
            return f'You did not provide a username'
    elif p_message.startswith('!channel_info '):
        splt = p_message.split(' ')
        if len(splt) >= 2: 
            channel_query = ' '.join(splt[1:])
            return get_channel_info(channel_query) # f'TODO(!channel_info {channel_query})'
        return 'You did not provide a channel query'
    return f'Could not process message {message}'


    return f'Could not parse `{p_message}`.'

async def send_message(message, user_message, is_private): 
    if user_message.startswith('!'):
        response = handle_response(user_message)
        if is_private:
            await message.author.send(response) 
        else: 
            await message.channel.send(response)

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
    client.run(discord_token)


if __name__ == '__main__':
    run_discord_bot() 

