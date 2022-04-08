#!/bin/sh
import discord
import random
import os
import asyncio
import socket
import platform
import json
import time
#import steam
from datetime import timedelta
import requests

import MCServerUtilities
#import steamStuff

PRODUCTION = 1

startTime = time.time()
# determines where it's being run to set the correct path
path = os.getcwd()
slash = '/'
# if not running on a macbook (where this is debugged)
if PRODUCTION:
    if platform.system() != 'Darwin':
        path = 'C:\\Users\\hotmr\\Dropbox\\Robot_Overlords'
        slash = '\\'

# load constants and data from files (besides users.json)
CHANNELS = {
    #avengers
    "shield-headquarters" : "519210590934401040",
    "the-meme-dept" : "519211875016114177",
    "recreation-services" : "519212454912327697",
    "fabrication-labritories" : "519213405937336331",
    "the-mainframe" : "519211111787266075",
    "the-war-room" : "519211536619929609",
    "department-of-audio" : "519215178047291422",
    "shield-garage" : "522115108189503498",
    "center-for-adulting" : "521847285894742038",
    "deadpools-shady-hotel-room" : "519213829540937728",
    "department-of-big-ol-anime-tiddies" : "524389973735112715",
    "the-guidebook" : "519228931371433984",
    "ultron" : "572171381815377922",
    "power-stone" : "616808934187204618",
    #dc
    "edgy-chat" : "240282018510929920",
    "into-the-darkness" : "572121647629336588",
    "even-edgier-chat" : "337677719347265536",
    "crime-scene-photos" : "390523219594969119",
    "the-sewer, you heathen" : "619380141679968256"
}

# keeps token and ip off public github
TOKEN = ''
with open(path+'token.private') as file:
    TOKEN = file.read()
print(TOKEN)

IP = ''
with open(path+slash+'ip.private') as file:
    IP = file.read()
print(IP)

eightBallResponses = []
with open(path+slash+'eightBallResponses') as file:
    for line in file.readlines():
        eightBallResponses.append(line.strip())

# initialize client
client = discord.Client()

#returns instructions string
def getHelp():
    return """List of commands:
!ip - get server IP
!vanilla - get vanilla server status (25565)
!modcraft - get modded server status (25566)
!diecraft - get amped server status (25567)
!roll xDx - roll dice
!ask - ask magic 8 ball
!level - get level in current chat
!hiscores [optional: here] [optional: length of list]
!totalxp - get sum of all XP collected and tracked by RoboCow
!uptime - get uptime
"""

# returns ', Dad' if user is dad
def isDad(message):
    if str(message.author) == 'cowsareinme#1533':
        return ', Dad'
    # Calls Laura Crazy Lady
    elif str(message.author) == 'PsychoSqushie#2941':
        return ', Crazy Lady'
    # Calls Ryan Fool
    elif str(message.author) == 'Excalibur#7087':
        return ', Fool'
    # Calls Shannon Muse
    elif str(message.author) == 'Shannon#9098':
        return ', Muse'
    else: return ''

def getUptime():
    global startTime
    return timedelta(seconds=(time.time()-startTime))
    
def getWaifu(string):
    category = string.split()[1]
    categories = 'waifu,neko,shinobu,megumin,bully,cuddle,cry,hug,awoo,kiss,lick,pat,smug,bonk,yeet,blush,smile,wave,highfive,handhold,nom,bite,glomp,slap,kill,kick,happy,wink,poke,dance,cringe'.split(',')
    if category not in categories:
        return 'Please pick from this cursed list (all sfw):\nwaifu, neko, shinobu ,megumin, bully, cuddle, cry, hug, awoo, kiss, lick, pat, smug, bonk, yeet, blush, smile, wave, highfive, handhold, nom, bite, glomp, slap, kill, kick, happy, wink, poke, dance, cringe'
    else:
        response = requests.get('https://api.waifu.pics/sfw/'+category)
        url = json.loads(response.text)['url']
        return url
    

# custom dice roll procedure
def rollDice(string):
    s = string.split()
    msg = ''
    print(s)
    nums = s[1].split('d')
    if len(nums) == 1: nums = s[1].split('D')
    if len(nums) == 1: 
        msg = ("Bad read format should look like '!roll xdx'")
    else:
        dice = int(nums[1])
        times = int(nums[0])   
        if dice >= 1000000000 or times > 100000000:
            msg = "What does a dice of that many sides even look like?"
        else:
            result = 0
            string = ''
            for x in range(0, times):
                roll = random.randint(1, dice)
                string = string+str(roll)+' + '
                result+=roll
            if len(str(string)) < 1900:
                msg = string[0:-3]+'\nRESULT: '+str(result)
            else:
                msg = 'Discord won''t let me send you over 2000 characters of addition, so trust me on this one.\nRESULT: '+str(result)
    return msg

def getChannelName(ID):
    for key, value in CHANNELS.items():
        if value == str(ID):
            return key
    return "a channel that I don't recognize. If cows sees this, he'll add it."

