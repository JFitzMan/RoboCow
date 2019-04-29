import discord
import random
import os

TOKEN = ''
with open(r"token.no") as file:
    TOKEN = file.read()

eightBallResponses = []
with open(r"eightBallResponses") as file:
    for line in file.readlines():
        eightBallResponses.append(line.strip())
print(eightBallResponses)

client = discord.Client()

def isDad(message):
    if str(message.author) == 'cowsareinme#1533':
        return ', Dad'
    else: return ''

async def rollDice(string):
    s = string.split()
    msg = ''
    print(s)
    nums = s[1].split('d')
    if len(nums) == 1: nums = s[1].split('D')
    if len(nums) == 1: 
        await channel.send("Bad read format should look like '!roll xdx'")
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
        hostname = "98.194.112.73"
        response = os.system("ping -c 1 " + hostname)
        if response == 0:
            msg = 'Minecraft server is up'+isDad(message)
        else:
            msg = 'Minecraft server is down'+isDad(message)
        channel = message.channel
        await channel.send(msg)
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
        msg = diceRoll(content)
        await channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')

client.run(TOKEN)

