import requests
import json
import asyncio
import socket

from mcstatus import MinecraftServer

def pingMSServer(IP, port):
    server = MinecraftServer(IP, port)
    name = 'Vanilla'
    if port == 25566:
        name = "Modcraft (I don't understand what's happening and at this point I'm too afraid to ask)"
    elif port == 25567:
        name = 'Soulscraft (Prepare to Die)'
    try:
        status = server.status()
        msg = ''
        if status:
            msg = "{3} server is online and has {0} players. Connect via {1}:{2}".format(status.players.online, '98.194.112.73', port, name)
        else:
            msg = "{2} server is offline at {0}:{1}".format('98.194.112.73', port, name)
    except socket.error as socketerror:
        msg = "{2} server is offline at {0}:{1}".format('98.194.112.73', port, name)
    return msg

VSTATUS = None
async def serverWatchVanilla(IP, TOKEN, CHANNEL):
    global VSTATUS
    curStatus = 'off'
    while 1:
        baseURL = "https://discordapp.com/api/channels/{0}/messages".format(CHANNEL)
        headers = { "Authorization":"Bot {0}".format(TOKEN),
                    "User-Agent":"RoboCow",
                    "Content-Type":"application/json", }

        msg = pingMSServer(IP, 25565)
        
        if 'online' in msg: curStatus = 'on'
        else: curStatus = 'off'

        if VSTATUS is None:
            VSTATUS = curStatus
        elif curStatus != VSTATUS:
            POSTedJSON =  json.dumps ( {"content":msg} )
            r = requests.post(baseURL, headers = headers, data = POSTedJSON)
            VSTATUS = curStatus

        await asyncio.sleep(30)

MSTATUS = None
async def serverWatchMod(IP, TOKEN, CHANNEL):
    global MSTATUS
    while 1:
        baseURL = "https://discordapp.com/api/channels/{0}/messages".format(CHANNEL)
        headers = { "Authorization":"Bot {0}".format(TOKEN),
                    "User-Agent":"RoboCow",
                    "Content-Type":"application/json", }

        msg = pingMSServer(IP, 25566)
        curStatus = ''
        if 'online' in msg: curStatus = 'on'
        else: curStatus = 'off'

        if MSTATUS is None:
            MSTATUS = curStatus
        elif curStatus != MSTATUS:
            POSTedJSON =  json.dumps ( {"content":msg} )
            r = requests.post(baseURL, headers = headers, data = POSTedJSON)
            MSTATUS = curStatus
            
        await asyncio.sleep(30)

HSTATUS = None
async def serverWatchHard(IP, TOKEN, CHANNEL):
    global HSTATUS
    while 1:

        baseURL = "https://discordapp.com/api/channels/{0}/messages".format(CHANNEL)
        headers = { "Authorization":"Bot {0}".format(TOKEN),
                    "User-Agent":"RoboCow",
                    "Content-Type":"application/json", }

        msg = pingMSServer(IP, 25567)
        curStatus = ''
        if 'online' in msg: curStatus = 'on'
        else: curStatus = 'off'

        if HSTATUS is None:
            HSTATUS = curStatus
        elif curStatus != HSTATUS:
            POSTedJSON =  json.dumps ( {"content":msg} )
            r = requests.post(baseURL, headers = headers, data = POSTedJSON)
            HSTATUS = curStatus
            
        await asyncio.sleep(30)