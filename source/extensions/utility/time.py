'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime

import discord
import pytz
from discord import app_commands
from discord.ext import commands

class time(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'time',
        description = 'Returns actual time for the most important timezones.'
    )
    @app_commands.guild_only()
    async def dice(self, interaction: discord.Interaction):
        timezones = [
            "UTC",
            "GMT",
            "America/New_York",
            "America/Chicago",
            "America/Los_Angeles",
            "Europe/Berlin",
            "Europe/Athens",
            "Australia/Sydney",
            "Asia/Tokyo"
        ]
        current_time = datetime.datetime.now()

        embed = discord.Embed(
            title = 'Current Time',
            color = 0x575fcf,
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
        )

        for timezone in timezones:
            tz = pytz.timezone(timezone)
            time_in_timezone = current_time.astimezone(tz)
            formatted_time = time_in_timezone.strftime("%Y-%m-%d %H:%M")
            embed.add_field(
                name = f'<:time:1117463834135896155>  {timezone}',
                value = formatted_time
            )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(time(client))