import sqlite3
import os

CONFIG_PATH = "run/config.ini"

config = {}

def reload_config():
    if not os.path.exists(CONFIG_PATH):
        raise RuntimeError("Config not found; create run/config.ini and add values")
    with open(CONFIG_PATH, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            spl = line.partition("=")
            if spl[1]:
                key = spl[0].strip()
                val = spl[2].strip()
                config[key] = val
            else:
                key = spl[0]
                val = spl[0]
                config[key] = val

def init_db():
    conn = sqlite3.connect(config['DB_PATH'])
    conn.execute("""
CREATE TABLE IF NOT EXISTS "emotes" (
	"serverID"	INTEGER NOT NULL,
	"ename"	TEXT NOT NULL,
	"emoteID"	INTEGER NOT NULL,
	PRIMARY KEY("serverID","ename")
)
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "osubeatmaplink" (
	"channel"	INTEGER,
	PRIMARY KEY("channel")
)    
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "osutrack" (
	"username"	TEXT NOT NULL,
	"discordServerID"	TEXT NOT NULL,
	"plays"	TEXT,
	"lmt"	INTEGER NOT NULL,
	"pp"	INTEGER,
	"rank"	INTEGER,
	PRIMARY KEY("username","discordServerID")
)
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "users" (
    "discordID" INTEGER PRIMARY KEY,
    "osuUsername" TEXT
)
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "webhooks" (
	"discordID"	INTEGER NOT NULL,
	"channelID"	INTEGER NOT NULL,
	"webhook"	TEXT NOT NULL,
	PRIMARY KEY("discordID","channelID")
)    
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "youtubenotifs" (
	"id"	TEXT,
	"lastVid"	TEXT,
	"channels"	TEXT,
	PRIMARY KEY("id")
)
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "ranked" (
	"channel" INTEGER NOT NULL,
    PRIMARY KEY("channel")
)
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "loved" (
	"channel" INTEGER NOT NULL,
    PRIMARY KEY("channel")
)
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS "qualified" (
	"channel" INTEGER NOT NULL,
    PRIMARY KEY("channel")
)
""")
    conn.close()

reload_config()
init_db()