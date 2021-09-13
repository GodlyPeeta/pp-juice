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
import json
from bs4 import BeautifulSoup

def enable_beatmap_link(conn, channel):
    """
    Create a new project into the projects table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ''' INSERT INTO osubeatmaplink(channel)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (channel,))
    conn.commit()
    return cur.lastrowid

def disable_beatmap_link(conn, channel):
    cur = conn.cursor()
    #print(discordID)
    cur.execute("DELETE FROM osubeatmaplink WHERE channel=?", (channel,))
    conn.commit()

def get_beatmaplink_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM osubeatmaplink")

    rows = cur.fetchall()
    rows2=[]
    for r in rows:
        rows2.append(r[0])

    return rows2

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def mapfeed_add(conn, channel, ty):
    """
    add channel to the mapfeed for type
    :param conn:
    :param channel:
    :param type:
    """
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {ty}(channel) \nVALUES(?)", (channel,))
    conn.commit()

def mapfeed_del(conn, channel, ty):
    """
    remove channel from mapfeed for type
    :param conn:
    :param channel:
    :param type:
    """
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {ty} WHERE channel=?", (channel,))

def mapfeed_get(conn, ty):
    """
    get all channels that are tracking for that type
    :param conn:
    :param type:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {ty}")
    rows = cur.fetchall()
    rows2=[]
    for r in rows:
        rows2.append(r[0])
    return rows2

def mapfeed_get_new(conn):
    """
    get newest ranked, loved or qualified
    """
    r = requests.get("https://osu.ppy.sh/beatmapsets/events?user=&types%5B%5D=qualify&types%5B%5D=rank&types%5B%5D=love&types%5B%5D=disqualify&min_date=&max_date=", headers = {'User-agent': 'GodlyPeeta#7272'}).content
    s = BeautifulSoup(r, 'html.parser')
    #print(s.prettify())
    s=s.find("script",{'id': 'json-events'}).contents[0]
    
    j=json.loads(str(s))[0]
    #print(j)
    #print(j)

    state = j['type']
    beatmap_id = j['beatmapset']['id']
    return [state, beatmap_id]

def add_yt_channel_notif(conn, id):
    sql = ' INSERT INTO youtubenotifs(id, channels)\n              VALUES(?,?) '
    cur = conn.cursor()
    cur.execute(sql, id)
    conn.commit()
    return cur.lastrowid

def del_yt_channel_notif(conn, id):
    cur = conn.cursor()
    cur.execute('DELETE FROM youtubenotifs WHERE id=?', id)
    conn.commit()

def yt_notif_getchannels(conn, id):
    cur = conn.cursor()
    cur.execute('SELECT channels FROM youtubenotifs WHERE id=?', id)
    rows = cur.fetchall()
    return rows[0][0]

def yt_notif_lastVid(conn, id):
    sql = 'UPDATE youtubenotifs SET lastVid= ? WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, id)
    conn.commit()

def yt_notif_getAll(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM youtubenotifs')
    rows = cur.fetchall()
    return rows
