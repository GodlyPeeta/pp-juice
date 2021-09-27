import asyncio, discord
from discord.ext import commands
from discord.ext import tasks
import cogs, json
from ossapi import ossapi
from PIL import Image
import discord.emoji, sqlite3
from sqlite3 import Error
import time, bitwiseEnum, threading, config, strain, requests, utils
from multiprocessing import Pool
from os import getpid
import datetime, threading, urllib.request

import sys
import pyttanko as pyt

'''p = pyt.parser()
f = open('lib/map.txt', 'r', encoding="utf8")
bmap = p.map(f)

stars = pyt.diff_calc().calc(bmap)
print("%g stars" % stars.total)

pp, _, _, _, _ = pyt.ppv2(stars.aim, stars.speed, bmap=bmap)
print("%g pp" % pp)'''

'''#print(ppcalc.ppcalculate(90, 123, 0, '', 'lib/map.txt', False))

def ppcalculate(ac, co, mi, mo, link, feature=True, c300=0, c100=0, c50=0):
    mods = pyt.mods_from_str(mo)
    p = pyt.parser()
    f = open(link, 'r', encoding="utf8")
    bmap = p.map(f)
    #print(bmap.hitobjects)
    if c300 == 0 and c100 == 0 and c50 == 0:
        temp = pyt.acc_round(ac, bmap.ncircles+bmap.nsliders+bmap.nspinners, mi)
        c300 = temp[0]
        c100 = temp[1]
        c50 = temp[2]

    stars = pyt.diff_calc().calc(bmap)

    stats = pyt.mods_apply(mods, ar=bmap.ar, od=bmap.od, cs=bmap.cs, hp=bmap.hp)
    #print(stats)

    pp, _, _, _, _ = pyt.ppv2(stars.aim, stars.speed, bmap=bmap, combo = co, nmiss=mi, n50=c50, n300 = c300, n100 = c100)

    #return round(pp.pp, 2), str(round(map.ar, 2)), str(round(map.cs, 2)), str(round(map.od, 2)), str(round(diff[0], 2)), str(round(diff[1], 2)), str(round(diff[2], 2)), map.speed, str(round(map.hp,2))
    return pp, stats[1], stats[3], stats[2], stars.aim, stars.speed, stars.total, stats[0], stats[4]

print(ppcalculate(90, 123, 0, '', 'lib/map.txt', False))'''

import ppcalc

#ppcalc.getReplayById(3803171282)

print(ppcalc.processBeatmapIntoHitboxes("lib/map.txt"))