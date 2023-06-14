'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
from config.functions.permissions.is_owner import is_owner

import discord
from discord import app_commands
from discord.ext import commands

class reload(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'reload',
        description = 'Reloads Hayate\'s cogs.'
    )
    @is_owner()
    @app_commands.guild_only()
    async def reload(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = 'Cogs Reload',
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
        )
        
        try:
            cogslist = [
            'extensions.economy.wallet',
            'extensions.economy.daily',
            'extensions.economy.give',
            'extensions.economy.checklist',
            
            'extensions.fun.flags',
            'extensions.fun.emoji',
            'extensions.fun.dice',
            'extensions.fun.ship',

            'extensions.info.github',
            'extensions.info.members', 
            'extensions.info.guild',

            'extensions.utility.ping',
            'extensions.utility.remindme',
            'extensions.utility.time',
            'extensions.utility.info',
            'extensions.utility.snipe',

            'extensions.music.artist',

            'extensions.settings.qotd',
            'extensions.settings.moderator',
            ]

            for ext in cogslist:
                await self.client.unload_extension(ext)
                await self.client.load_extension(ext)

            embed.description = f'**Successfully Reloaded** `{str(len(cogslist))}` **Cogs!**'
            embed.color = 0x575fcf
        except Exception as e:
            embed.description = f'**An error occured:** {e}'
            embed.color = 0xff5e57

        await interaction.response.send_message(embed = embed)

    @reload.error
    async def say_error(self, interaction: discord.Interaction, error):
        embed = discord.Embed(
            title = 'Missing Permissions',
            description = 'You\'re not Hayate\'s owner nor a Hayate\'s tester!',
            color = 0xff5e57,
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
            text = f'Requested by {interaction.user.name}',
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(reload(client))