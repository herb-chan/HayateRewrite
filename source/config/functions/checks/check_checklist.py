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
checklists = db['Checklists']

def check_checklist(interaction: discord.Interaction, user: discord.Member):
    user = interaction.user
    user_id = user.id
    
    # filters database to find just the right user
    user_filter = {'user_id': user_id}
    check = checklists.find_one(user_filter)

    if not check:
        user_checklists = {
            'user_id': user_id,
            'times_claimed': 1,
            'streak': 1,
            'last_claimed': None
        }
        checklists.insert_one(user_checklists)
        
        times_claimed = 1
        streak = 1
        last_claimed = None
    else:
        times_claimed = check.get('times_claimed')
        streak = check.get('streak')
        last_claimed = check.get('last_claimed')

    return times_claimed, streak, last_claimed