'''
 Hayate Bot for Discord
 Copyright (C) 2023 herbuś
 This software is licensed under CC BY-NC-SA 4.0
 For more information, see README.md and LICENSE
'''

import asyncio
import datetime
from random import choice

import discord
from config.load_env import mongo

# database collections
db = mongo['Flags']
europe = db['European']
asia = db['Asian']
africa = db['African']
america = db['American']

european_flags = [
    {'name': 'Albania', 'flag': 'https://i.imgur.com/4rFjag8.png'},
    {'name': 'Andorra', 'flag': 'https://i.imgur.com/CzuLTCO.png'},
    {'name': 'Austria','flag': 'https://i.imgur.com/SN4v5gP.png'},
    {'name': 'Belarus','flag': 'https://i.imgur.com/aW10HBN.png'},
    {'name': 'Belgium','flag': 'https://i.imgur.com/Ks3gguF.png'},
    {'name': 'Bosnia and Herzegovina','flag': 'https://i.imgur.com/Yl8zdJ1.png'},
    {'name': 'Bulgaria','flag': 'https://i.imgur.com/A2WxDqI.png'},
    {'name': 'Croatia','flag': 'https://i.imgur.com/Hqxff7J.png'},
    {'name': 'Cyprus','flag': 'https://i.imgur.com/k2aY9DL.png'},
    {'name': 'Czechia','flag': 'https://imgur.com/P3NftvD.png'},
    {'name': 'Denmark','flag': 'https://i.imgur.com/21CXfon.png'},
    {'name': 'Estonia','flag': 'https://i.imgur.com/xGOgdQv.png'},
    {'name': 'Finland','flag': 'https://i.imgur.com/VgoEQZe.png'},
    {'name': 'France','flag': 'https://i.imgur.com/zMQlAWD.png'},
    {'name': 'Germany','flag': 'https://i.imgur.com/2pyWF5D.png'},
    {'name': 'Greece','flag': 'https://i.imgur.com/0RTWYNz.png'},
    {'name': 'Hungary','flag': 'https://i.imgur.com/Q54JKwl.png'},
    {'name': 'Iceland','flag': 'https://i.imgur.com/poyQRLL.png'},
    {'name': 'Ireland','flag': 'https://i.imgur.com/Zlced2D.png'},
    {'name': 'Italy','flag': 'https://i.imgur.com/9aJ0ZsD.png'},
    {'name': 'Kosovo','flag': 'https://i.imgur.com/ycakCHJ.png'},
    {'name': 'Latvia','flag': 'https://i.imgur.com/X0qkqCW.png'},
    {'name': 'Liechtenstein','flag': 'https://i.imgur.com/Yaq30qp.png'},
    {'name': 'Lithuania','flag': 'https://i.imgur.com/b0rBVpw.png'},
    {'name': 'Luxembourg','flag': 'https://i.imgur.com/D2K8olB.png'},
    {'name': 'Malta','flag': 'https://i.imgur.com/QpuNqtK.png'},
    {'name': 'Moldova','flag': 'https://i.imgur.com/atkxdmi.png'},
    {'name': 'Monaco','flag': 'https://i.imgur.com/LMJOLf5.png'},
    {'name': 'Montenegro','flag': 'https://i.imgur.com/PLVJj5F.png'},
    {'name': 'Netherlands','flag': 'https://i.imgur.com/mI3vd1N.png'},
    {'name': 'North Macedonia','flag': 'https://i.imgur.com/BYzanP8.png'},
    {'name': 'Norway','flag': 'https://i.imgur.com/bIpQ6jH.png'},
    {'name': 'Poland','flag': 'https://i.imgur.com/NUmGRbe.png'},
    {'name': 'Portugal','flag': 'https://i.imgur.com/LxJtbS6.png'},
    {'name': 'Romania','flag': 'https://i.imgur.com/hRkwKNZ.png'},
    {'name': 'Russia','flag': 'https://i.imgur.com/aVlH3hK.png'},
    {'name': 'San Marino','flag': 'https://i.imgur.com/Rc7CHVy.png'},
    {'name': 'Serbia','flag': 'https://i.imgur.com/I5LuiVg.png'},
    {'name': 'Slovakia','flag': 'https://i.imgur.com/ybywkCR.png'},
    {'name': 'Slovenia','flag': 'https://i.imgur.com/Yo1vpa6.png'},
    {'name': 'Spain','flag': 'https://i.imgur.com/njWuDen.png'},
    {'name': 'Sweden','flag': 'https://i.imgur.com/KAAYU6j.png'},
    {'name': 'Switzerland','flag': 'https://i.imgur.com/TIMFnHb.png'},
    {'name': 'Ukraine','flag': 'https://i.imgur.com/kuWwWAE.png'},
    {'name': 'United Kingdom','flag': 'https://i.imgur.com/6iezndZ.png'},
    {'name': 'Vatican City','flag': 'https://i.imgur.com/Usq22RH.png'}
]

