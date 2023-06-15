'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under MIT
 For more information, see README.md and LICENSE
'''

import logging

import discord
from config.load_env import bot_token, mongo
from discord.ext import commands

# Configure logging
logging.basicConfig(level = logging.INFO)
log = logging.getLogger(__name__)

# Define a subclass of the commands.AutoShardedBot class
class Hayate(commands.AutoShardedBot):
    def __init__(self):
        # Configuration
        allowed_mentions = discord.AllowedMentions(roles = False, everyone = False, users = True)
        intents = discord.Intents().all()
        activity = discord.Activity(type = discord.ActivityType.playing, name = f'sucking some smeggsy toes')
        
        super().__init__(
            command_prefix = commands.when_mentioned,
            pm_help = None, 
            activity = activity,
            heartbeat_timeout = 150.0,
            allowed_mentions = allowed_mentions,
            intents = intents
        )

        self.cogslist = [
            'extensions.economy.wallet',
            'extensions.economy.daily',
            'extensions.economy.give',
            'extensions.economy.checklist',
            'extensions.economy.lottery',
            
            'extensions.fun.flags',
            'extensions.fun.emoji',
            'extensions.fun.dice',
            'extensions.fun.ship',

            'extensions.info.github',
            'extensions.info.members', 
            'extensions.info.guild',

            'extensions.utility.ping',
            'extensions.utility.remindme',
            'extensions.utility.time',
            'extensions.utility.info',
            'extensions.utility.snipe',
            'extensions.utility.reload',

            'extensions.music.artist'
        ]

    # Define an asynchronous method to load the cogs
    async def setup_hook(self):
        for ext in self.cogslist:
            try:
                await self.load_extension(ext)
            except Exception as e:
                log.exception(f'Failed to load extension {ext}.')

# Configure logging format
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    # Create an instance of the Hayate class and run the bot using a token
    client = Hayate()

    try:
        mongo.admin.command('ping')
        log.info('Successfully connected to MongoDB!')
    except Exception as e:
        log.exception(f'Failed to connect to MongoDB: {e}')

    # Run the bot, and catch any exceptions that may be raised
    try:
        log.info(f'Logged in as Hayate')
        client.run(bot_token)
    except Exception as e:
        log.exception(f'Error: {e}')
