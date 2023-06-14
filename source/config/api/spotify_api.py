'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import base64
import json

from config.load_env import spotify_id, spotify_secret
from requests import get, post

def get_token():
    auth_string = spotify_id + ':' + spotify_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

def search_for_artist(artist_name, token = None):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)['artists']['items']
    
    if len(json_result) == 0:
        result = 'Couldn\'t find any artist under this name...'
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)['tracks']
    json_result = json_result[:3]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)['items']
    return json_result
