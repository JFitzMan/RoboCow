import discord
import random
import os
import asyncio

TOKEN = ''
with open(r"token.private") as file:
    TOKEN = file.read()
print(TOKEN)

IP = ''
with open(r"ip.private") as file:
    IP = file.read()
print(IP)

GAME_CHANNELS = ['572156522071719945']

eightBallResponses = []
with open(r"eightBallResponses") as file:
    for line in file.readlines():
        eightBallResponses.append(line.strip())
print(eightBallResponses)

client = discord.Client()

def getHelp():
    return """List of commands:
!ip - get server IP
!server - get server status
!roll xDx - roll dice
!ask - ask magic 8 ball
"""

async def serverWatchdog(client):
    ping = False
    await client.wait_until_ready()
    while True:
        response = os.system("ping -c 1 " + IP)
        if response == 0:
            if ping == False:
                ping = True
                for chan in GAME_CHANNELS:
                    channel = discord.Object(id=chan)
                    print(channel)
                    await client.send_message(channel, "Server is up")
            else:
                print('Ping unchanged: on')
        else:
            if ping == 1:
                ping = False
                channel = discord.Object(id='572156522071719945')
                print(channel)
                print('its off')
            else:
                print('Ping unchanged: off')

        await asyncio.sleep(3)

def isDad(message):
    if str(message.author) == 'cowsareinme#1533':
        return ', Dad'
    else: return ''

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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!server'):
        response = os.system("ping -c 1 " + IP)
        if response == 0:
            msg = 'Minecraft server is up'+isDad(message)
        else:
            msg = 'Minecraft server is down'+isDad(message)
        channel = message.channel
        await channel.send(msg)
    if message.content.startswith('!ip') or message.content.startswith('!IP'):
        channel = message.channel
        await channel.send(IP)
    if message.content.startswith('!ask'):
        responseIndex = random.randint(0, len(eightBallResponses)-1)
        channel = message.channel
        await channel.send(eightBallResponses[responseIndex]+isDad(message))
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        if isDad(message) == ', Dad': msg = 'Hi Dad'
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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
  #client.loop.create_task(serverWatchdog(client))
    print('LETS GO BOIS')

client.run(TOKEN)

