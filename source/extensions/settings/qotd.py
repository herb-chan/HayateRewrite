'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import asyncio
import datetime
from random import randint
from typing import Optional

import discord
from config.load_env import mongo
from discord import app_commands
from discord.ext import commands, tasks

# database collections
db = mongo['Guilds']
qotd_channel = db['QOTD_Channels']
qotd_questions = db['QOTD_Questions']

class qotd(commands.GroupCog, name = 'qotd'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name = 'send',
        description = 'Configure your own QOTD module.'
    )
    @app_commands.guild_only()
    async def send(self, interaction: discord.Interaction,):
        # filters all the questions so that current guild.id matches
        guild = interaction.guild
        guild_filter = {"guild_id": guild.id}
        user_avatar = interaction.user.avatar

        # finds all the questions that were added in the current guild
        matching_questions = qotd_questions.find(guild_filter)

        # get the count of questions with the matching guild.id
        num_questions = matching_questions.count()

        # if there are questions with the matching guild.id pick a random one
        if num_questions > 0:
            random_question = qotd_questions.aggregate([
                {"$match": guild_filter},
                {"$sample": {"size": 1}}
            ]).next()

            # check if the question field is None
            if random_question['question'] is None:
                no_questions = discord.Embed(
                    description = f'Unfortunately, there are no questions added for this guild.\nYou can always use `/qotd config add` command to add some!',
                    color = 0xffc048,
                    timestamp = datetime.datetime.utcnow()
                )
                no_questions.set_footer(
                    text = f'Requested by {interaction.user.name}', 
                    icon_url = user_avatar
                )

                await interaction.response.send_message(embed = no_questions)
            else:
                # creates new dictionary to help download a random question from the database
                mydict = {
                    'guild_id': guild.id,
                    'question': random_question['question']
                }

                # get qotd channel to send questions here and not on the current channel
                channel_filter = {"guild_id": guild.id}
                qotd_channel_id = qotd_channel.find_one(channel_filter)

                if qotd_channel_id is None:
                    no_channel_set = discord.Embed(
                        description = f'There is no QOTD channel set for this guild.\nYou can use `/qotd config channel` command to set one.',
                        color = 0xffc048,
                        timestamp = datetime.datetime.utcnow()
                    )
                    no_channel_set.set_footer(
                        text = f'Requested by {interaction.user.name}', 
                        icon_url = user_avatar
                    )

                    await interaction.response.send_message(embed = no_channel_set)
                else:
                    qotd_channel_id = qotd_channel_id['channel_id']
                    get_qotd_channel = await guild.fetch_channel(qotd_channel_id)
                    # deletes the question so that it won't occur 2nd time
                    x = qotd_questions.delete_one(mydict)
                        
                    question = random_question['question']
                        
                    qotd_embed = discord.Embed(
                        title = 'Question of the Day!',
                        description = f'{question}',
                        color = 0x575fcf,
                        timestamp = datetime.datetime.utcnow()
                    )
                    qotd_embed.set_footer(
                        text = f'Requested by {interaction.user.name}', 
                        icon_url = user_avatar
                    )

                    await get_qotd_channel.send(embed = qotd_embed)
                    await interaction.response.send_message(f'Question of the Day has been successfully sent to <#{get_qotd_channel.id}> channel!')

    @app_commands.command(
        name = 'config',
        description = 'Configure QOTD module for your guild.'
    )
    @app_commands.describe(
        channel = 'Select channel to which all the questions will be sent.',
        add = 'Provide question that you want to add to the question pool.',
        remove = 'Provide question id to remove it from database.',
    )
    @app_commands.guild_only()
    async def config(
            self,
            interaction: discord.Interaction,
            channel: Optional[discord.TextChannel] = None,
            add: Optional[str] = None,
            remove: Optional[int] = None,):
        
        user_avatar = interaction.user.avatar
        guild = interaction.guild
     
        if channel is not None and add is None and remove is None:
        # checks if there already is QOTD channel in this guild
            to_check = {
                'guild_id': guild.id
                }
            channel_check = qotd_channel.find_one(to_check)

            # if there already is QOTD channel makes a new dictionary to update the channel to a new one
            if channel_check is not None and channel_check['channel_id'] == channel.id:
                setqotd_embed_exists = discord.Embed(
                    description = f'<#{channel.id}> is already set as a Question of the Day channel. If you want to change it please provide different channel.',
                    color = 0xffc048,
                    timestamp = datetime.datetime.utcnow()
                )
                setqotd_embed_exists.set_footer(
                    text = f'Requested by {interaction.user.name}', 
                    icon_url = user_avatar
                )
                setqotd_embed_exists.set_footer(
                    text = f'Requested by {interaction.user.name}',
                    icon_url = user_avatar
                )
                response = None

                await interaction.response.send_message(embed = setqotd_embed_exists)
            
            elif channel_check is not None:
                update = {
                    '$set': {
                    'channel_id': channel.id
                    }
                }
                
                previous = channel_check['channel_id']
                
                # updates current QOTD channel to a new one
                x = qotd_channel.update_one(to_check, update)

                # get qotd channel to send questions here and not on the current channel
                guild_filter = {"guild_id": guild.id}
                new_qotd_channel = qotd_channel.find_one(guild_filter)['channel_id']

                response = f'Successfully changed the Question of the Day channel from <#{previous}> to <#{new_qotd_channel}>.'
            
            else:    
                # creates dictionary to create new record in the database storing the channel
                mydict = {
                    'guild_id': guild.id,
                    'channel_id': channel.id
                        }
                # creates new record in the database
                x = qotd_channel.insert_one(mydict)

                # get qotd channel to send questions here and not on the current channel
                guild_filter = {"guild_id": guild.id}
                new_qotd_channel = qotd_channel.find_one(guild_filter)['channel_id']

                response = f'Successfully set the Question of the Day channel as <#{new_qotd_channel}>.\n\n You can now add question to the Question of the Day question pool by using `/qotd config add` command.'

            if response is not None:
                setqotd_embed = discord.Embed(
                    description = f'{response}',
                    color = 0x575fcf,
                    timestamp = datetime.datetime.utcnow()
                )
                setqotd_embed.set_footer(
                    text = f'Requested by {interaction.user.name}', 
                    icon_url = user_avatar
                )
                setqotd_embed.set_footer(
                    text = f'Requested by {interaction.user.name}',
                    icon_url = user_avatar
                )

                await interaction.response.send_message(embed = setqotd_embed)
        
        elif add is not None and channel is None and remove is None:
            question = add  # Define the question variable

            # filters all the questions so that current guild.id matches
            guild_filter = {'guild_id': guild.id}

            # finds all the questions that were added in the current guild
            matching_questions = qotd_questions.find(guild_filter)

            # get the count of questions with the matching guild.id
            how_many = matching_questions.count() + 1

            custom_id = randint(700000, 800000) + (randint(1000, 9999))

            # creates a dictionary to create a new record in the database storing the question
            mydict = {
                'id': custom_id,
                'guild_id': guild.id,
                'question': question
            }
            # inserts the new record into the database
            x = qotd_questions.insert_one(mydict)

            question = question.strip()
            question = question.replace('`', ' ')

            addqotd_embed = discord.Embed(
                title = 'Question Added',
                description = f'**Added question:** \n ```{question}``` \nYou can now use the `/qotd send` command as you have {how_many} questions in the pool.',
                color = 0x575fcf,
                timestamp = datetime.datetime.utcnow()
            )
            addqotd_embed.set_footer(
                text = f'Requested by {interaction.user.name}',
                icon_url = user_avatar
            )

            await interaction.response.send_message(embed = addqotd_embed)

        elif remove is not None and channel is None and add is None:
            # filters all the questions so that current guild.id matches
            guild_filter = {
                'id': remove,
                'guild_id': guild.id
            }

            # finds all the questions that were added in the current guild
            matching_questions = qotd_questions.find(guild_filter)

            if matching_questions.count() == 0:
                title = 'Invalid ID'
                description = f'Make sure that the ID `{remove}` you just provided is assigned to a question in the database.'
            else:
                for question in matching_questions:
                    question_id = question['id']
                    question = question['question']

                    title = 'Question Removed'
                    description = f'**Question:**\n```{question}```\n**ID:**\n```{question_id}```'

                x = qotd_questions.delete_one(guild_filter)

            removed = discord.Embed(
                title = title,
                description = description,
                color = 0xff5e57,
                timestamp = datetime.datetime.utcnow()
            )
            removed.set_footer(
                text=f'Requested by {interaction.user.name}',
                icon_url=user_avatar
            )

            await interaction.response.send_message(embed=removed)

        else:
            too_many = discord.Embed(
                    description = f'Unfortunately, you can\'t set up multiple things all at once. Try setting them up one at a time.',
                    color = 0xff5e57,
                    timestamp = datetime.datetime.utcnow()
                )
            too_many.set_footer(
                    text = f'Requested by {interaction.user.name}', 
                    icon_url = user_avatar
                )

            await interaction.response.send_message(embed = too_many)

    @app_commands.command(
        name = 'list',
        description = 'Returns a complete list of qotd questions saved in the database.'
    )
    @app_commands.guild_only()
    async def list(self, interaction: discord.Interaction,):
        user_avatar = interaction.user.avatar
        guild = interaction.guild
        # filters all the questions so that current guild.id matches
        guild_filter = {"guild_id": guild.id}

        # finds all the questions that were added in the current guild
        matching_questions = qotd_questions.find(guild_filter)

        question_list = discord.Embed(
            title = 'QOTD List',
            color = 0x575fcf,
            timestamp = datetime.datetime.utcnow()
        )
        question_list.set_footer(
            text = f'Requested by {interaction.user.name}',
            icon_url = user_avatar
        )
            
        for question in matching_questions:
            question_id = question['id']
            question = question['question']
                    
            question_list.add_field(
                name = ' ',
                value = f'**Question:** {question}\n**ID:** {question_id}',
                inline = True
            )

        if len(question_list.fields) == 0:
            question_list.description = 'You haven\'t added any questions yet. To do so you can use `/qotd config add` command.'
            question_list.color = 0xff5e57
        else:
            question_list.description = f'**You have** `{len(question_list.fields)}/25` **questions!**'
                
        await interaction.response.send_message(embed = question_list)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(qotd(client))