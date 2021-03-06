#!/bin/sh
from mcstatus import MinecraftServer
import discord
import random
import os
import asyncio
import socket
import platform

# determines where it's being run to set the correct path
path = ''
if platform.system() != 'Darwin':
    path = '/home/pi/RoboCow/'

# keeps token and ip off public github
TOKEN = ''
with open(path+'token.private') as file:
    TOKEN = file.read()
print(TOKEN)

IP = ''
with open(path+'ip.private') as file:
    IP = file.read()
print(IP)

# may be useful someday to know what channels are gaming related
#GAME_CHANNELS = ['572156522071719945']

eightBallResponses = []
with open(path+'eightBallResponses') as file:
    for line in file.readlines():
        eightBallResponses.append(line.strip())
print(eightBallResponses)

# initialize client
client = discord.Client()
#returns instructions string
def getHelp():
    return """List of commands:
!ip - get server IP
!server - get server status
!roll xDx - roll dice
!ask - ask magic 8 ball
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
                msg = 'Discord won''t let me show you over 2000 lines of addition, so trust me on this one.\nRESULT: '+str(result)
    return msg

# listens for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!server'):
        server = MinecraftServer(IP, 25565)
        try:
            status = server.status()
            msg = ''
            if status:
                msg = "The minecraft server has {0} players and replied in {1} ms".format(status.players.online, status.latency)
            else:
                msg = 'Offline'
            channel = message.channel
            await channel.send(msg)
        except socket.error as socketerror:
            msg = 'Minecraft server is offline'
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
    if message.content.startswith('!help'):
        channel = message.channel
        await channel.send(getHelp())
    # Template for adding simple custom commands for anyone not comfy in python
    #if message.content.startswith('{!COMMAND}'):
        #msg = '{MESSAGE}'
        #channel = message.channel
        #await channel.send(msg)

# runs at startup
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # how to start an async child proc
    #client.loop.create_task(serverWatchdog(client))
    print('LETS GO BOIS')

client.run(TOKEN)

