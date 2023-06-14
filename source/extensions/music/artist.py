'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
import locale
import math

import discord
from config.api.spotify_api import (get_songs_by_artist, get_token, search_for_artist)
from discord import app_commands
from discord.ext import commands

# locale formatting
locale.setlocale(locale.LC_ALL, 'en_US') 

class artists(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
            name = 'artist', 
            description = 'Returns all important information about requested artist.'
            )
    @app_commands.describe(artist = 'Artist which profile you want to see.')
    @app_commands.guild_only()
    async def artist(self, interaction: discord.Interaction, artist: str):
        member = interaction.user

        token = get_token()
        artist_result = search_for_artist(token = token, artist_name = artist)
        artist_id = artist_result['id']

        artist_avatar = artist_result['images'][0]['url']
        artist_name = artist_result['name']
        artist_profile = artist_result['external_urls']['spotify']
        artist_followers = artist_result['followers']['total']
        artist_followers = locale.format_string('%d', artist_followers, grouping = True)
        
        if artist_result['genres'] is None:
            artist_genres = 'None'
        else:
            artist_genres = artist_result['genres']
            genres = ''
            for genre in artist_genres:
                genres += genre + ' '

        artist_embed = discord.Embed(
            color = 0x575fcf,
            timestamp = datetime.datetime.utcnow()
        )
        artist_embed.set_author(
            name = f'{artist_name}\'s Spotify Profile',
            icon_url = artist_avatar,
            url = artist_profile
        )
        artist_embed.add_field(
            name = '<:followers:1118256333838364712> Total followers', value = f'{artist_followers}',
            inline = True
        )
        artist_embed.add_field(
            name = '<:category:1118213343392579634> Genres', value = f'{genres}',
            inline = True
        )
        songs = get_songs_by_artist(token = token, artist_id = artist_id)
        for idx, song in enumerate(songs):
            artist_embed.add_field(
                name=f"<:star:1118256900996341791> {idx + 1}. Top Song",
                value = f"**Name:** {song['name']}\n**Album:** {song['album']['name']}\n**Duration:** {math.ceil(song['duration_ms'] / 60000)}min",
                inline = False
            )
        artist_embed.set_thumbnail(url = artist_avatar)
        artist_embed.set_footer(
            text = f'Requested by {member.name}', 
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = artist_embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(artists(client))
