'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

from config.load_env import mongo
import discord

# database collection
db = mongo['Users']
money = db['Wallets']

def check_wallet(interaction: discord.Interaction, user: discord.Member):
    user = user or interaction.user
    user_id = user.id
    
    # filters database to find just the right user
    user_filter = {'user_id': user_id}
    check = money.find_one(user_filter)

    if not check:
        user_wallet = {
            'user_id': user_id,
            'balance': 0,
        }
        money.insert_one(user_wallet)
        balance = 0
    else:
        balance = check.get('balance', 0)

    return balance