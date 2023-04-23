import requests as r
from dotenv import load_dotenv
import os
import argparse 

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
grant_type = 'client_credentials'

get_oauth_token_url: str = 'https://id.twitch.tv/oauth2/token'
client_req_params = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': grant_type}
access_token = os.getenv('ACCESS_TOKEN') 

parser = argparse.ArgumentParser(prog='Twitch API CLI (Games only)', 
        description='')
parser.add_argument('-n', '--next-games')


top_game_headers = {'Authorization': f'Bearer {access_token}', 'Client-Id': client_id }
if __name__ == '__main__':
    args = parser.parse_args()
    next_games = args.next_games
    params = {'first': 10} 
    
    if next_games: 
        print('getting after', next_games)
        params['after'] = next_games
    top_games_res = r.get('https://api.twitch.tv/helix/games/top',
                        params=params, 
                        headers=top_game_headers
                ).json()


    for game in top_games_res['data']:
        name = game['name'] 
        igdb_id = game['igdb_id']
        print(f'{igdb_id=} {name=}')
    print()
    next_page = top_games_res['pagination']['cursor']
    print(f'if you want the next 10 run:\n"python3 get_games.py --next-games=\"{next_page}\""')
