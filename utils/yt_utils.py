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

api="AIzaSyCOHR7QL19fSYppTJu8jWr9LCF2b09U7Kk"

def getLastVid(id):
    r=requests.get(f'https://www.googleapis.com/youtube/v3/search?key={api}&channelId={id}&part=snippet,id&order=date&maxResults=1')
    return r.json()

def getChannel(id):
    r=requests.get(f'https://www.googleapis.com/youtube/v3/channels?part=snippet&id={id}&key={api}')
    return r.json()