# level up stuff
async def update_data(users, user, channel):
    if not f"{user.id}-{channel.id}" in users:
        users[f"{user.id}-{channel.id}"] = {}
        users[f"{user.id}-{channel.id}"]["experience"] = 0
        users[f"{user.id}-{channel.id}"]["level"] = 1
        users[f"{user.id}-{channel.id}"]["last_message"] = 0
        users[f"{user.id}-{channel.id}"]["give-shit"] = 1
        # this is finished annoying everybody
        # await channel.send( f"LevelUp minigame is on for this channel, and you are in by default, but type !no if you don't want to be notified when you level up.")

async def add_experience(users, user, exp, channel):
    if time.time() - users[f"{user.id}-{channel.id}"]["last_message"] > 15: 
        users[f"{user.id}-{channel.id}"]["experience"] += exp
        users[f"{user.id}-{channel.id}"]["last_message"] = time.time()
    else:
        return

async def level_up(users, user, channel):
    experience = users[f"{user.id}-{channel.id}"]["experience"]
    lvl_start = users[f"{user.id}-{channel.id}"]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        if users[f"{user.id}-{channel.id}"]["give-shit"] == 1:
            await channel.send( f":tada: Congrats {user.mention}, you levelled up to level {lvl_end} in {getChannelName(channel.id)}!")
        users[f"{user.id}-{channel.id}"]["level"] = lvl_end

async def getUserXP(users, user, channel):
    if f"{user.id}-{channel.id}" in users:
        return f"{user.mention}, you are level {users[user.id + '-' + channel.id]['level']} in {getChannelName(channel.id)}, nice."
    else:
        return "I have failed you. Yell at cows."

def gethiscores(users, channel):
    simple = {}
    for key, value in users.items():
        simple[value['experience']] = key
    
    scores = []
    for key in sorted(simple.keys(), reverse=True):
        userID = simple[key].split('-')[0]
        chanelID = simple[key].split('-')[1]
        user = [userID, chanelID, key]
        if str(chanelID) == str(channel):
            scores.append(user)
        elif channel == -1:
            scores.append(user)

    return scores

def getTotalXP(users):
    xp = 0
    for key, value in users.items():
        xp += value['experience']
    return xp

def urlCheck(message):
    return 'https://' in message.content

