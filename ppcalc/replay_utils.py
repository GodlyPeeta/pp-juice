import asyncio, discord
from math import nan
from discord.ext import commands
from discord.ext import tasks
from ossapi import ossapi
from PIL import Image
import discord.emoji, sqlite3
import config
from multiprocessing import Pool
from os import getpid
import datetime, threading, urllib.request
import random

import base64
import lzma

import sys
import pyttanko as pyt

tokens = config.OSU_TOKEN

def getReplayById(scoreid):
    token = tokens[random.randint(0, len(tokens)-1)]
    print(f"token used: {token}")
    api = ossapi(token)

    r = api.get_replay({'s': str(scoreid)})
    try:
        s = base64.b64decode(r['content'])
    except:
        return None

    #TODO: fix this, it is currently making a new .lzma file every time and decoding that which is bad and nto good and bad (((((redo to do it in memory later)))))
    f = open('./lib/replay.lzma', "wb")
    f.write(s)
    output = lzma.open("./lib/replay.lzma", "rb")
    data = output.read().decode("utf-8")
    arr = data.split(',')
    out=[]
    for i in arr:
        out.append(i.split('|'))
    del out[-2:] # last 2 are peppy's seed and empty list
    return out

def processReplayByClickStart(decodedReplay, hitWindow, hitObjects):
    lastk1 = False
    lastk2 = False

