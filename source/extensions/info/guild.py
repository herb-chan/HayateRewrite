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

class guild(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
            name = 'guild', 
            description = 'Returns all important information about the current guild.'
            )
    @app_commands.guild_only()
    async def guild(self, interaction: discord.Interaction):
        guild_icon = interaction.guild.icon

        # if guild doesn't have it's icon set, display discord logo
        if guild_icon is None:
            guild_icon = 'https://i.imgur.com/5zbw1Gq.png'

        guild_embed = discord.Embed(
            color = 0x575fcf,
            timestamp = datetime.datetime.utcnow()
        )
        guild_embed.set_author(
            name = f'{interaction.guild.name}',
            icon_url = guild_icon
        )

        guild_embed.add_field(
            name = '<:info:1118212340685475861> Guild ID', 
            value = f'{interaction.guild.id}',
            inline = True
         )
        guild_embed.add_field(
            name = '<:calendar:1118212348755312642> Created', 
            value = f'{discord.utils.format_dt(interaction.guild.created_at)}',
            inline = True
        )
        guild_embed.add_field(
            name = '<:category:1118213343392579634>  Channel count',
            value = f'{len(interaction.guild.channels)}',
            inline = True
        )
        guild_embed.add_field(
            name = '<:users:1118212347488649377> Member count',
            value = f'{interaction.guild.member_count}',
            inline = True
        )
        
        guild_embed.add_field(
            name = '<:ticket:1118212335773950024> Role count',
            value = f'{len(interaction.guild.roles)}',
            inline = True
        )
        guild_embed.add_field(
            name = '<:emoji:1118213023698526299> Emoji count',
            value = f'{len(interaction.guild.emojis)}',
            inline = True
        )
        guild_embed.set_thumbnail(
            url = f'{guild_icon}'
        )
        guild_embed.set_footer(
            text = f'Requested by {interaction.user.name}', 
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = guild_embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(guild(client))
