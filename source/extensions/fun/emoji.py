'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import asyncio
import datetime
import unicodedata

import discord
import requests
from discord import app_commands
from discord.ext import commands

class emoji(commands.GroupCog, name = 'emoji'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'enlarge',
        description = 'Enlarges chosen emoji and sends in a downloadable form.'
    )
    @app_commands.describe(
        emoji = 'Emoji that you want to enlarge.'
    )
    @app_commands.guild_only()
    async def enlarge(self, interaction: discord.Interaction, emoji: str):
        try:
            ctx = await self.client.get_context(interaction)
            emoji_object = await commands.PartialEmojiConverter().convert(ctx, emoji)
            emoji_url = emoji_object.url
            emoji_name = emoji_object.name
            emoji_id = emoji_object.id
            
            embed = discord.Embed(
                title = "Enlarged Emoji",
                description = f'<:customization:1117463839324241991> **Name:** `{emoji_name}`\n<:info:1118212340685475861> **ID:** `{emoji_id}`', 
                color = 0x575fcf,
                timestamp = datetime.datetime.now()
                )
            embed.set_image(url = emoji_url)
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )

            await interaction.response.send_message(embed = embed)
        
        except commands.PartialEmojiConversionFailure:
            try:
                emoji_string = unicodedata.name(emoji).lower()
            except:
                embed = discord.Embed(
                    title = "Invalid emoji",
                    description = f'Unfortunately the name you provided isn\'t suitable for an emoji.\n```{emoji}```', 
                    color = 0xff5e57,
                    timestamp = datetime.datetime.now()
                    )
                embed.set_footer(
                    text = f'Requested by {interaction.user.name}',
                    icon_url = interaction.user.avatar
                )
                await interaction.response.send_message(embed = embed, delete_after = 5)
                return
                
            discord_emoji = hex(ord(emoji))[2:]
            discord_emoji_enlarge = f'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/{discord_emoji}.png'

            embed = discord.Embed(
                title = "Enlarged emoji",
                description = f'**Name:** `{emoji_string}`', 
                color = 0x575fcf,
                timestamp = datetime.datetime.now()
            )
            embed.set_image(url = discord_emoji_enlarge)
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )

            await interaction.response.send_message(embed = embed)

    @app_commands.command(
    name='steal',
    description='Steal\'s provided emoji and adds it to the current guild.'
    )
    @app_commands.describe(
        emoji='Emoji that you want to steal.'
    )
    @app_commands.guild_only()
    async def steal(self, interaction: discord.Interaction, emoji: str):
        try:
            ctx = await self.client.get_context(interaction)
            emoji_object = await commands.PartialEmojiConverter().convert(ctx, emoji)
            emoji_url = emoji_object.url

            embed = discord.Embed(
                title = 'Stealing emoji...',
                description = 'You have **15s** to provide a name for the emoji. Please do it within new message.',
                color = 0x2b2d31,
                timestamp = datetime.datetime.now()
            )
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )

            await interaction.response.send_message(content = 'Stealing emoji...', delete_after = 0.01)
            message = await interaction.channel.send(embed = embed)

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel

            try:
                emoji_name = await self.client.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                time_fail = discord.Embed(
                    title = 'Canceling...',
                    description = f'Time\'s up! You didn\'t provide suitable name for the emoji.',
                    color = 0xff5e57,
                    timestamp = datetime.datetime.utcnow()
                )
                time_fail.set_footer(
                    text = f'Requested by {interaction.user.name}',
                    icon_url = interaction.user.avatar
                )

                await message.edit(embed = time_fail, delete_after = 3)
                return

            emoji_name_fixed = emoji_name.content.lower().replace(' ', '_')
            name_length = len(emoji_name_fixed)
            if name_length < 2 or name_length > 32:
                length_fail = discord.Embed(
                    title = 'Canceling...',
                    description = 'The name you provided was either too short or too long. Remember that a name can\'t be shorter than **2** characters and longer than **32**.',
                    color = 0xff5e57,
                    timestamp = datetime.datetime.utcnow()
                )
                length_fail.set_footer(
                    text = f'Requested by {interaction.user.name}',
                    icon_url = interaction.user.avatar
                )

                await message.edit(embed = length_fail, delete_after = 3)
                await emoji_name.delete()
            else:
                response = requests.get(emoji_url)
                emoji_bytes = response.content
                
                await interaction.guild.create_custom_emoji(name = emoji_name_fixed, image = emoji_bytes)
                
                success = discord.Embed(
                    title = 'Emoji Stolen',
                    description = f'You may now use the `:{emoji_name_fixed}:` on your server!',
                    color = 0x575fcf,
                    timestamp = datetime.datetime.now()
                )
                success.set_footer(
                    text = f'Requested by {interaction.user.name}',
                    icon_url = interaction.user.avatar
                )
                
                await message.edit(embed = success)
                await emoji_name.delete()
        
        except commands.PartialEmojiConversionFailure:
            embed = discord.Embed(
                title = "Invalid emoji",
                description = f'Unfortunately you didn\'t provide emoji i could steal. Try providing some custom emojis.\n```{emoji}```', 
                color = 0xff5e57,
                timestamp = datetime.datetime.now()
            )
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )
            await interaction.response.send_message(embed = embed, delete_after = 5)
            return

async def setup(client: commands.Bot) -> None:
    await client.add_cog(emoji(client))