import discord
import random

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
        print(responseIndex)
        channel = message.channel
        await channel.send(eightBallResponses[responseIndex])

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')

client.run(TOKEN)