asian_flags = [
    {'name': 'Afghanistan', 'flag': 'https://flagcdn.com/w2560/af.png'},
    {'name': 'Armenia', 'flag': 'https://flagcdn.com/w2560/am.png'},
    {'name': 'Azerbaijan', 'flag': 'https://flagcdn.com/w2560/az.png'},
    {'name': 'Bahrain', 'flag': 'https://flagcdn.com/w2560/bh.png'},
    {'name': 'Bangladesh', 'flag': 'https://flagcdn.com/w2560/bd.png'},
    {'name': 'Bhutan', 'flag': 'https://flagcdn.com/w2560/bt.png'},
    {'name': 'Brunei', 'flag': 'https://flagcdn.com/w2560/bn.png'},
    {'name': 'Cambodia', 'flag': 'https://flagcdn.com/w2560/kh.png'},
    {'name': 'China', 'flag': 'https://flagcdn.com/w2560/cn.png'},
    {'name': 'Cyprus', 'flag': 'https://flagcdn.com/w2560/cy.png'},
    {'name': 'Georgia', 'flag': 'https://flagcdn.com/w2560/ge.png'},
    {'name': 'India', 'flag': 'https://flagcdn.com/w2560/in.png'},
    {'name': 'Indonesia', 'flag': 'https://flagcdn.com/w2560/id.png'},
    {'name': 'Iran', 'flag': 'https://flagcdn.com/w2560/ir.png'},
    {'name': 'Iraq', 'flag': 'https://flagcdn.com/w2560/iq.png'},
    {'name': 'Israel', 'flag': 'https://flagcdn.com/w2560/il.png'},
    {'name': 'Japan', 'flag': 'https://flagcdn.com/w2560/jp.png'},
    {'name': 'Jordan', 'flag': 'https://flagcdn.com/w2560/jo.png'},
    {'name': 'Kazakhstan', 'flag': 'https://flagcdn.com/w2560/kz.png'},
    {'name': 'Kuwait', 'flag': 'https://flagcdn.com/w2560/kw.png'},
    {'name': 'Kyrgyzstan', 'flag': 'https://flagcdn.com/w2560/kg.png'},
    {'name': 'Laos', 'flag': 'https://flagcdn.com/w2560/la.png'},
    {'name': 'Lebanon', 'flag': 'https://flagcdn.com/w2560/lb.png'},
    {'name': 'Malaysia', 'flag': 'https://flagcdn.com/w2560/my.png'},
    {'name': 'Maldives', 'flag': 'https://flagcdn.com/w2560/mv.png'},
    {'name': 'Mongolia', 'flag': 'https://flagcdn.com/w2560/mn.png'},
    {'name': 'Myanmar', 'flag': 'https://flagcdn.com/w2560/mm.png'},
    {'name': 'Nepal', 'flag': 'https://flagcdn.com/w2560/np.png'},
    {'name': 'North Korea', 'flag': 'https://flagcdn.com/w2560/kp.png'},
    {'name': 'Oman', 'flag': 'https://flagcdn.com/w2560/om.png'},
    {'name': 'Pakistan', 'flag': 'https://flagcdn.com/w2560/pk.png'},
    {'name': 'Palestine', 'flag': 'https://flagcdn.com/w2560/ps.png'},
    {'name': 'Philippines', 'flag': 'https://flagcdn.com/w2560/ph.png'},
    {'name': 'Qatar', 'flag': 'https://flagcdn.com/w2560/qa.png'},
    {'name': 'Russia', 'flag': 'https://flagcdn.com/w2560/ru.png'},
    {'name': 'Saudi Arabia', 'flag': 'https://flagcdn.com/w2560/sa.png'},
    {'name': 'Singapore', 'flag': 'https://flagcdn.com/w2560/sg.png'},
    {'name': 'South Korea', 'flag': 'https://flagcdn.com/w2560/kr.png'},
    {'name': 'Sri Lanka', 'flag': 'https://flagcdn.com/w2560/lk.png'},
    {'name': 'Syria', 'flag': 'https://flagcdn.com/w2560/sy.png'},
    {'name': 'Taiwan', 'flag': 'https://flagcdn.com/w2560/tw.png'},
    {'name': 'Tajikistan', 'flag': 'https://flagcdn.com/w2560/tj.png'},
    {'name': 'Thailand', 'flag': 'https://flagcdn.com/w2560/th.png'},
    {'name': 'Timor-Leste', 'flag': 'https://flagcdn.com/w2560/tl.png'},
    {'name': 'Turkey', 'flag': 'https://flagcdn.com/w2560/tr.png'},
    {'name': 'Turkmenistan', 'flag': 'https://flagcdn.com/w2560/tm.png'},
    {'name': 'United Arab Emirates', 'flag': 'https://flagcdn.com/w2560/ae.png'},
    {'name': 'Uzbekistan', 'flag': 'https://flagcdn.com/w2560/uz.png'}
]

