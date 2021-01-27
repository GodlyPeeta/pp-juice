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
