'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
from typing import Optional

import discord
from config.load_env import mongo
from discord import app_commands
from discord.ext import commands, tasks

# database collections
db = mongo['Guilds']
moderator_rank = db['Moderators']

class moderator(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'moderator',
        description = 'Configure moderator rank for your server.'
    )
    @app_commands.describe(
        create = 'Creates moderator rank for the current guild if there isn\'t one set.',
        rank = 'Makes specified role a moderator one.',
        grant = 'Grants specified user a moderator role.',
        revoke = 'Revokes moderator role from specified user.',
        list = 'If chosen to show, replies with complete list of all the moderator ranks and list of users that have them.'
    )
    @app_commands.choices(
        list = [
            discord.app_commands.Choice(name = 'Show', value = 1)
        ]
    )
    @app_commands.guild_only()
    async def moderator(
        self,
        interaction: discord.Interaction,
        create: Optional[str] = None,
        rank: Optional[discord.Role] = None,
        grant: Optional[discord.Member] = None,
        revoke: Optional[discord.Member] = None,
        list: Optional[int] = 0
    ):
        user_avatar = interaction.user.avatar
        guild = interaction.guild

        if create is not None and rank is None and grant is None and revoke is None and list == 0:
            await interaction.response.send_message(content = 'The command is yet to be done.')
        
        elif create is None and rank is not None and grant is None and revoke is None and list == 0:
            await interaction.response.send_message(content = 'The command is yet to be done.')
        
        elif create is None and rank is None and grant is not None and revoke is None and list == 0:
            await interaction.response.send_message(content = 'The command is yet to be done.')
        
        elif create is None and rank is  None and grant is None and revoke is not None and list == 0:
            await interaction.response.send_message(content = 'The command is yet to be done.')
        
        elif create is None and rank is None and grant is None and revoke is None and list == 1:
            await interaction.response.send_message(content = 'The command is yet to be done.')
        else:
            too_many = discord.Embed(
                    description = f'Unfortunately, you can\'t set up multiple things all at once. Try setting them up one at a time.',
                    color = 0xff5e57,
                    timestamp = datetime.datetime.utcnow()
                )
            too_many.set_footer(
                    text = f'Requested by {interaction.user.name}', 
                    icon_url = user_avatar
                )

            await interaction.response.send_message(embed = too_many)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(moderator(client))