african_flags = [
    {'name': 'Algeria', 'flag': 'https://flagcdn.com/w2560/dz.png'},
    {'name': 'Angola', 'flag': 'https://flagcdn.com/w2560/ao.png'},
    {'name': 'Benin', 'flag': 'https://flagcdn.com/w2560/bj.png'},
    {'name': 'Botswana', 'flag': 'https://flagcdn.com/w2560/bw.png'},
    {'name': 'Burkina Faso', 'flag': 'https://flagcdn.com/w2560/bf.png'},
    {'name': 'Burundi', 'flag': 'https://flagcdn.com/w2560/bi.png'},
    {'name': 'Cabo Verde', 'flag': 'https://flagcdn.com/w2560/cv.png'},
    {'name': 'Cameroon', 'flag': 'https://flagcdn.com/w2560/cm.png'},
    {'name': 'Central African Republic', 'flag': 'https://flagcdn.com/w2560/cf.png'},
    {'name': 'Chad', 'flag': 'https://flagcdn.com/w2560/td.png'},
    {'name': 'Comoros', 'flag': 'https://flagcdn.com/w2560/km.png'},
    {'name': 'Congo', 'flag': 'https://flagcdn.com/w2560/cd.png'},
    {'name': 'Congo', 'flag': 'https://flagcdn.com/w2560/cg.png'},
    {'name': 'Cote d\'Ivoire', 'flag': 'https://flagcdn.com/w2560/ci.png'},
    {'name': 'Djibouti', 'flag': 'https://flagcdn.com/w2560/dj.png'},
    {'name': 'Egypt', 'flag': 'https://flagcdn.com/w2560/eg.png'},
    {'name': 'Equatorial Guinea', 'flag': 'https://flagcdn.com/w2560/gq.png'},
    {'name': 'Eritrea', 'flag': 'https://flagcdn.com/w2560/er.png'},
    {'name': 'Eswatini', 'flag': 'https://flagcdn.com/w2560/sz.png'},
    {'name': 'Ethiopia', 'flag': 'https://flagcdn.com/w2560/et.png'},
    {'name': 'Gabon', 'flag': 'https://flagcdn.com/w2560/ga.png'},
    {'name': 'Gambia', 'flag': 'https://flagcdn.com/w2560/gm.png'},
    {'name': 'Ghana', 'flag': 'https://flagcdn.com/w2560/gh.png'},
    {'name': 'Guinea', 'flag': 'https://flagcdn.com/w2560/gn.png'},
    {'name': 'Guinea-Bissau', 'flag': 'https://flagcdn.com/w2560/gw.png'},
    {'name': 'Kenya', 'flag': 'https://flagcdn.com/w2560/ke.png'},
    {'name': 'Lesotho', 'flag': 'https://flagcdn.com/w2560/ls.png'},
    {'name': 'Liberia', 'flag': 'https://flagcdn.com/w2560/lr.png'},
    {'name': 'Libya', 'flag': 'https://flagcdn.com/w2560/ly.png'},
    {'name': 'Madagascar', 'flag': 'https://flagcdn.com/w2560/mg.png'},
    {'name': 'Malawi', 'flag': 'https://flagcdn.com/w2560/mw.png'},
    {'name': 'Mali', 'flag': 'https://flagcdn.com/w2560/ml.png'},
    {'name': 'Mauritania', 'flag': 'https://flagcdn.com/w2560/mr.png'},
    {'name': 'Mauritius', 'flag': 'https://flagcdn.com/w2560/mu.png'},
    {'name': 'Morocco', 'flag': 'https://flagcdn.com/w2560/ma.png'},
    {'name': 'Mozambique', 'flag': 'https://flagcdn.com/w2560/mz.png'},
    {'name': 'Namibia', 'flag': 'https://flagcdn.com/w2560/na.png'},
    {'name': 'Niger', 'flag': 'https://flagcdn.com/w2560/ne.png'},
    {'name': 'Nigeria', 'flag': 'https://flagcdn.com/w2560/ng.png'},
    {'name': 'Rwanda', 'flag': 'https://flagcdn.com/w2560/rw.png'},
    {'name': 'Sao Tome and Principe', 'flag': 'https://flagcdn.com/w2560/st.png'},
    {'name': 'Senegal', 'flag': 'https://flagcdn.com/w2560/sn.png'},
    {'name': 'Seychelles', 'flag': 'https://flagcdn.com/w2560/sc.png'},
    {'name': 'Sierra Leone', 'flag': 'https://flagcdn.com/w2560/sl.png'},
    {'name': 'Somalia', 'flag': 'https://flagcdn.com/w2560/so.png'},
    {'name': 'South Africa', 'flag': 'https://flagcdn.com/w2560/za.png'},
    {'name': 'South Sudan', 'flag': 'https://flagcdn.com/w2560/ss.png'},
    {'name': 'Sudan', 'flag': 'https://flagcdn.com/w2560/sd.png'},
    {'name': 'Tanzania', 'flag': 'https://flagcdn.com/w2560/tz.png'},
    {'name': 'Togo', 'flag': 'https://flagcdn.com/w2560/tg.png'},
    {'name': 'Tunisia', 'flag': 'https://flagcdn.com/w2560/tn.png'},
    {'name': 'Uganda', 'flag': 'https://flagcdn.com/w2560/ug.png'},
    {'name': 'Zambia', 'flag': 'https://flagcdn.com/w2560/zm.png'},
    {'name': 'Zimbabwe', 'flag': 'https://flagcdn.com/w2560/zw.png'}
]

