import ppcalc
import asyncio
import discord
from discord.ext import commands
from discord.ext import tasks
import cogs
import json
from ossapi import ossapi
from PIL import Image
import discord.emoji
import sqlite3
from sqlite3 import Error
import time
import bitwiseEnum
import threading
import config
import strain
import requests
import os
import time
import random

def roll(per):
    outof=100
    
    return (random.uniform(0, outof) <= per)

def edit_dist(s, t):
    dist = [[0 for i in range(len(t)+1)] for j in range(2)]
    for i in range(0, len(t)+1):
        dist[0][i] = i
    for i in range(1, len(s)+1):
        dist[i % 2][0] = i
        for j in range(1, len(t)+1):
            if s[i-1] == t[j-1]:
                #why the fuck is there a ; here this isnt java are u high
                dist[i % 2][j] = dist[(i-1) % 2][j-1];
            else:
                dist[i % 2][j] = 1 + min(
                    dist[(i-1) % 2][j-1],
                    dist[(i-1) % 2][j],
                    dist[i % 2][j-1]
                )
    return dist[len(s) % 2][len(t)]

def text_similarity(s, t): # TODO: this is buggy. fix
    return 1-edit_dist(s, t)/len(s)

def has_admin(user):
    flag = False
    lst = user.roles
    for i in lst:
        if i.permissions.administrator:
            flag = True
            break
    return flag

def is_owner(user):
    if user.id == config.OWNER:
        return True
    else:
        return False

def kwargs(str, arg, flags = []):
    if (type(arg) == list):
        b = False
        for i in arg:
            if i in str:
                b = True
        return b
    else:
        if arg in str:
            if 'remove' in flags:
                return str.replace(arg, '')
            return True

def measure_freq():
    f = os.popen("sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq").readline()
    return f

def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return float(temp.replace("temp=","").replace("'C\n",""))