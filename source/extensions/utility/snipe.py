'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime

import discord
from config.load_env import mongo
from discord import app_commands
from discord.ext import commands
from main import Hayate

# database collections
db = mongo['Guilds']
snipes = db['Snipes']

class snipe(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel_id = message.channel.id
        deleted_message = {
            'channel_id': channel_id,
            'guild_id': message.guild.id,
            'author_id': message.author.id,
            'content': message.content,
        }
        existing_message = snipes.find_one({'channel_id': channel_id})
        if existing_message:
            snipes.replace_one({'channel_id': channel_id}, deleted_message)
        else:
            snipes.insert_one(deleted_message)

    @app_commands.command(
        name = 'snipe',
        description = 'Snipes the most recent deleted message.'
    )
    @app_commands.guild_only()
    async def snipe(self, interaction: discord.Interaction):
        channel_id = interaction.channel.id
        deleted_message = snipes.find_one({'channel_id': channel_id})
        
        if deleted_message:
            author_id = deleted_message['author_id']
            content = deleted_message['content']

            embed = discord.Embed(
                title = 'Snipe!',
                description = f'`{content}` - <@{author_id}>',
                color = 0x575fcf,
                timestamp = datetime.datetime.now()
            )
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )   
            
            await interaction.response.send_message(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Snipe Failed',
                description = f'It seems like I can\'t snipe any messages on this channel.',
                color = 0xff5e57,
                timestamp = datetime.datetime.now()
            )
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )   

            await interaction.response.send_message(embed = embed)
        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(snipe(client))