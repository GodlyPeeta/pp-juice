import discord
from discord.ext import commands
import asyncio
import sqlite3
from sqlite3 import Error
from discord.utils import get
from discord import Webhook, RequestsWebhookAdapter, File
from discord import *
import utils
import config
from discord.ext import tasks
import datetime

def delete_emote(conn, emote):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param discordID: id of the task
    :return:
    """
    sql = 'DELETE FROM emotes WHERE ename=? AND serverID=?'
    cur = conn.cursor()
    cur.execute(sql, emote)
    conn.commit()


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

def add_webhook(conn, arg):
    """
    Create a new project into the projects table
    :param conn:
    :param webhook:
    :return: user id
    """
    sql = ''' INSERT INTO webhooks(discordID, channelID, webhook)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    print(arg)
    cur.execute(sql, arg)
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

def add_emote(conn, arg):
    """
    Create a new project into the projects table
    :param conn:
    :param webhook:
    :return: user id
    """
    sql = ''' INSERT INTO emotes(serverID, ename, emoteID)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    print(arg)
    cur.execute(sql, arg)
    conn.commit()
    return cur.lastrowid


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


def deletewebhook(conn, webhook):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param webhook: id of the task
    :return:
    """
    sql = 'DELETE FROM webhooks WHERE discordID=? AND channelID=?'
    cur = conn.cursor()
    cur.execute(sql, webhook)
    conn.commit()


class cog:
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands

class command:
    def __init__(self, name, desc, usage, example, alias=None):
        self.name = name
        self.desc = desc
        self.usage = usage
        self.example = example
        self.alias = alias

osu = command("osu", "Finds info about a user's osu! profile", "pp.osu <name>", "pp.osu GodlyPeeta")
beatmap = command("beatmap", "Gives info about a certain beatmap\nView top scores on the map with `scores` after the command", "pp.beatmap <beatmap link>", "pp.beatmap https://osu.ppy.sh/b/2201460", "ob, bm")
pp = command("pp", "Finds how much a map is worth with given arguments", "pp.pp <link> <combo>x <miss>m <acc>% +<mods>", "pp.pp https://osu.ppy.sh/beatmapsets/798007#osu/1675844 69% +htEZ 420x 12m", "opp")
osuset = command("osuset", "Binds your profile to the bot, so you don't need to specify user for certain commands", "pp.osuset <osu username>", "pp.osuset GodlyPeeta")
top = command("top", "Finds the top 5 plays of a user", "pp.top <name>", "pp.top GodlyPeeta", "osutop, tp")
recent = command("recent", "Gives info on the most recent play of a user", "pp.recent <name>", "pp.recent GodlyPeeta", "ors, rs, rc")
leaderboard = command("leaderboard", "Shows the top players in the server", "pp.leaderboard", "pp.leaderboard", "lb")
strains = command("strains", "Renders a graph of the difficulty of parts of a map", "pp.strains <link>", "pp.strains https://osu.ppy.sh/b/1805627", "strain")
scores = command("scores", "Gets a user's top score on a map", "pp.scores <link> <name and/or mods>", "pp.scores https://osu.ppy.sh/beatmapsets/798007#osu/1675844 GodlyPeeta +dt", "sc, score")
multiresults = command("multiresults", "Gets the results of a multi lobby\nIf the round argument is not used, it will show the overall winners of every round. If it is used, it will show every play in the round", "pp.multiresults <match link or id> <round>", "pp.multiresults https://osu.ppy.sh/community/matches/69483825 3", "mr, multiresult")
recentbest = command("recentbest", "Gets the most recent play in an user's top X scores", "pp.recent best", "pp.recentbest GodlyPeeta 69", "rb")

osuCog = cog("osu!", [osu, pp, osuset, top, beatmap, recent, leaderboard, scores, strains, multiresults, recentbest])

osutrack = command("osutrack", "Alerts this channel whenever the user has set a top score within the limit (defauts to 50)", "pp.osutrack <osu username> <limit>", "pp.osutrack GodlyPeeta 50")
stoposutrack = command("stoposutrack", "Stops tracking the user", "pp.stoposutrack <osu username>", "pp.osutrack GodlyPeeta")
beatmaplink = command("beatmaplink", "When a user posts a beatmap link in a channel where this is enabled, the bot will send info about the map", "pp.beatmaplink <enable or disable>", "pp.beatmaplink enable")
mapfeed = command("mapfeed", "When a map gets ranked/loved/qualified, alert this channel (qualified also alerts for disqualified)", "pp.mapfeed <ranked/loved/qualified>", "pp.mapfeed ranked")
stopmapfeed = command("stopmapfeed", "Stops alerting the channel of ranked/loved/qualified maps", "pp.stopmapfeed <ranked/loved/qualified>", "pp.stopmapfeed ranked")