american_flags = [
    {'name': 'Canada', 'flag': 'https://flagcdn.com/w2560/ca.png'},
    {'name': 'United States', 'flag': 'https://flagcdn.com/w2560/us.png'},
    {'name': 'Mexico', 'flag': 'https://flagcdn.com/w2560/mx.png'},
    {'name': 'Belize', 'flag': 'https://flagcdn.com/w2560/bz.png'},
    {'name': 'Costa Rica', 'flag': 'https://flagcdn.com/w2560/cr.png'},
    {'name': 'El Salvador', 'flag': 'https://flagcdn.com/w2560/sv.png'},
    {'name': 'Guatemala', 'flag': 'https://flagcdn.com/w2560/gt.png'},
    {'name': 'Honduras', 'flag': 'https://flagcdn.com/w2560/hn.png'},
    {'name': 'Nicaragua', 'flag': 'https://flagcdn.com/w2560/ni.png'},
    {'name': 'Panama', 'flag': 'https://flagcdn.com/w2560/pa.png'},
    {'name': 'Antigua and Barbuda', 'flag': 'https://flagcdn.com/w2560/ag.png'},
    {'name': 'Bahamas', 'flag': 'https://flagcdn.com/w2560/bs.png'},
    {'name': 'Barbados', 'flag': 'https://flagcdn.com/w2560/bb.png'},
    {'name': 'Cuba', 'flag': 'https://flagcdn.com/w2560/cu.png'},
    {'name': 'Dominica', 'flag': 'https://flagcdn.com/w2560/dm.png'},
    {'name': 'Dominican Republic', 'flag': 'https://flagcdn.com/w2560/do.png'},
    {'name': 'Grenada', 'flag': 'https://flagcdn.com/w2560/gd.png'},
    {'name': 'Haiti', 'flag': 'https://flagcdn.com/w2560/ht.png'},
    {'name': 'Jamaica', 'flag': 'https://flagcdn.com/w2560/jm.png'},
    {'name': 'Saint Kitts and Nevis', 'flag': 'https://flagcdn.com/w2560/kn.png'},
    {'name': 'Saint Lucia', 'flag': 'https://flagcdn.com/w2560/lc.png'},
    {'name': 'Saint Vincent and the Grenadines', 'flag': 'https://flagcdn.com/w2560/vc.png'},
    {'name': 'Trinidad and Tobago', 'flag': 'https://flagcdn.com/w2560/tt.png'},
    {'name': 'Argentina', 'flag': 'https://flagcdn.com/w2560/ar.png'},
    {'name': 'Bolivia', 'flag': 'https://flagcdn.com/w2560/bo.png'},
    {'name': 'Brazil', 'flag': 'https://flagcdn.com/w2560/br.png'},
    {'name': 'Chile', 'flag': 'https://flagcdn.com/w2560/cl.png'},
    {'name': 'Colombia', 'flag': 'https://flagcdn.com/w2560/co.png'},
    {'name': 'Ecuador', 'flag': 'https://flagcdn.com/w2560/ec.png'},
    {'name': 'Guyana', 'flag': 'https://flagcdn.com/w2560/gy.png'},
    {'name': 'Paraguay', 'flag': 'https://flagcdn.com/w2560/py.png'},
    {'name': 'Peru', 'flag': 'https://flagcdn.com/w2560/pe.png'},
    {'name': 'Suriname', 'flag': 'https://flagcdn.com/w2560/sr.png'},
    {'name': 'Uruguay', 'flag': 'https://flagcdn.com/w2560/uy.png'},
    {'name': 'Venezuela', 'flag': 'https://flagcdn.com/w2560/ve.png'}
]

