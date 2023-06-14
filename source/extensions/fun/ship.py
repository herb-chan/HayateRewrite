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

class ship(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'ship',
        description = 'Creates a ship name for two lovers.'
    )
    @app_commands.describe(
        user = 'Your lover that you want to create ship name with.'
    )
    @app_commands.guild_only()
    async def dice(self, interaction: discord.Interaction, user: discord.Member):
        lover = interaction.user
        crush = user

        half_lover = len(lover.display_name)//2
        half_crush = len(crush.display_name)//2

        ship = f'{lover.display_name[:half_lover]}{crush.display_name[half_crush:]}'

        embed = discord.Embed(
            title = ':revolving_hearts: Aww how adorable!',
            description = f'You two look cute together **{lover.display_name}** and **{crush.display_name}**! Your relationship name should be **{ship}**! ',
            color = 0x575fcf,
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ship(client))