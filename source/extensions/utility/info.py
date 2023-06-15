'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
import platform

import discord
import psutil
from discord import app_commands
from discord.ext import commands
from main import Hayate

class info(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
        name = 'info',
        description = 'Returns all the important and nerdy stuff about Hayate.',
    )
    @app_commands.guild_only()
    async def info(self, interaction: discord.Interaction):
        # cpu & ram usages
        ram_usage = psutil.Process().memory_full_info().rss / 1024 ** 2
        cpu_usage = psutil.cpu_percent()

        # server information
        total_servers = len(self.client.guilds)
        total_channels = sum(len(guild.channels) for guild in self.client.guilds)
        total_members = sum(guild.member_count for guild in self.client.guilds)
        avg_members = sum(g.member_count for g in self.client.guilds) // len(self.client.guilds)
        
        # system information
        python_version = platform.python_version()
        discordpy_version = discord.__version__
        os_info = platform.system()

        # ping
        latency = self.client.latency

        embed = discord.Embed(
            title = 'Hayate Information',
            description = f'Here\'s a handful of information about Hayate! If you need help with comands, use `/help`.',
            color = 0x575fcf,
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
        )
        embed.add_field(
            name = 'Current Guild',
            value = f'```md\n<User_ID: {interaction.user.id}>\n<Channel_ID: {interaction.channel.id}>\n<Guild_ID: {interaction.guild.id}>```',
            inline = False
        )
        embed.add_field(
            name = 'Global Statistics',
            value = f'```md\n<Guilds: {total_servers}>\n<Channels: {total_channels}>\n<Users: {total_members}>\n<Avg_Users: {avg_members}>```',
            inline = False
        )
        embed.add_field(
            name = 'Bot Information',
            value = f'```md\n<Ping: {round(latency * 1000)}ms>\n<RAM_Usage: {round(ram_usage, 1)}mb>\n<CPU_Usage: {cpu_usage}>```',
            inline = False
        )
        embed.add_field(
            name = 'Project Information',
            value = f'```md\n<Python: {python_version}>\n<Discord.py: {discordpy_version}>\n<OS: {os_info}>```',
            inline = False
        )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(info(client))