def embeds(interaction: discord.Interaction, country_name = str, country_flag = str):
    user_avatar = interaction.user.avatar

    flag_guesser = discord.Embed(
        title = 'Guess the flag!',
        description = 'You have **15s** to guess the country! Remember that all the answers must be provided in **English**.',
        color = 0x2b2d31,
        timestamp = datetime.datetime.utcnow()
    )
    flag_guesser.set_footer(
        text = f'Requested by {interaction.user.name}',
        icon_url = user_avatar
    )
    flag_guesser.set_image(url = f'{country_flag}')

    time_fail = discord.Embed(
        title = 'You ran out of time!',
        description = f'**Correct answer:** {country_name}',
        color = 0xff5e57,
        timestamp = datetime.datetime.utcnow()
    )
    time_fail.set_image(url = f'{country_flag}')
    time_fail.set_footer(
        text = f'Requested by {interaction.user.name}',
        icon_url = user_avatar
    )

    answer_fail = discord.Embed(
        title = 'Your answer was wrong!',
        description = f'**Correct answer:** {country_name}',
        color = 0xff5e57,
        timestamp = datetime.datetime.utcnow()
    )
    answer_fail.set_image(url = f'{country_flag}')
    answer_fail.set_footer(
        text = f'Requested by {interaction.user.name}',
        icon_url = user_avatar
    )

    answer_correct = discord.Embed(
        title = 'Your answer was correct!',
        description = f'**Correct answer:** {country_name}',
        color = 0x0be881,
        timestamp = datetime.datetime.utcnow()
    )
    answer_correct.set_image(url = f'{country_flag}')
    answer_correct.set_footer(
        text = f'Requested by {interaction.user.name}',
        icon_url = user_avatar
    )

    return flag_guesser, time_fail, answer_fail, answer_correct

