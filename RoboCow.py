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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!server'):
        hostname = "98.194.112.73"
        response = os.system("ping -c 1 " + hostname)
        if response == 0:
            msg = 'Minecraft server is up'
        else:
            msg = 'Minecraft server is down'
        channel = message.channel
        await channel.send(msg)
    if message.content.startswith('!ask'):
        responseIndex = random.randint(0, len(eightBallResponses)-1)
        channel = message.channel
        print(responseIndex)
        await channel.send(eightBallResponses[responseIndex])
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        channel = message.channel
        await channel.send(msg)
    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')

client.run(TOKEN)

