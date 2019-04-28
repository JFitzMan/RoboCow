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

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        channel = message.channel
        await channel.send(msg)

@client.event
async def on_message(message):
    global eightBallResponses
    if message.author == client.user:
        return
    if message.content.startswith('!8ball'):
        responseIndex = random.randint(0, len(eightBallResponses))
        channel = message.channel
        await channel.send(eightBallResponses[responseIndex])

mport os
hostname = "google.com" #example
response = os.system("ping -c 1 " + hostname)

#and then check the response...
if response == 0:
  print hostname, 'is up!'
else:
  print hostname, 'is down!'

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
        await channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')

client.run(TOKEN)