# TODO: create more tips and fun fucts to show in the description
def show_stats(interaction: discord.Interaction, mode: int, member = discord.Member):
    if mode == 1:
        database = europe
        stats_for = 'European'
    elif mode == 2:
        database = asia
        stats_for = 'Asian'
    elif mode == 3:
        database = africa
        stats_for = 'Asian'
    elif mode == 4:
        database = america
        stats_for = 'American'

    user_name = member.name
    user_id = member.id
    user_avatar = interaction.user.avatar

    response = [
        "Did you know? The flag of Nepal is the only national flag that is not rectangular in shape!",
        "Fun fact: The flag of Canada features a red maple leaf, which is a symbol of national pride and identity.",
        "Tip: Look for the number of stars on the flag of the United States to identify the number of states in the country.",
        "Did you know? The flag of Japan consists of a red circle representing the sun on a white background.",
        "Fun fact: The flag of Brazil has a unique design with a green field, a yellow diamond, and a blue circle with stars representing the night sky over Rio de Janeiro.",
        "Tip: Pay attention to the colors and patterns on the flag of South Africa to recognize its diverse population and cultural heritage.",
        "Did you know? The flag of Australia features the Union Jack in the canton, symbolizing its historical ties to Great Britain.",
        "Fun fact: The flag of Italy consists of three vertical stripes of green, white, and red, representing hope, faith, and charity.",
        "Tip: Look for the golden lion on the flag of Sri Lanka, which symbolizes bravery and strength.",
        "Did you know? The flag of Germany, also known as the 'Bundesflagge,' consists of three equal horizontal bands of black, red, and gold."
    ]

    random_response = choice(response)
    
    stats = discord.Embed(
        title = f'Displaying {stats_for} game of flags statistics for {user_name}',
        timestamp = datetime.datetime.utcnow()
    )
    stats.set_footer(
        text=f'Requested by {interaction.user.name}',
        icon_url = user_avatar
    )
    
    # filters database to find just the right user
    user_filter = {'user_id': user_id}

    # stats check
    user_data = database.find(user_filter)
    user_exists = user_data.count()

    current_user = database.find_one(user_filter)

    if user_exists == 0:
        stats.description = 'This user haven\'t played the game of flags before!'
        stats.color = 0xff5e57
    else: 
        games_played = current_user.get('games_played', 0)
        games_lost = current_user.get('games_lost', 0)
        wrong_answer = current_user.get('wrong_answer', 0)
        time_lost = current_user.get('time_lost', 0)
        highest_streak = current_user.get('highest_streak', 0)
        rounds_won = current_user.get('rounds_won', 0) # for the latest game
        
        stats.description = f'{random_response}'
        stats.color = 0x575fcf
        
        if wrong_answer == 0:
            wrong_perc = '0'
        else:
            wrong_perc = (wrong_answer/ games_lost) * 100
            wrong_perc = str(round(wrong_perc, 2))

        if time_lost == 0:
            time_perc = '0'
        else:
            time_perc = (time_lost / games_lost) * 100
            time_perc = str(round(time_perc, 2))
        
        stats.add_field(
        name = 'Games played',
        value = f'{games_played}',
        inline = True
        )
        stats.add_field(
            name = 'Games lost',
            value = f'{games_lost}',
            inline = True
        )
        stats.add_field(
            name = 'Wrong answers',
            value = f'{wrong_answer} – {wrong_perc}% of lost games.',
            inline = True
        )
        stats.add_field(
            name = 'Loses on time',
            value = f'{time_lost} – {time_perc}% of lost games.',
            inline = True
        )
        stats.add_field(
            name = 'Highest streak',
            value = f'{highest_streak}',
            inline = True
        )
        stats.add_field(
            name = 'Latest game streak',
            value = f'{rounds_won}',
            inline = True
        )

    return stats

def show_top(interaction: discord.Interaction, mode: int):
    if mode == 1:
        database = europe
    elif mode == 2:
        database = asia
    elif mode == 3:
        database = africa
    elif mode == 4:
        database = america
    
    top_players = database.find().sort("highest_streak", -1).limit(25)
    
    top = discord.Embed(
        title = 'Displaying Top 25 players.',
        color = 0x575fcf,
        timestamp = datetime.datetime.utcnow()
    )
    top.set_footer(
        text=f'Requested by {interaction.user.name}',
        icon_url = interaction.user.avatar
    )
    
    for index, player in enumerate(top_players, 1):
        player_name = player['user_name']
        highest_streak = player['highest_streak']
        top.add_field(
            name = f'{index}. {player_name}',
            value = f'**Highest Streak:** {highest_streak}',
            inline = False
        )
    
    return top

