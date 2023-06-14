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
            synced = await self.client.tree.sync()

            embed.description = f'**Successfully Reloaded** `{str(len(synced))}` **Cogs!**'
            embed.color = 0x575fcf
        except Exception as e:
            embed.description = f'**An error occured:** {e}'
            embed.color = 0xff5e57
            print(e)

        await interaction.response.send_message(embed = embed)

    @reload.error
    async def say_error(self, interaction: discord.Interaction):
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