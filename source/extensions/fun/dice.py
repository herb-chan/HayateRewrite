'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import asyncio
import datetime
import random

import discord
from discord import app_commands
from discord.ext import commands
from main import Hayate

class dice(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
        name = 'dice',
        description = 'Rolls a six sided dice.'
    )
    @app_commands.guild_only()
    async def dice(self, interaction: discord.Interaction):
        result = random.randint(1, 6)

        embed = discord.Embed(
            title = f'{interaction.user.display_name}\'s Roll Result',
            description = f'You rolled **{result}** :game_die:',
            color = 0x575fcf,
            timestamp = datetime.datetime.now(),  
        )
        embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(dice(client))