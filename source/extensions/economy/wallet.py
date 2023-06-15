'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
import locale
from typing import Optional

import discord
from config.functions.checks.check_wallet import check_wallet
from config.load_env import mongo
from discord import app_commands
from discord.ext import commands
from main import Hayate

# locale formatting
locale.setlocale(locale.LC_ALL, 'en_US') 

# database collection
db = mongo['Users']
money = db['Wallets']

class wallet(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
        name = 'wallet',
        description = 'Returns ammount of money provided user has.'
    )
    @app_commands.describe(
        user = 'Whose wallet you want to view.'
    )
    @app_commands.guild_only()
    async def wallet(self, interaction: discord.Interaction, user: Optional[discord.Member]):
        user = user or interaction.user
        
        balance = check_wallet(interaction = interaction, user = user)

        balance = locale.format_string('%d', balance, grouping = True)

        embed = discord.Embed(
            description = f'<@{user.id}> currently has 💷 `{balance} cash`',
            color = 0x575fcf,
            timestamp = datetime.datetime.now()  
        )
        embed.set_author(
            name = f'{user.display_name}\'s Wallet',
            icon_url = user.avatar
        )
        embed.set_footer(
            text = f'Requested by {interaction.user.name}',
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(wallet(client))