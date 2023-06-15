'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import datetime
import locale

import discord
from config.functions.checks.check_daily import check_daily
from config.functions.checks.check_wallet import check_wallet
from config.load_env import mongo
from discord import app_commands
from discord.ext import commands
from discord.utils import format_dt
from main import Hayate

# locale formatting
locale.setlocale(locale.LC_ALL, 'en_US')

# database collection
db = mongo['Users']
money = db['Wallets']
daily = db['Dailies']

class Daily(commands.Cog):
    def __init__(self, client: Hayate):
        self.client: Hayate = client

    @app_commands.command(
    name='daily',
    description='Claim your daily reward.'
    )
    @app_commands.guild_only()
    async def daily(self, interaction: discord.Interaction):
        user = interaction.user
        user_id = user.id

        # Get the current date and time
        now = datetime.datetime.now()

        # Get the balance, streaks and date of last claimed daily
        balance = check_wallet(interaction = interaction, user = user)
        streak, last_claimed = check_daily(interaction = interaction, user = user)

        # Check if the last claim was made on the same day
        if last_claimed and last_claimed.date() == now.date():
            # Daily reward already claimed for the day
            next_day = now.date() + datetime.timedelta(days=1)
            next_daily_time = datetime.datetime.combine(next_day, datetime.time.min)
            
            embed = discord.Embed(
                title = 'Daily Reward',
                description = f'You have already claimed your daily reward for today. Please try again at {format_dt(next_daily_time, style="t")}.',
                color = 0xff5e57,
                timestamp = now
            )
            embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = interaction.user.avatar
            )

            await interaction.response.send_message(embed = embed)
            return

        # Calculate the streak and reward
        if last_claimed and last_claimed.date() == now.date() - datetime.timedelta(days=1):
            # Claimed consecutively
            streak += 1
        else:
            # Reset the streak
            streak = 1

        daily_reward = 100 * streak

        # Filter the database to get the user
        user_filter = {'user_id': user_id}

        # Update the user's wallet and last claimed time
        money.update_one(user_filter,
                        {'$set': {
                            'balance': balance + daily_reward,
                        }
                        })

        daily.update_one(user_filter,
                        {'$set': {
                            'streak': streak,
                            'last_claimed': now
                        }
                        })

        daily_reward = locale.format_string('%d', daily_reward, grouping = True)

        embed = discord.Embed(
            title = 'Claimed Daily!',
            description = f'💷 `+{daily_reward} cash`\n<:streak:1117463831522836582> `{streak} day(s) streak`',
            color = 0x575fcf,
            timestamp = now
        )
        embed.set_footer(
            text = f'Requested by {interaction.user.name}',
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Daily(client))