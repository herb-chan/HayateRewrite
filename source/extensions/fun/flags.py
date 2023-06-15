'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

from typing import Optional

import discord
from config.functions.flags import show_stats, show_top, start_game
from discord import app_commands
from discord.ext import commands
from main import Hayate

class flags(commands.GroupCog, name='flags'):
    def __init__(self, client: Hayate):
        self.client: Hayate = client
    
    @app_commands.command(
        name = 'guess',
        description = 'Lets you start a minigame of game of flags.'
    )
    @app_commands.describe(
        mode = 'Let\'s you choose between modes.'
    )
    @app_commands.choices(
        mode = [
            discord.app_commands.Choice(name = 'Europe', value = 1),
            discord.app_commands.Choice(name = 'Asia', value = 2),
            discord.app_commands.Choice(name = 'Africa', value = 3),
            discord.app_commands.Choice(name = 'America', value = 4),
        ]
    )
    @app_commands.guild_only()
    async def guess(
        self,
        interaction: discord.Interaction,
        mode: int
    ):
        await start_game(self, interaction=interaction, mode=mode)
    
    @app_commands.command(
        name = 'statistics',
        description = 'Returns a bunch of statistics for nerds regarding the game of flags.'
    )
    @app_commands.describe(
        mode = 'Let\'s you choose between modes.',
        member = 'Member which statistics you want to see, skip to view yours.'
    )
    @app_commands.choices(
        mode = [
            discord.app_commands.Choice(name = 'Europe', value = 1),
            discord.app_commands.Choice(name = 'Asia', value = 2),
            discord.app_commands.Choice(name = 'Africa', value = 3),
            discord.app_commands.Choice(name = 'America', value = 4),
        ]
    )
    @app_commands.guild_only()
    async def statistics(
        self,
        interaction: discord.Interaction,
        mode: int,
        member: Optional[discord.Member] = None
    ):
        member = member or interaction.user

        stats = show_stats(interaction = interaction, mode=mode, member = member)

        await interaction.response.send_message(embed = stats)

    @app_commands.command(
        name = 'leaderboard',
        description = 'Returns the top 25 players and their streaks.'
    )
    @app_commands.describe(
        mode = 'Let\'s you choose between modes.'
    )
    @app_commands.choices(
        mode = [
            discord.app_commands.Choice(name = 'Europe', value = 1),
            discord.app_commands.Choice(name = 'Asia', value = 2),
            discord.app_commands.Choice(name = 'Africa', value = 3),
            discord.app_commands.Choice(name = 'America', value = 4),
        ]
    )
    @app_commands.guild_only()
    async def leaderboard(
        self,
        interaction: discord.Interaction,
        mode: int
    ):

        top = show_top(interaction = interaction, mode=mode)

        await interaction.response.send_message(embed = top)
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(flags(client))