def random_country(country = str) -> tuple:
    if country == 'european':
        flags = european_flags
    elif country == 'asian':
        flags = asian_flags
    elif country == 'african':
        flags = african_flags
    elif country == 'american':
        flags = american_flags

    rand_country = choice(flags)
    country_name = rand_country['name']
    country_flag = rand_country['flag']

    return country_name, country_flag

async def start_game(self, interaction: discord.Interaction, mode: int) -> None:
    await interaction.response.send_message(content='Starting a game for you...', ephemeral=True, delete_after=1)

    if mode == 1:
        database = europe
    elif mode == 2:
        database = asia
    elif mode == 3:
        database = africa
    elif mode == 4:
        database = america

    user_filter = {'user_id': interaction.user.id}
    new_stats = {'$inc': {}, '$set': {}}
    new_time = {'$inc': {}}
    new_streak = {'$inc': {}}
    user_data = database.find_one(user_filter)
    user_avatar = interaction.user.avatar

    if not user_data:
        user_stats = {
            'user_id': interaction.user.id,
            'user_name': interaction.user.name,
            'games_played': 1,
            'games_lost': 0,
            'wrong_answer': 0,
            'time_lost': 0,
            'highest_streak': 0,
            'rounds_won': 0,
        }
        database.insert_one(user_stats)
    else:
        updated_stats = {'$inc': {'games_played': 1}}
        database.update_one(user_filter, updated_stats)
        game_start = {'$set': {'rounds_won': 0}}
        database.update_one(user_filter, game_start)
    
    while True:
        if mode == 1:
            country_name, country_flag = random_country(country = 'european')
        elif mode == 2:
            country_name, country_flag = random_country(country = 'asian')
        elif mode == 3:
            country_name, country_flag = random_country(country = 'african')
        elif mode == 4:
            country_name, country_flag = random_country(country = 'american')
        
        flag_guesser, time_fail, answer_fail, answer_correct = embeds(
            interaction=interaction, country_name=country_name, country_flag=country_flag)
        
        message = await interaction.channel.send(embed=flag_guesser)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        try:
            guess = await self.client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await message.edit(embed=time_fail)
            new_time['$inc']['games_lost'] = 1
            new_time['$inc']['time_lost'] = 1
            database.update_one(user_filter, new_time)
            break
        else:
            if guess.content.lower() == country_name.lower():
                await message.edit(embed=answer_correct)
                await asyncio.sleep(3)
                await message.delete()
                await guess.delete()
                
                user_data = database.find_one(user_filter)
                current_streak = user_data.get('rounds_won', 0)
                highest_streak = user_data.get('highest_streak', 0)
                
                if current_streak > highest_streak:
                    new_stats['$set']['highest_streak'] = current_streak
                
                new_stats['$inc']['rounds_won'] = 1
                database.update_one(user_filter, new_stats)
                continue
            else:
                await message.edit(embed=answer_fail)
                new_stats['$inc']['games_lost'] = 1
                new_stats['$inc']['wrong_answer'] = 1
                database.update_one(user_filter, new_stats)
        
        await guess.delete()
        break
    
    await asyncio.sleep(3)
    await message.delete()
    user_data = database.find_one(user_filter)
    current_streak = user_data.get('rounds_won', 0)
    highest_streak = user_data.get('highest_streak', 0)
    games_played = user_data.get('games_played', 0)
    
    if current_streak > highest_streak:
        new_streak['$inc']['highest_streak'] = 1
        database.update_one(user_filter, new_streak)
    
    suffix = ''
    if str(games_played)[-1] == '1':
        suffix = 'st'
    elif str(games_played)[-1] == '2':
        suffix = 'nd'
    elif str(games_played)[-1] == '3':
        suffix = 'rd'
    else:
        suffix = 'th'
    
    statistics = discord.Embed(
        title='Game has concluded!',
        description=f"Congratulations <@{interaction.user.id}>! You just completed your **{games_played}{suffix}** game with the streak of **{current_streak}** correct guesses! To display additional information about users just run the `/flags statistics` command or `/flags leaderboard` for global statistics.",
        color=0x575fcf,
        timestamp=datetime.datetime.utcnow()
    )
    statistics.set_footer(
        text=f'Requested by {interaction.user.name}',
        icon_url=user_avatar
    )
    
    await interaction.channel.send(embed=statistics)