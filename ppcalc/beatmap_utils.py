import asyncio, discord
from math import nan
from discord.ext import commands
from discord.ext import tasks
from ossapi import ossapi
from PIL import Image
import discord.emoji, sqlite3
from utils.init_utils import config
from multiprocessing import Pool
from os import getpid
import datetime, threading, urllib.request
import random

import base64
import lzma

import sys
import pyttanko as pyt

tokens = config['OSU_TOKEN']

def processBeatmapIntoHitboxes(maplink):
    radius = 0
    f = open(maplink, "r")
    ret = []
    ho = False

    for line in f:
        l = line.rstrip()

        if ho:
            if l == '\n':
                break
            ret.append(l.split(",")[:3])
        if l[:12] == "[HitObjects]":
            ho = True
        if l[:11] == "CircleSize:":
            radius = (512/16)*(1-(0.7*(int(l[11:12])-5)/5)) #SOURCE: https://www.reddit.com/r/osugame/comments/4pz8nr/how_to_click_beside_circles_in_osu_and_get_300/d4p2so0/ practically accurate based on hovering over stats
        
    return {"radius": radius,
            "hitobjects": ret}