osuCog2 = cog("osu!channelstuff", [osutrack, stoposutrack, beatmaplink, mapfeed, stopmapfeed])

addwebhook = command("addwebhook", "adds a webhook to the channel (for animated emotes, pp.help addemote)", "pp.addwebhook <webhook url> <channelID>", "pp.addwebhook https://discordapp.com/api/webhooks/132123131/bbbbbbbbbbbbbbbbb 644268290474115075")
removewebhook = command("removewebhook", "Removes the webhook associated with this channel", "pp.removewebhook", "pp.removewebhook")
addemote = command("addemote", "Adds a animated emote that users without nitro can use(has to have a webhook in the channel)(get emote id with \\ :emote: or inspect element)", "pp.addemote <emote name> <emote id>", "pp.addemote spicy 752385471446908980")
help = command("help", "Find help about a given command", "pp.help <command name>", "pp.help help")
emotelist = command("emotelist", "Get a list of every animated emote given to the bot in this server, where each page has 10 emotes\n**(NOTE: Page starts at 0)**", "pp.emotelist <page number>", "pp.emotelist 1")
removeemote = command("removeemote", "Removes a emote from the server", "pp.removeemote <emote name>", "pp.removeemote spicy")

generalCog = cog("general", [help, addwebhook, removewebhook, addemote, emotelist, removeemote])

wpm = command("wpm", "Tests your words per minute by sending a bunch of words for you to type out (30 words at default, 75 max)", "pp.wpm <# of words>", "pp.wpm 40")
minesweeper = command("minesweeper", "Minesweeper (7x7 5 bombs by default)", "pp.minesweeper <# of bombs> <x> <y>", "pp.minesweeper 2 5 5")

randomCog = cog("random", [wpm, minesweeper])

ytadd = command('ytadd', 'Adds a youtube channel to track, when a new video comes out it will show up in the set channel. (if discord channelID field is empty, defaults to current channel)', 'pp.ytadd <channel link> <discord channelID>', 'pp.ytadd https://www.youtube.com/channel/UC1DCedRgGHBdm81E1llLhOQ 123123123')
ytdel = command('ytdel', 'Removes a channel from being tracked (if discord channelID field is empty, defaults to current channel)', 'pp.ytdel <channel link> <discord channelID>', 'pp.ytdel https://www.youtube.com/channel/UC1DCedRgGHBdm81E1llLhOQ')

ytCog = cog('youtube', [ytadd, ytdel])

cogs = [osuCog, osuCog2, randomCog, generalCog]

