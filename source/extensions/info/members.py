'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from main import Hayate

class members(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
            name = 'avatar', 
            description = 'Returns requested user\'s avatar.'
            )
    @app_commands.describe(user = 'User which avatar you want to get.')
    @app_commands.guild_only()
    async def avatar(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        # sets 'user' variable to user that executed the command, or if chosed, user that was pinged
        user = user or interaction.user
        avatar = user.avatar

        avatar_embed = discord.Embed(
            color = 0x575fcf,
            timestamp = datetime.datetime.utcnow()
        )
        avatar_embed.set_author(
            name = f'{user.name}\'s Avatar', 
            icon_url = avatar,
            url = avatar.url
        )
        avatar_embed.set_image(
            url = avatar
        )
        avatar_embed.set_footer(
            text = f'Requested by {interaction.user.name}', 
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = avatar_embed)

    @app_commands.command(
            name = 'user', 
            description = 'Returns all important information about user.'
            )
    @app_commands.describe(
        user = 'User which info you want to get about.'
    )
    @app_commands.guild_only()
    async def user(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        # sets 'user' variable to user that executed the command, or if chosed, user that was pinged
        user = user or interaction.user
        avatar = user.avatar

        # checks if user has nickname, and if so, displays it in the place of username
        if user.nick is not None:
            username = user.nick
        else:
            username = user.name

        # list of all existing badges that you can get access to (and bot can read them)
        badges = {
            'Discord Partner': {'icon': '<:2166discordpartner:1098243539839762483>'},
            'HypeSquad Events': {'icon': '<:9472hypesquadeventsbadge:1098245618343882892>'},
            'Bug Hunter Level 1': {'icon': '<:1572discordbughunter:1098243533099499630>'},
            'Bug Hunter Level 2': {'icon': '<:9148discordgoldbughunter:1098243578335088782>'},
            'House Bravery': {'icon': '<:6601hypesquadbravery:1098243564691005462>'},
            'House Brilliance': {'icon': '<:6318iconhypesquadbrilliance:1098246051359641720>'},
            'House Balance': {'icon': '<:5242hypesquadbalance:1098243560383459378>'},
            'Early Supporter': {'icon': '<:6832badgeearlysupporter:1098246335188172840>'},
            'Verified Bot': {'icon': '<:9142discordverifiedbot1fromvega:1098253815943274586><:3099discordverifiedbot2fromvega:1098253813384745031>'},
            'Verified Bot Developer': {'icon': '<:7088earlyverifiedbotdeveloper:1098243570831474717>'},
            'Discord Staff': {'icon': '<:7871discordstaff:1098243574581166152>'},
            'Active Developer': {'icon': '<:7011activedeveloperbadge:1098243568964997253>'},
            'Nitro': {'icon': '<:4306subscribernitro:1098243555048308817>'}
        }

        # gets list of all badges user has and creates empty list to show them
        flags = user.public_flags
        user_badges = []

        # check if user has nitro status cause you can't do it normally we need to do it like cavemen
        nitro_check = user.avatar.url
        file_extension = nitro_check.split('.')[-1].split('?')[0]

        if flags.discord_certified_moderator == True:
            user_badges.append(badges['Discord Certified Moderator']['icon'])
        
        if flags.partner == True:
            user_badges.append(badges['Discord Partner']['icon'])
        
        if flags.hypesquad == True:
            user_badges.append(badges['HypeSquad Events']['icon'])
        
        if flags.bug_hunter == True:
            user_badges.append(badges['Bug Hunter Level 1']['icon'])
        
        if flags.bug_hunter_level_2 == True:
            user_badges.append(badges['Bug Hunter Level 2']['icon'])
        
        if flags.hypesquad_bravery == True:
            user_badges.append(badges['House Bravery']['icon'])
        
        if flags.hypesquad_brilliance == True:
            user_badges.append(badges['House Brilliance']['icon'])
        
        if flags.hypesquad_balance == True:
            user_badges.append(badges['House Balance']['icon'])
        
        if flags.early_supporter == True:
            user_badges.append(badges['Early Supporter']['icon'])
        
        if flags.verified_bot == True:
            user_badges.append(badges['Verified Bot']['icon'])
        
        if flags.verified_bot_developer == True:
            user_badges.append(badges['Verified Bot Developer']['icon'])
        
        if flags.staff == True:
            user_badges.append(badges['Discord Staff']['icon'])

        if file_extension == 'gif':
            user_badges.append(badges['Nitro']['icon'])

        # since list will be displayed like that ['badges'], get rid of the brackets
        user_badges = str(user_badges).replace('[', '').replace(']', '').replace("'", '').replace(",", '')

        info_embed = discord.Embed(
            color = 0x575fcf,
            timestamp = datetime.datetime.utcnow()
        )
        info_embed.set_author(
            name = f'{user.name}\'s Profile', 
            icon_url = avatar,
            url = avatar.url
        )
        info_embed.set_thumbnail(
            url = f'{user.avatar}'
        )
        info_embed.add_field(
            name = '<:customization:1117463839324241991> Display name',
            value = f'{username}', 
            inline = True
        )
        info_embed.add_field(
            name = '<:info:1118212340685475861> ID', 
            value = f'{user.id}', 
            inline = True
        )
        info_embed.add_field(
            name = '<:badge:1118215335473070090> Badges', 
            value = f'{user_badges}', 
            inline = True
        )
        info_embed.add_field(
            name = '<:calendar:1118212348755312642> Joined discord',
            value = f'{discord.utils.format_dt(user.created_at)}', 
            inline = True
        )
        info_embed.add_field(
            name = '<:calendar:1118212348755312642> Joined server', value=f'{discord.utils.format_dt(user.joined_at)}', 
            inline = True
        )
        info_embed.set_footer(
            text = f'Requested by {interaction.user.name}', 
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = info_embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(members(client))
