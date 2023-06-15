'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import asyncio
import datetime

import discord
from discord import app_commands
from discord.ext import commands
from main import Hayate

class remindme(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
        name = 'remindme',
        description = 'Send a reminder after provided time.'
    )
    @app_commands.describe(
        time = 'Time for which Hayate will wait to send reminder.',
        unit = 'Specify in what unit is the time provided.',
        reminder = 'Reminder that will be sent by Hayate once the time passses.'
    )
    @app_commands.choices(
        unit = [
            discord.app_commands.Choice(name = 'seconds', value = 1),
            discord.app_commands.Choice(name = 'minutes', value = 2),
            discord.app_commands.Choice(name = 'hours', value = 3),
            discord.app_commands.Choice(name = 'days', value = 4),
        ]
    )
    @app_commands.guild_only()
    async def remindme(self, interaction: discord.Interaction, time: int, unit: int, reminder: str):
        reminded_user = interaction.user.id
        
        if unit == 1:
            duration = time
            time_unit = 'seconds'
        elif unit == 2:
            duration = time * 60
            time_unit = 'minutes'
        elif unit == 3:
            duration = time * 60 * 60
            time_unit = 'hours'
        elif unit == 4:
            duration = time * 60 * 60 * 24
            time_unit = 'days'

        embed = discord.Embed(
            title = 'Reminder has been set.',
            description = f'I will remind you in **{time} {time_unit}**!',
            color = 0x575fcf,
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)
        await asyncio.sleep(duration)

        reminder_embed = discord.Embed(
            title = 'Reminder!',
            description = reminder,
            color = 0x575fcf,
            timestamp = datetime.datetime.now()
        )
        reminder_embed.set_footer(
                text = f'Reminding {interaction.user.name}',
                icon_url = interaction.user.avatar
        )

        await interaction.channel.send(content = f'<@{reminded_user}>', embed = reminder_embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(remindme(client))