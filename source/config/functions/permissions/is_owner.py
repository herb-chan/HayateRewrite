'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import discord
from discord import app_commands

def is_owner():
    def predicate(interaction: discord.Interaction):
        if interaction.user.id == 511889215672287242:
            return True
    return app_commands.check(predicate)