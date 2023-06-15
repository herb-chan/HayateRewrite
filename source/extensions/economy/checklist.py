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
from config.functions.checks.check_checklist import check_checklist
from config.load_env import mongo
from discord import app_commands
from discord.ext import commands
from main import Hayate

# locale formatting
locale.setlocale(locale.LC_ALL, 'en_US')

# database collection
db = mongo['Users']
money = db['Wallets']
daily = db['Dailies']
checklists = db['Checklists']

class checklist(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'checklist',
        description = 'Complete daily challenges to claim rewards!'
    )
    @app_commands.guild_only()
    async def checklist(self, interaction: discord.Interaction):
        user = interaction.user
        user_id = user.id

        # Get the current date and time
        now = datetime.datetime.now()

        # Get the date of the last claimed daily
        _, daily_last_claimed = check_daily(interaction = interaction, user = user)

        # Check if the last claim was made on the same day
        if daily_last_claimed and daily_last_claimed.date() == now.date():
            # Daily reward already claimed for the day
            daily = '<:daily_claimed:1117459690142576752>・You have claimed your daily!'
            daily_check = True
        else:
            # Daily reward isn't claimed for the day yet
            daily = '<:daily_unclaimed:1117459692684320878>・You haven\'t claimed your daily yet.'
            daily_check = False

        # Check if all the daily challenges were completed
        if daily_check == True:
            # Daily challenges already completed

            # Get the data about last users checklists
            check_times_claimed, check_streak, check_last_claimed = check_checklist(interaction = interaction, user = user)

            if check_last_claimed and check_last_claimed.date() == now.date():
                # Checklist reward already claimed for this day
                checklist = '<:congratulations:1117466048988450968>・You have already claimed your rewards!'
                checklist_followup = False
                pass
            else:
                # Checklist reward not claimed for this day yet
                
                # Calculate the streak
                if check_last_claimed and check_last_claimed.date() == now.date() - datetime.timedelta(days=1):
                    # Claimed consecutively
                    check_streak += 1
                else:
                    # Reset the streak
                    check_streak = 1

                # Increase the statistic of claimed checklists
                if check_times_claimed == 1:
                    pass
                else:
                    check_times_claimed += 1

                # Get users ballance and increase it by 1000 as a reward for completing the checklist
                balance = check_wallet(interaction = interaction, user = user)

                # Filter the database to get the user
                user_filter = {'user_id': user_id}
                
                # Update the user's wallet and last claimed time
                money.update_one(user_filter,
                                {'$set': {
                                    'balance': balance + 1000,
                                }
                                })
                
                checklists.update_one(user_filter,
                        {'$set': {
                            'times_claimed': check_times_claimed,
                            'streak': check_streak,
                            'last_claimed': now
                        }
                        })
                
                checklist = '<:congratulations:1117466048988450968>・You have completed your checklist!'
                checklist_followup = True
        else:
            # Daily challenges not completed yet
            checklist = '<:challenge:1117463843170439188>・Complete your checklist to get a reward!'

        embed = discord.Embed(
            title = f'{user.display_name}\'s Checklist',
            description = f'{daily}\n{checklist}',
            color = 0x575fcf,
            timestamp = now
        )
        embed.set_footer(
            text = f'Requested by {interaction.user.name}',
            icon_url = interaction.user.avatar
        )

        await interaction.response.send_message(embed = embed)

        if checklist_followup == True:
            embed = discord.Embed(
                title = f'{user.display_name}\'s Reward',
                description = f'Congratulations on completing all the daily challenges here\'s your reward:\n💷 `+1000 cash`!',
                color = 0x575fcf
            )
            embed.set_footer(
                text = f'Checklists reset at 00:00'
            )

            await interaction.followup.send(embed = embed, ephemeral = True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(checklist(client))