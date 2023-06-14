'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime

import discord
import requests
from discord import app_commands
from discord.ext import commands

class github(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'github',
        description = 'Displays information about github user and his repositories.'
    )
    @app_commands.describe(
        username = 'User which github profile you want to display.'
    )
    @app_commands.guild_only()
    async def github(self, interaction: discord.Interaction, username: str):
        # Make API request to fetch GitHub user's information
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant information from the response
            followers = data["followers"]
            following = data["following"]
            public_repos = data["public_repos"]
            
            # Make API request to fetch user's most starred repositories
            starred_repos_response = requests.get(f"https://api.github.com/users/{username}/starred")
            if starred_repos_response.status_code == 200:
                starred_repos = starred_repos_response.json()
                
                # Sort the repositories by the number of stars
                starred_repos.sort(key=lambda x: x["stargazers_count"], reverse=True)
                
                # Get the top 3 repositories
                top_starred_repos = starred_repos[:3]
                repo_info = ""
                for repo in top_starred_repos:
                    repo_name = repo["name"]
                    stargazers_count = repo["stargazers_count"]
                    repo_info += f"\n<:link:1118212338022088704> **[{repo_name}](https://github.com/{username}/{repo_name})**: {stargazers_count} stars"
                
                # Send the user's GitHub profile information and top starred repositories to the Discord channel
                embed = discord.Embed(
                    color = 0x575fcf,
                    timestamp = datetime.datetime.now()
                )
                embed.set_author(
                    name = f'{username}\'s Github Profile',
                    icon_url = f'https://avatars.githubusercontent.com/{username}',
                    url = f'https://github.com/{username}'
                )
                embed.add_field(
                    name = f'<:followers:1118256333838364712> Followers',
                    value = followers,
                    inline = True
                )
                embed.add_field(
                    name = f'<:followers:1118256333838364712> Following',
                    value = following,
                    inline = True
                )
                embed.add_field(
                    name = f'<:world:1118256855894995046> Public repositories',
                    value = public_repos,
                    inline = True
                )
                embed.add_field(
                    name = f'<:star:1118256900996341791> Top 3 starred repositories',
                    value = repo_info,
                    inline = False
                )
                embed.set_thumbnail(
                    url = f'https://avatars.githubusercontent.com/{username}'
                )
                embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
                )

                await interaction.response.send_message(embed = embed)

            else:
                embed = discord.Embed(
                    title = 'Something went wrong...',
                    description = f'Failed to fetch starred repositories for {username}.',
                    color = 0xff5e57,
                    timestamp = datetime.datetime.now()
                )

                await interaction.response.send_message(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Something went wrong...',
                description = f'GitHub user {username} not found.',
                color = 0xff5e57,
                timestamp = datetime.datetime.now()
            )

            await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(github(client))