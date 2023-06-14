'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
import locale
from config.functions.checks.check_wallet import check_wallet

import discord
from config.load_env import mongo
from discord import app_commands
from discord.ext import commands

# locale formatting
locale.setlocale(locale.LC_ALL, 'en_US') 

# database collection
db = mongo['Users']
money = db['Wallets']

class give(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'give',
        description = 'Give your friends some of your cash!'
    )
    @app_commands.describe(
        amount = 'Amount of cash you want to give.',
        user = 'Whom you want to give the cash.'
    )
    @app_commands.guild_only()
    async def give(self, interaction: discord.Interaction, amount: int, user: discord.Member):
        giver = interaction.user
        user = user
        
        # Get current balance of the specified user and the giver
        balance_user = check_wallet(interaction = interaction, user = user)
        balance_giver = check_wallet(interaction = interaction, user = giver)

        if balance_giver < amount:
            balance = locale.format_string('%d', balance_giver, grouping = True)
            
            embed = discord.Embed(
                title = f'Transaction Failed',
                description = f'You have only 💷 `{balance} cash`, you can\'t give someone more than you already have!',
                color = 0xff5e57,
                timestamp = datetime.datetime.now()
            )
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )

            await interaction.response.send_message(embed = embed)
            return

        # Filter the database to get the user
        user_filter = {'user_id': user.id}
        giver_filter = {'user_id': giver.id}

        # Update the user's wallet and last claimed time
        money.update_one(user_filter,
                        {'$set': {
                            'balance': balance_user + amount,
                        }
                        })
            
        # Update the giver's wallet and last claimed time
        money.update_one(giver_filter,
                        {'$set': {
                            'balance': balance_giver - amount,
                        }
                        })

        amount = locale.format_string('%d', amount, grouping = True)

        embed = discord.Embed(
            title = f'Transaction Successful',
            description = f'💷 `+{amount} cash` <@{user.id}>\n💷 `-{amount} cash` <@{giver.id}>',
            color = 0x575fcf,
            timestamp = datetime.datetime.now()  
        )
        embed.set_footer(
            text = f'Requested by {interaction.user.name}',
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(give(client))