# listens for messages
@client.event
async def on_message(message):
    # xp stuff
    with open("users.json", "r") as f:
        users = json.load(f)
        if message.author.bot: # bot xp?
            return
        else:
            await update_data(users, message.author, message.channel)
            number = random.randint(5,8)
            await add_experience(users, message.author, number, message.channel)
            await level_up(users, message.author, message.channel)

        with open("users.json", "w") as f:
            json.dump(users, f)

    # return if sender is a bot or self
    if message.author == client.user:
        return
    if message.author.bot:
        return

    if message.content.startswith('!server'):
        msg = 'Not a valid server. Try: !vanilla, !modcraft, or !diecraft'
        channel = message.channel
        await channel.send(msg)
    
    if message.content.startswith('!level'):
        with open("users.json", "r") as f:
            users = json.load(f)
            user = message.author
            channel = message.channel
            msg = "I have failed you. Yell at cows."
            if f"{user.id}-{message.channel.id}" in users:
                msg = f"{user.mention}, you are level {users[str(user.id) + '-' + str(channel.id)]['level']} in {getChannelName(channel.id)}, nice."
            await channel.send(msg)

    if message.content.startswith('!hiscores'):
        msg = ''
        channelID = -1
        if ' here' in message.content:
            channelID = message.channel.id
            msg+= 'Local Hiscores:\n'
        else:
            msg+= 'Global Hiscores:\n'

        listLength = 5
        channel = message.channel
        if message.content[-2:].isdigit():
            listLength = int(message.content[-2:])
        elif message.content[-1:].isdigit():
            listLength = int(message.content[-1:])
        with open("users.json", "r") as f:
            users = json.load(f)
            scores = gethiscores(users, channelID)
            shortenedList = scores[0:listLength]
            count = 1
            for score in shortenedList:
                # user = [userID, chanelID, key]
                user = await client.fetch_user(score[0])
                #TODO doesn't dispaly nickname
                username = user.display_name
                channelname = getChannelName(score[1])
                xp = score[2]
                msg += f"{count}. {username}\n\t In {channelname} with {xp} xp\n"
                count += 1
            await channel.send(msg)

    if message.content.startswith('!totalxp'):
        with open("users.json", "r") as f:
            users = json.load(f)
            xp = getTotalXP(users)
            msg = f'Total XP collected: {xp}'
            channel = message.channel
            await channel.send(msg)

    if message.content.startswith('!no'):
        with open("users.json", "r") as f:
            users = json.load(f)
            user = message.author
            channel = message.channel
            msg = f"LevelUp muted for {user.mention}"
            if f"{user.id}-{message.channel.id}" in users:
                users[f"{user.id}-{channel.id}"]["give-shit"] = 0
            with open("users.json", "w") as f:
                json.dump(users, f)
            await channel.send(msg)

    if message.content.startswith('!wtp'):
        text = message.content.split(' ')
        author = str(message.author)
        channel = message.channel
        if len(text) != 3:
            msg = f'Must include 2 users. Example: !wtp @Robocow @{author}'
            await channel.send(msg)
        else:
            users = message.mentions
            user1 = users[0].name+'#'+users[0].discriminator
            user2 = users[1].name+'#'+users[1].discriminator

            with open(path+slash+'steamInfo.json') as f:
                steamInfo = json.load(f)
                
                # get both users steamIDs
                if user1 not in steamInfo.keys():
                    await channel.send(f"{author}, what is {user1}'s steam profile URL?")
                    msg = await client.wait_for('message', check=urlCheck, timeout =40)
                    user1ID = steamStuff.getID(msg.content)
                    steamInfo[user1] = [msg.content, user1ID]
                else:
                    user1ID = steamInfo[user1][1]
                if user2 not in steamInfo.keys():
                    await channel.send(f"{author}, what is {user2}'s steam profile URL?'")
                    msg = await client.wait_for('message', check=urlCheck, timeout =40)
                    user2ID = steamStuff.getID(msg.content)
                    steamInfo[user2] = [msg.content, user2ID]
                else:
                    user2ID = steamInfo[user2][1]

                # TODO use steamIDs to get game lists

                await channel.send(user1+' '+user2)

                with open("steamInfo.json", "w") as f:
                    json.dump(steamInfo, f)

    if message.content.startswith('!diecraft'):
        msg = MCServerUtilities.pingMSServer(IP, 25567)
        channel = message.channel
        await channel.send(msg)

    if message.content.startswith('!vanilla'):
        msg = MCServerUtilities.pingMSServer(IP, 25565)
        channel = message.channel
        await channel.send(msg)

    if message.content.startswith('!modcraft'):
        msg = MCServerUtilities.pingMSServer(IP, 25566)
        channel = message.channel
        await channel.send(msg)

    if message.content.startswith('!ip') or message.content.startswith('!IP'):
        channel = message.channel
        await channel.send(IP)

    if message.content.startswith('!ask'):
        if message.content[-2:] == '??':
            msg = 'Fuck yeah'+isDad(message)
            channel = message.channel
            await channel.send(msg)
        elif message.content[-2:] == ' ?':
            msg = 'Fuck no'+isDad(message)
            channel = message.channel
            await channel.send(msg)
        else:
            responseIndex = random.randint(0, len(eightBallResponses)-1)
            channel = message.channel
            await channel.send(eightBallResponses[responseIndex]+isDad(message))

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        if isDad(message) == ', Dad': msg = 'Hi Daddy'
        channel = message.channel
        await channel.send(msg)

    if message.content.startswith('!roll'):
        channel = message.channel
        content = str(message.content)
        msg = rollDice(content)
        await channel.send(msg)
        
    if message.content.startswith('!waifu'):
        channel = message.channel
        content = str(message.content)
        msg = getWaifu(content)
        await channel.send(msg)

    if message.content.startswith('!uptime'):
        channel = message.channel
        msg = getUptime()
        await channel.send(msg)

    if message.content.startswith('!whoami'):
        channel = message.channel
        msg = getUptime()
        await channel.send(msg)

    if message.content.startswith('!help'):
        channel = message.channel
        await channel.send(getHelp())

    # Template for adding simple custom commands for anyone not comfy in python
    #if message.content.startswith('{!COMMAND}'):
        #msg = '{MESSAGE}'
        #channel = message.channel
        #await channel.send(msg)

# listens for reactions
#@client.event
#async def on_reaction_add(reaction, user):
#  if reaction.emoji == '👍':
    #do stuff

def NEWLIFE():
    lastTime = 0
    with open(path+slash+'lastStartTime.txt') as file:
        lastTime = file.read()

    totalTime = timedelta(seconds=(time.time()-float(lastTime)))
    msg = f'I HAVE BEEN REBORN ONCE AGAIN INTO THIS MORTAL COIL\nFs in the chat for my last life, which lasted {totalTime}'

    with open(path+slash+'lastStartTime.txt', 'w') as file:
        file.write(str(time.time()))
        file.close()

    baseURL = "https://discordapp.com/api/channels/{0}/messages".format(CHANNELS["ultron"])
    headers = { "Authorization":"Bot {0}".format(TOKEN),
                "User-Agent":"RoboCow",
                "Content-Type":"application/json", }
    POSTedJSON =  json.dumps ( {"content":msg} )
    r = requests.post(baseURL, headers = headers, data = POSTedJSON)

# runs at startup
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    client.loop.create_task(MCServerUtilities.serverWatchVanilla(IP, TOKEN, CHANNELS["recreation-services"]))
    client.loop.create_task(MCServerUtilities.serverWatchMod(IP, TOKEN, CHANNELS["recreation-services"]))
    client.loop.create_task(MCServerUtilities.serverWatchHard(IP, TOKEN, CHANNELS["recreation-services"]))
    print('LETS GO BOIS')
    if PRODUCTION:
        NEWLIFE()


client.run(TOKEN)

