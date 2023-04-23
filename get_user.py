import requests as r
from dotenv import load_dotenv
import os

from pprint import pprint 
import argparse 

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
grant_type = 'client_credentials'
access_token = os.getenv('ACCESS_TOKEN') 
parser = argparse.ArgumentParser(prog='Twitch API CLI (User only)', 
        description='provide a username and you will get data about that twitch user')
parser.add_argument('username')

headers = {'Authorization': f'Bearer {access_token}', 
                    'Client-Id': client_id }
if __name__ == '__main__':
    args = parser.parse_args()
    params = {'login': args.username}
    res = r.get(f'https://api.twitch.tv/helix/users',
                        params, 
                        headers=headers)
    pprint(res.json())

