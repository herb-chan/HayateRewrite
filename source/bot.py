'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under MIT
 For more information, see README.md and LICENSE
'''

import platform
import time

import discord
from colorama import Back, Fore, Style
from config.load_env import bot_token, mongo
from discord.ext import commands

# Define a subclass of the commands.Bot class
class Client(commands.Bot):
    def __init__(self):
        # Call the superclass constructor and set command prefix and intents
        intents = discord.Intents().all()
        activity = discord.Activity(type = discord.ActivityType.playing, name = f'test')
        
        super().__init__(command_prefix = commands.when_mentioned, intents = intents, activity = activity)

        # Create a list of cogs that the bot will load when it starts up
        self.cogslist = [
            'extensions.economy.wallet',
            'extensions.economy.daily',
            'extensions.economy.give',
            'extensions.economy.checklist',
            
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

            'extensions.music.artist',

            'extensions.settings.qotd',
            'extensions.settings.moderator',
            ]

    # Define an asynchronous method to load the cogs
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

    # Define an asynchronous method that is called when the bot is logged in and ready to start accepting commands
    async def on_ready(self):
        # Set console text color
        prfx = (Back.BLACK + Fore.GREEN + Style.BRIGHT + time.strftime("%H:%M:%S", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)

        # Print information about the bot
        print(f'\n{prfx} Logged in as {Fore.YELLOW}{self.user.name}')
        print(f'{prfx} Discord.py version: {Fore.YELLOW}{discord.__version__}')
        print(f'{prfx} Python version: {Fore.YELLOW}{platform.python_version()}')

        try:
            prfx = (Back.BLACK + Fore.GREEN + Style.BRIGHT + time.strftime("%H:%M:%S", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
            mongo.admin.command('ping')
            print(f'{prfx} Successfully connected to {Fore.YELLOW}MongoDB!\n{Style.RESET_ALL}')
        
        except Exception as e:
            prfx = (Back.BLACK + Fore.GREEN + Style.BRIGHT + time.strftime("%H:%M:%S", time.localtime()))
            err = (Fore.RED + Style.BRIGHT)
            res = (Style.RESET_ALL)

            print(f'{prfx} {err}Error: {str(e).capitalize()}{res}')


# Create an instance of the Client class and run the bot using a token
client = Client()

# Run the bot, and catch any exceptions that may be raised
try:
    client.run(bot_token)

except Exception as e:
    prfx = (Back.BLACK + Fore.GREEN + Style.BRIGHT + time.strftime("%H:%M:%S", time.localtime()))
    err = (Fore.RED + Style.BRIGHT)
    res = (Style.RESET_ALL)

    print(f'{prfx} {err}Error: {str(e).capitalize()}{res}')
