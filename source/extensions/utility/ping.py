'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime

import discord
from discord import app_commands
from discord.ext import commands
from main import Hayate

class ping(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
        name = 'ping',
        description = 'Returns ping of a current shard.'
    )
    @app_commands.guild_only()
    async def ping(self, interaction: discord.Interaction):
        ctx = await self.client.get_context(interaction)
        shard_id = ctx.guild.shard_id
        latency = self.client.latency

        embed = discord.Embed(
            title = ':ping_pong: Pong!',
            description = f'<:info:1118212340685475861> **Shard ID:** `{shard_id}`\n<:timer:1117463845036892190> **Latency:** `{round(latency * 1000)}ms`',
            color = 0x575fcf,
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ping(client))