class GENERAL(commands.Cog):
    def __init__(self, bot):
        #self.chrllFeet.start()
        self.bot = bot
        self.curDate = 0

    @commands.command()
    async def addwebhook(self, ctx, webhook, channelID):
        channelID = int(channelID)
        f=False
        for i in ctx.guild.channels:
            print(i.id)
            if channelID == i.id:
                f=True
        if f == False:
            await ctx.send("not in this server")
            return
        if not (utils.has_admin(ctx.author) or utils.is_owner(ctx.author)):
            await ctx.send("You do not have enough permissions to do this (admin)")
            print("ERROR, Not a admin")
            return
        database = config.DB_PATH

        # create a database connection
        conn = create_connection(database)
        #try:
        add_webhook(conn, (ctx.guild.id, channelID, webhook))
        #except:
        #    await ctx.send("**webhook already added in this server (pp.removewebhook)**")
        #    return

        await ctx.send("**added webhook**")

    @commands.command()
    async def removewebhook(self, ctx):
        if not (utils.has_admin(ctx.author) or utils.is_owner(ctx.author)):
            await ctx.send("You do not have enough permissions to do this (admin)")
            print("ERROR, Not a admin")
            return
        database = config.DB_PATH

        # create a database connection
        conn = create_connection(database)
        try:
            deletewebhook(conn, (ctx.guild.id, ctx.channel.id))
        except:
            await ctx.send("**no webhook found**")
            return

        await ctx.send("**deleted webhook**")

    @commands.command()
    async def addemote(self, ctx, ename, emote):
        database = config.DB_PATH

        # create a database connection
        conn = create_connection(database)
        add_emote(conn, (ctx.guild.id, ename, emote))
        await ctx.send("added emote: "+ename)

    @commands.command()
    async def emotelist(self, ctx, page=0):
        database = config.DB_PATH

        # create a database connection
        conn = create_connection(database)

        u=self.bot.get_user(697244972914573473)
        w=get_webhook(conn, (ctx.guild.id, ctx.channel.id))
        url = w[2]
        parts = url.split('/')
        webhook = Webhook.partial(parts[5],
                                  parts[6],
                                  adapter=RequestsWebhookAdapter())
        
        el = get_all_emotes(conn, (ctx.guild.id,))
        #print(el)

        '''msg = await ctx.send("Test")
        await msg.add_reaction(emoji="◀️")
        await msg.add_reaction(emoji="▶️")'''

        desc = "Non discord nitro users can use these (Use pp.emotelist <list number> to navigate)\n\n"
        for i in range(page*10, page*10+10):
            try:
                desc+=f"<a:{el[i][1]}:{el[i][2]}>: **{el[i][1]}**\n"
            except:
                break
        embed = discord.Embed(title=f"Animated Emotes for {ctx.guild.name} (Page {page})", description=desc, color=0xff8ee6)
        webhook.send(embed=embed, username=u.name, avatar_url=u.avatar_url)
            

         



    @commands.command()
    async def removeemote(self, ctx, ename):
        database = config.DB_PATH

        # create a database connection
        conn = create_connection(database)
        delete_emote(conn, (ename, ctx.guild.id))
        await ctx.send(f"Emote {ename} has been removed")

    @commands.command()
    async def test(self, ctx):
        #495327409487478787
        channelb = self.bot.get_channel(495327409487478787)
        #await channelb.send('https://cdn.discordapp.com/attachments/644268290474115075/803800435039272980/unknown.png haha ur all slow')
        #logChannel = self.bot.get_channel(771776176359473152)
        return



    @commands.command()
    async def help(self, ctx, arg = None):
        if arg is None:
            desc = "Use `pp.help <command>` to find out more about any of these commands\n\n"
            for i in cogs:
                desc+=f"**{i.name}** - "
                for k in i.commands:
                    desc += f"`{k.name}` "
                desc+='\n'
            desc += "\nAdd this bot to your server with this [link](https://discord.com/oauth2/authorize?client_id=697244972914573473&scope=bot&permissions=0)"
            embed = discord.Embed(title=f"Commands for pp juice bot", url="https://www.youtube.com/watch?v=oHg5SJYRHA0",
                                  description=desc, color=0x9003fc)
            await ctx.send(embed=embed)
        else:
            desc = ""
            cmd=None
            for i in cogs:
                for k in i.commands:
                    if k.name == arg:
                        cmd=k
            if cmd is None:
                await ctx.send("Command not found")
                return
            desc+=(f"{cmd.desc}\n"
                   f"Use with: `{cmd.usage}`\n"
                   f"Example: `{cmd.example}`")
            embed = discord.Embed(title=f"How to use: {cmd.name}", url="https://www.youtube.com/watch?v=oHg5SJYRHA0",
                                  description=desc, color=0x9003fc)
            if cmd.alias is not None:
                embed.set_footer(text=f"Aliases: {cmd.alias}")
            await ctx.send(embed=embed)
    @tasks.loop(minutes = 60)
    async def chrllFeet(self):
        f = open("lib\chrllFeet.txt", "r")
        lastD = int(f.readline())
        date = int(f.readline())
        #print(f"{lastD} {date}")
        current_time = datetime.datetime.now()  
        if current_time.day != date:
            channelb = self.bot.get_channel(766524355898245131)
            fw = open("lib\chrllFeet.txt", "w")
            fw.write(f"{lastD+1}\n{current_time.day}")
            webhook2 = Webhook.partial(766347428923441173, '_crFnW3tNxYSCl6LkBfqwIZ33UT3XkzRgNXHKZ2r6qSXBVZoxopvvnYBW_weKDbpICOo', adapter=RequestsWebhookAdapter())
            #user = get(self.bot.get_all_members(), id=639545986884304896)
            #print(user)
            webhook2.send(f"day {lastD}: <@!158691947890868224> send feet pics", username = "epic chrll fan", avatar_url="https://cdn.discordapp.com/avatars/639545986884304896/c30d9061ab961adbeacf662a6fe6d6fe.png?size=128")
            await channelb.send(f"It has been {abs(130-lastD)} days since Hu Tao banner :)))))))")