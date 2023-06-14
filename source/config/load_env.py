'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Path to the secret .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'secret', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Get bot token from the .env file
bot_token = os.getenv('BOT_TOKEN')

# Create a new client and connect to the server
mongo_connection = os.getenv('MONGODB_CONNECTION')
uri = mongo_connection
mongo = MongoClient(uri)

# Create a new Spotify API connection
spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
