import requests as r
from dotenv import load_dotenv
import os
import argparse 

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
grant_type = 'client_credentials'
access_token = os.getenv('ACCESS_TOKEN') 

client_req_params = {'client_id': client_id, 
                    'client_secret': client_secret, 
                    'grant_type': grant_type}

parser = argparse.ArgumentParser(prog='Twitch API CLI (Channels only)', 
        description='What Channel would you like to search?')
parser.add_argument('query')
parser.add_argument('-n', '--next-page')
parser.add_argument('-l', '--live-only', action='store_true')


top_game_headers = {'Authorization': f'Bearer {access_token}', 'Client-Id': client_id }
if __name__ == '__main__':
    args = parser.parse_args()
    query = args.query
    print(f'{args=}')
    params = {'query': args.query, 'first': 20, 'live_only': args.live_only} 
    next_page = args.next_page
    if next_page: 
        params['after'] = next_page 

    
    broadcasters_res = r.get('https://api.twitch.tv/helix/search/channels',
                        params=params, 
                        headers=top_game_headers
                ).json()


    for broadcaster in broadcasters_res['data']:
        _id = broadcaster['id']
        lang = broadcaster['broadcaster_language'] 
        name = broadcaster['display_name']
        game = broadcaster['game_name']
        is_live = broadcaster['is_live']
        title = broadcaster['title']
        print(f'id={_id} {name=} ({lang=}, {is_live=})')
        print(f'\tPlaying {game=} {title=}')

    next_page = broadcasters_res['pagination']
    if 'cursor' in next_page: 
        cursor = next_page['cursor'] 
        print()
        print('to get the next set of channels run')
        print(f'"python3 get_channel_info.py \"{args.query}\" --next-page \"{cursor}\""')


