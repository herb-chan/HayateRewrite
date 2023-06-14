'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import discord
from config.load_env import mongo

# database collection
db = mongo['Users']
daily = db['Dailies']

def check_daily(interaction: discord.Interaction, user: discord.Member):
    user = interaction.user
    user_id = user.id
    
    # filters database to find just the right user
    user_filter = {'user_id': user_id}
    check = daily.find_one(user_filter)

    if not check:
        user_dailies = {
            'user_id': user_id,
            'streak': 1,
            'last_claimed': None
        }
        daily.insert_one(user_dailies)
        
        streak = 1
        last_claimed = None
    else:
        streak = check.get('streak', 0)
        last_claimed = check.get('last_claimed')

    return streak, last_claimed