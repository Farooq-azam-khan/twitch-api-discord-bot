import requests as r
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
grant_type = 'client_credentials'

get_oauth_token_url: str = 'https://id.twitch.tv/oauth2/token'
client_req_params = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': grant_type}

def get_access_token():
    auth_key = r.post(get_oauth_token_url, params=client_req_params)
    return auth_key

access_token = os.getenv('ACCESS_TOKEN') 
top_game_headers = {'Authorization': f'Bearer {access_token}', 'Client-Id': client_id }
top_games_res = r.get('https://api.twitch.tv/helix/games/top',
                      headers=top_game_headers)

if __name__ == '__main__':
    for game in top_games_res.json()['data']:
        print(f'name={game["name"]}')
