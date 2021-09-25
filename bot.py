import discord
from discord.ext import commands
from discord.ext import tasks
import cogs
import sqlite3
from sqlite3 import Error
import time
from discord import Webhook, RequestsWebhookAdapter, File
from discord.utils import get
import config
from datetime import date
import datetime  
import utils
import sys
import time
import io
# create_user(conn, (70, "abcd")) id, osuUsername
# update_user(conn, ("FUCK", 69)) osuUsername, id
# get_user(conn, discordID) just the id, gets a tuple (69, 'FUCK') (same with get_user_osu and the other variants)

def get_user_osu(conn, discordID):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE discordID=?", (discordID,))

    rows = cur.fetchall()

    for row in rows:
        return row[1]


def delete_user(conn, discordID):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param discordID: id of the task
    :return:
    """
    sql = 'DELETE FROM users WHERE discordID=?'
    cur = conn.cursor()
    cur.execute(sql, (discordID,))
    conn.commit()


def delete_emote(conn, emote):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param discordID: id of the task
    :return:
    """
    sql = 'DELETE FROM emotes WHERE ename=?'
    cur = conn.cursor()
    cur.execute(sql, (emote,))
    conn.commit()



def get_user(conn, discordID):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE discordID=?", (discordID,))

    rows = cur.fetchall()

    for row in rows:
        return row


def get_emote(conn, emote):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM emotes WHERE ename=? AND serverID=?", emote)

    rows = cur.fetchall()
    for row in rows:
        return row


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

def get_all_emotes(conn, server):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM emotes WHERE serverID=?", server)

    rows = cur.fetchall()
    return rows


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(conn, user):
    """
    Create a new project into the projects table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ''' INSERT INTO users(discordID, osuUsername)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def get_webhook(conn, webhook):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM webhooks WHERE discordID=? AND channelID=?", webhook)

    rows = cur.fetchall()
    print(rows)
    for row in rows:
        return row

def add_webhook(conn, webhook):
    """
    Create a new project into the projects table
    :param conn:
    :param webhook:
    :return: user id
    """
    sql = ''' INSERT INTO webhooks(discordID, webhook)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def update_user(conn, user):
    """
    update osuUsername
    :param conn:
    :param user:
    :return: user id
    """
    sql = ''' UPDATE users
              SET osuUsername= ?
              WHERE discordID = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()



def main():
    database = config.DB_PATH

    # create a database connection
    conn = create_connection(database)

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        discordID integer PRIMARY KEY,
                                        osuUsername text
                                    ); """

    # create table
    if conn is not None:
        # create users table
        create_table(conn, sql_create_users_table)
    else:
        print("you;re dumb")

    with conn:
        print(get_user_osu(conn, 69) + "<-- if this says \"FUCK\" that means there arent compile and sql errors, if it says something else you fucked up a lot")


if __name__ == '__main__':
    main()

prefix = "pp."
intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')
bot.add_cog(cogs.nh(bot))
bot.add_cog(cogs.OSU(bot))
bot.add_cog(cogs.GENERAL(bot))
bot.add_cog(cogs.RANDOM(bot))
bot.add_cog(cogs.VOICE(bot))
bot.add_cog(cogs.YOUTUBE(bot))

stalkerBot = commands.Bot(command_prefix=prefix, intents=intents)

current_time = datetime.datetime.now()
lastDay = 0

database = config.DB_PATH
# create a database connection
conn = create_connection(database)
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Streaming(name=" with your pp.help", url="https://www.youtube.com/watch?v=oHg5SJYRHA0"))
    print('We have logged in as {0.user}'.format(bot))
    '''
    while True:
        await bot.get_channel(644268290474115075).send("pings")'''

@bot.event
async def on_message(message):
    if message.content.lower() == "ratio":
        await message.add_reaction("❤️")
    if message.content.lower() == "i asked" '''or str(message.author.id) == "695357678909653093"''':
        tempmsg = await message.channel.send("ratio")
        await tempmsg.add_reaction("❤️")
        #await tempmsg.add_reaction("🔃️")

    if message.author.bot == True:
        return
    if (str(message.author.id) == "773016933511200800" or str(message.author.id) == "626604979272024084" or str(message.author.id) == "414848078244347904" or str(message.author.id) == "357663900180676610") and str(message.content)[:9] == 'pp.osuset':
        await message.channel.send("fuck off retard")
        return 
    if str(message.author.id) == "414848078244347904":
        if (utils.roll(10)):
            await message.channel.send("you are  bad")

    '''for i in message.content: 
        if '''
    
    if "https://osu.ppy.sh/b" == message.content[:20]:
        if message.channel.id in utils.get_beatmaplink_all(conn):
            #print("kdsfjd")
            await message.channel.send(embed = cogs.OSU.beatmaplinkembed(message.content))
    if message.channel.id == 771776176359473152 or message.channel.id == 771772013198049280:
        return
    
    msg = message.content

    el = get_all_emotes(conn, (message.guild.id,))
    #print(el)
    msg2 = msg
    for e in el:
        msg2=msg2.replace(f":{e[1]}:", f"<a:{e[1]}:{e[2]}>")
    #print(msg2)
    if False and msg2 != msg and message.author.id!=388098902680928270 and message.author.id!=329639809524170755:
        print("Got")
        msg2 = msg2.replace("@", "")

        w=get_webhook(conn, (message.guild.id, message.channel.id))
        url = w[2]
        parts = url.split('/')
        webhook = Webhook.partial(parts[5],
                                  parts[6],
                                  adapter=RequestsWebhookAdapter())
        await message.delete()
        
        try:
            name = message.author.nick
        except:
            name = message.author.name
        if name == None:
            name = message.author.name

        webhook.send(msg2, username=name, avatar_url=message.author.avatar_url)
    
    if utils.kwargs(message.content, "--ms"):
        message.content = utils.kwargs(message.content, "--ms", ['remove'])
        a = datetime.datetime.now()
        await bot.process_commands(message)
        b = datetime.datetime.now()
        await message.channel.send(f"This command took {((b-a).total_seconds()*1000)}ms")
    else:
        await bot.process_commands(message)


bot.run(config.DISCORD_TOKEN)
stalkerBot.run(config.STALKER_TOKEN)