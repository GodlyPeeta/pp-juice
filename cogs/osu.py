import ppcalc, asyncio, discord
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
msgcount = 2000
modDic = {0:'nm',
 1:'nf',
 2:'ez',
 4:'td',
 8:'hd',
 16:'hr',
 32:'sd',
 64:'dt',
 128:'rx',
 256:'ht',
 512:'nc',
 1024:'fl',
 4096:'so',
 16384:'pf'}

def add_plays(conn, plays):
    """
        update osuUsername
        :param conn:
        :param plays:
        :return: user id
        """
    sql = ' UPDATE osutrack\n                  SET plays= ?\n                  WHERE username = ? AND discordServerID = ?'
    cur = conn.cursor()
    cur.execute(sql, plays)
    conn.commit()


def add_pp(conn, plays):
    """
        update osuUsername
        :param conn:
        :param plays:
        :return: user id
        """
    sql = ' UPDATE osutrack\n                  SET pp= ?\n                  WHERE username = ?'
    cur = conn.cursor()
    cur.execute(sql, plays)
    conn.commit()


def add_rank(conn, plays):
    """
        update osuUsername
        :param conn:
        :param plays:
        :return: user id
        """
    sql = ' UPDATE osutrack\n                  SET rank= ?\n                  WHERE username = ?'
    cur = conn.cursor()
    cur.execute(sql, plays)
    conn.commit()


def get_user_osu(conn, discordID):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE discordID=?', (discordID,))
    rows = cur.fetchall()
    for row in rows:
        return row[1]


def get_allusers_osu(conn):
    """
    Query users by discordID
    :param conn: the Connection object
    :return: row
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    return rows


def get_osutrack_all(conn):
    """
        Query users by discordID
        :param conn: the Connection object        :return: row
        """
    cur = conn.cursor()
    cur.execute('SELECT * FROM osutrack')
    rows = cur.fetchall()
    return rows


def get_osutrack(conn, discordID):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM osutrack WHERE discordServerID=?', (discordID,))
    rows = cur.fetchall()
    return rows


def remove_osutrack(conn, discordID):
    """
    Query users by discordID
    :param conn: the Connection object
    :param discordID:
    :return: row
    """
    cur = conn.cursor()
    cur.execute('DELETE FROM osutrack WHERE username=? AND discordServerID=?', discordID)
    conn.commit()


def get_pp(conn, username):
    cur = conn.cursor()
    cur.execute('SELECT pp FROM osutrack WHERE username=?', (username,))
    rows = cur.fetchall()
    return rows[0][0]


def get_rank(conn, username):
    cur = conn.cursor()
    cur.execute('SELECT rank FROM osutrack WHERE username=?', (username,))
    rows = cur.fetchall()
    return rows[0][0]


def get_limit(conn, username):
    """
    Query users by discordID
    :param conn: the Connection object
    :param username:
    :return: row
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM osutrack WHERE username=?', (username,))
    rows = cur.fetchall()
    return rows[0]


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
        try:
            print(e)
        finally:
            e = None
            del e

    return conn


def create_user(conn, user):
    """
    Create a new project into the projects table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ' INSERT INTO users(discordID, osuUsername)\n              VALUES(?,?) '
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def track_user(conn, user):
    """
    Create a new project into the projects table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ' INSERT INTO osutrack(username, discordServerID, lmt)\n              VALUES(?,?,?) '
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def check_exists_track(conn, user):
    sql = 'SELECT EXISTS(SELECT 1 FROM osutrack WHERE username=?);'
    cur = conn.cursor()
    cur.execute(sql, user)
    res = cur.fetchall()
    print(res)
    return res


def get_servers_track(conn, username):
    cur = conn.cursor()
    cur.execute('SELECT discordServerID FROM osutrack WHERE username = ?', (username,))
    return cur.fetchall()[0][0]


def update_track(conn, user, discordServerID):
    cur = conn.cursor()
    serverID = f"{get_servers_track(conn, user)} {discordServerID}"
    print(serverID)
    cur.execute('UPDATE osutrack SET discordServerID = ? WHERE username = ?', (serverID, user))


def update_user(conn, user):
    """
    update osuUsername
    :param conn:
    :param user:
    :return: user id
    """
    sql = ' UPDATE users\n              SET osuUsername= ?\n              WHERE discordID = ?'
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()


def set_servers_track(conn, username, servers):
    cur = conn.cursor()
    cur.execute('UPDATE osutrack SET discordServerID = ? WHERE username = ?', (servers, username))


def getBeatmaps(arg, beatmap, i):
    beatmap[i] = api.get_beatmaps(arg)[0]


def getUser(arg, var, i):
    var[i] = api.get_user(arg)[0]


def get_user_pp(top, all, temp, i, id):
    try:
        b = api.get_user({'u': id})
        top[all[temp[i]][0]] = float(b[0]['pp_raw'])
    except Exception as e:
        try:
            print(e)
        finally:
            e = None
            del e


token = config.OSU_TOKEN[0]
api = ossapi(token)
apis = []
for i in config.OSU_TOKEN:
    apis.append(ossapi(i))

rankLinks = {'a':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/A_Rank.png',
 'b':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/B_Rank.png',
 'c':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/C_Rank.png',
 'd':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/D_Rank.png',
 'f':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/F_Rank.png',
 's':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/S_Rank.png',
 'ss':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/X_Rank.png',
 'x':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/X_Rank.png',
 'sh':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/SH_Rank.png',
 'ssh':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/XH_Rank.png',
 'xh':'https://raw.githubusercontent.com/LeaPhant/flowabot/master/emotes/XH_Rank.png'}
rankEmotes = {'a':'<:a_Rank:740827382168158289>',
 'b':'<:b_Rank:740827382121889832>',
 'c':'<:c_Rank:740827381912305686>',
 'd':'<:d_Rank:740827381912305755>',
 'f':'<:f_Rank:740827538359844874>',
 's':'<:s_Rank:740827382138667028>',
 'sh':'<:sh_Rank:740827382117826590>',
 'ss':'<:ss_Rank:740827382042329160>',
 'x':'<:ss_Rank:740827382042329160>',
 'ssh':'<:ssh_Rank:740827382285598730>',
 'xh':'<:ssh_Rank:740827382285598730>'}
modEmotes = {'ez':'<:ez:747573448707932210>',
 'ht':'<:ht:747573448754069514>',
 'nf':'<:nf:747573448850669759>',
 'hr':'<:hr:747573448640954419>',
 'dt':'<:dt:747573448452210849>',
 'nc':'<:nc:747573448863121519>',
 'hd':'<:hd:747573448833761420>',
 'fl':'<:fl:747573448737292368>',
 'so':'<:so:747573449047670934>'}

class OSU(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.msgflag = False
        self.osutracker.start()
        self.database = config.DB_PATH
        self.conn = create_connection(self.database)
        self.msgcount = 140000 - config.CUR_MESSAGE_COUNT
        self.cycle = 0

    def beatmaplinkembed(link):
        id = ''
        if link[:8] == 'https://':
            for i in range(len(link) - 1, 0, -1):
                if link[i] == '/':
                    break
                id = link[i] + id

        b = api.get_beatmaps({'b': id})
        b = b[0]
        status = int(b['approved'])
        if status == 4:
            status = 'Loved'
        else:
            if status == 3:
                status = 'Qualified'
            else:
                if status == 2:
                    status = 'Approved'
                else:
                    if status == 1:
                        status = 'Ranked'
                    else:
                        if status == 0:
                            status = 'Pending'
                        else:
                            if status == -1:
                                status = 'WIP'
                            else:
                                if status == -2:
                                    status = 'Graveyard'
                                else:
                                    status = 'Graveyard'
        url = 'https://osu.ppy.sh/osu/' + id
        urllib.request.urlretrieve(url, 'lib/map.txt')
        desc = f"**Map length:** {time.strftime('%M:%S', time.gmtime(int(b['total_length'])))} **BPM: **{b['bpm']} **Combo:** {b['max_combo']}\n**CS:** {b['diff_size']} **OD:** {b['diff_overall']} **AR:** {b['diff_approach']} **HP:** {b['diff_drain']}\n\n**90%** - {ppcalc.ppcalculate(90, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **95%** - {ppcalc.ppcalculate(95, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **97%** - {ppcalc.ppcalculate(97, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} \n**98%** - {ppcalc.ppcalculate(98, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **99%** - {ppcalc.ppcalculate(99, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **100%** - {ppcalc.ppcalculate(100, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]}"
        embed = discord.Embed(title=f"{b['title']} **[{b['version']}]** {round(float(b['difficultyrating']), 2)}★",
            description=desc,
            url=f"https://osu.ppy.sh/b/{id}",
            color=16748262)
        embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{b['beatmapset_id']}l.jpg")
        if b['approved_date'] == None:
            embed.set_footer(text=f"▶ {b['playcount']}  ❤ {b['favourite_count']} | Not approved | Mapped by {b['creator']}", icon_url=f"http://s.ppy.sh/a/{b['creator_id']}")
        else:
            embed.set_footer(text=f"▶ {b['playcount']}  ❤ {b['favourite_count']} | {status} on {b['approved_date'][:10]} | Mapped by {b['creator']}", icon_url=f"http://s.ppy.sh/a/{b['creator_id']}")
        return embed

    @commands.command()
    async def osuset(self, ctx, user=None):
        database = config.DB_PATH
        conn = create_connection(database)
        if user is None:
            try:
                update_user(conn, (None, ctx.author.id))
            except:
                await ctx.send('sync your profile with `pp.osuset osuUsername`')
                return
            await ctx.send('unsynced your profile')
            return

        try:
            create_user(conn, (ctx.author.id, user))
        except:
            update_user(conn, (user, ctx.author.id))

        await ctx.send(ctx.author.name + "'s osu! profile has been set to " + user)

    @commands.command()
    async def osu(self, ctx, user=None):
        database = config.DB_PATH
        conn = create_connection(database)
        if user is None:
            try:
                user = get_user_osu(conn, ctx.author.id)
            except:
                await ctx.send('user has not set a profile (`pp.osuset osuUsername`)')
                return

        p = api.get_user({'u': user})
        if p == []:
            await ctx.send('cannot find user')
            return
        p = p[0]
        desc2 = f"**Ranked Score: ** {int(p['ranked_score']):,} \n**Hit Accuracy: ** {round(float(p['accuracy']), 2)}% \n**Play Count:   ** {int(p['playcount']):,}\n\n"
        embed = discord.Embed(title=f"{p['username']} :flag_{p['country'].lower()}:", url=('https://osu.ppy.sh/u/' + p['user_id']),
          description=desc2,
          color=16748262)
        embed.add_field(name='Play Time', value=f"{round(int(p['total_seconds_played']) / 3600 / 24, 1)} Days", inline=True)
        embed.add_field(name='pp', value=(f"{p['pp_raw']}"), inline=True)
        embed.add_field(name=f"{rankEmotes['ssh']}: {p['count_rank_ssh']} {rankEmotes['ss']}: {p['count_rank_ss']}", value=f"**{rankEmotes['s']}: {p['count_rank_s']} {rankEmotes['sh']}: {p['count_rank_sh']} {rankEmotes['a']}: {p['count_rank_a']}**",
          inline=True)
        embed.set_thumbnail(url=('http://a.ppy.sh/' + p['user_id']))
        embed.set_footer(text=f"Rank {p['pp_rank']} ({p['country']}: {p['pp_country_rank']})")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['bm', 'ob'])
    async def beatmap(self, ctx, arg, scores=''):
        id = ''
        if arg[:8] == 'https://':
            for i in range(len(arg) - 1, 0, -1):
                if arg[i] == '/':
                    break
                id = arg[i] + id
        else:
            await ctx.send("No map found")
            return
        #else:
        b = api.get_beatmaps({'b': id})
        b = b[0]
        status = int(b['approved'])
        if status == 4:
            status = 'Loved'
        else:
            if status == 3:
                status = 'Qualified'
            else:
                if status == 2:
                    status = 'Approved'
                else:
                    if status == 1:
                        status = 'Ranked'
                    else:
                        if status == 0:
                            status = 'Pending'
                        else:
                            if status == -1:
                                status = 'WIP'
                            else:
                                if status == -2:
                                    status = 'Graveyard'
        url = 'https://osu.ppy.sh/osu/' + id
        urllib.request.urlretrieve(url, 'lib/map.txt')
        desc = f"**Mapped by** {b['creator']}, **Song by** {b['artist']}\n**[{b['version']}]** {round(float(b['difficultyrating']), 2)}★ **Aim:** {round(float(b['diff_aim']), 2)} **Speed:** {round(float(b['diff_speed']), 2)}\n**Map length:** {time.strftime('%M:%S', time.gmtime(int(b['total_length'])))} **BPM: **{b['bpm']} **Combo:** {b['max_combo']}\n**CS:** {b['diff_size']} **OD:** {b['diff_overall']} **AR:** {b['diff_approach']} **HP:** {b['diff_drain']}\n\n**90%** - {ppcalc.ppcalculate(90, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **95%** - {ppcalc.ppcalculate(95, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **97%** - {ppcalc.ppcalculate(97, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} \n**98%** - {ppcalc.ppcalculate(98, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **99%** - {ppcalc.ppcalculate(99, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]} | **100%** - {ppcalc.ppcalculate(100, int(b['max_combo']), 0, '', 'lib/map.txt', False)[0]}"
        embed = discord.Embed(title=(f"{b['title']}"),
          description=desc,
          url=f"https://osu.ppy.sh/b/{id}",
          color=16748262)
        embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{b['beatmapset_id']}l.jpg")
        embed.set_image(url=f"https://assets.ppy.sh/beatmaps/{b['beatmapset_id']}/covers/cover.jpg")
        embed.set_footer(text=f"▶ {b['playcount']}  ❤ {b['favourite_count']} | {status} on {b['approved_date'][:10]}", icon_url=f"http://s.ppy.sh/a/{b['creator_id']}")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['opp'])
    async def pp(self, ctx, arg, *arg2):
        id = ''
        if arg[:8] == 'https://':
            for i in range(len(arg) - 1, 0, -1):
                if arg[i] == '/':
                    break
                id = arg[i] + id

        #else:
        print(id)
        b = api.get_beatmaps({'b': id})
        b = b[0]
        acc = 100
        combo = b['max_combo']
        misses = 0
        mods = ''
        link = 'https://osu.ppy.sh/osu/' + id
        for i in arg2:
            if i[0] == '+':
                mods = i[1:].upper()
            elif i[-1:] == '%':
                acc = float(i[:-1])
            elif i[-1:] == 'm':
                misses = int(i[:-1])
            else:
                if i[-1:] == 'x':
                    combo = int(i[:-1])
        
        #print(mods)
        #print(acc)
        #print(combo)

        pp = ppcalc.ppcalculate(float(acc), int(combo), int(misses), mods, link)
        difficultyMods = []
        hasHidden = False
        modsStr = ''
        for i in range(0, len(mods) - 1):
            if mods[i] == 'H':
                if mods[(i + 1)] == 'D':
                    hasHidden = True
                    modsStr += modEmotes['hd']
            if mods[i] == 'F':
                if mods[(i + 1)] == 'L':
                    hasHidden = True
                    modsStr += modEmotes['fl']
            if mods[i] == 'H':
                if mods[(i + 1)] == 'R':
                    difficultyMods.append('hr')
                    modsStr += modEmotes['hr']
                if mods[(i + 1)] == 'T':
                    difficultyMods.append('ht')
                    modsStr += modEmotes['ht']
            
            if mods[i] == 'D':
                if mods[(i + 1)] == 'T':
                    difficultyMods.append('dt')
                    modsStr += modEmotes['dt']
            if mods[i] == 'N':
                if mods[(i + 1)] == 'C':
                    difficultyMods.append('dt')
                    modsStr += modEmotes['nc']
                if mods[(i + 1)] == 'F':
                    modsStr += modEmotes['nf']
            if mods[i] == 'E' and mods[(i + 1)] == 'Z':
                difficultyMods.append('ez')
                modsStr += modEmotes['ez']
            if mods[i] == 'S' and mods[(i + 1)] == 'O':
                modsStr += modEmotes['so']
        print(modsStr)
        print(difficultyMods)
        if mods == '':
            mods = 'NM'
            modsStr = 'None'
        
        if not hasHidden or acc == 100 or acc == 0:
            rankLink = rankLinks['ssh']
        else:
            pass
        if hasHidden and acc >= 93 and misses == 0:
            rankLink = rankLinks['sh']
        else:
            if acc == 100 or acc == 0:
                rankLink = rankLinks['ss']
            else:
                if acc >= 93 and misses == 0:
                    rankLink = rankLinks['s']
                else:
                    if not acc > 90 or misses == 0 or acc > 93:
                        rankLink = rankLinks['a']
                    else:
                        if not acc > 80 or misses == 0 or acc > 85:
                            rankLink = rankLinks['b']
                        else:
                            if acc > 70:
                                rankLink = rankLinks['c']
                            else:
                                rankLink = rankLinks['d']
                                    
        status = int(b['approved'])
        if status == 4:
            status = 'Loved'
        else:
            if status == 3:
                status = 'Qualified'
            else:
                if status == 2:
                    status = 'Approved'
                else:
                    if status == 1:
                        status = 'Ranked'
                    else:
                        if status == 0:
                            status = 'Pending'
                        else:
                            if status == -1:
                                status = 'WIP'
                            else:
                                if status == -2:
                                    status = 'Graveyard'
        if difficultyMods:
            print('sdauijfhdufhgudf')
            sr = round(float(b['difficultyrating']), 2)
            sa = round(float(b['diff_aim']), 2)
            ss = round(float(b['diff_speed']), 2)
            length = int(b['total_length'])
            bpm = float(b['bpm'])
            cs = b['diff_size']
            od = b['diff_overall']
            ar = b['diff_approach']
            hp = float(b['diff_drain'])
            sr = pp[6] + f"({sr})"
            sa = pp[4] + f"({sa})"
            ar = pp[1] + f"({ar})"
            od = pp[3] + f"({od})"
            for i in difficultyMods:
                if i == 'hr':
                    cs = pp[2] + f"({cs})"
                    hp = str(round(hp * 1.4, 2)) + f"({hp})"
                if i == 'dt':
                    ss = pp[5] + f"({ss})"
                    length = time.strftime('%M:%S', time.gmtime(length / 1.5)) + f"({time.strftime('%M:%S', time.gmtime(length))})"
                    bpm = str(round(bpm * 1.5, 2)) + f"({bpm})"
                if i == 'ez':
                    cs = pp[2] + f"({cs})"
                    hp = str(round(hp * 0.5, 2)) + f"({hp})"
                if i == 'ht':
                    ss = pp[5] + f"({ss})"
                    length = time.strftime('%M:%S', time.gmtime(length / 0.75)) + f"({time.strftime('%M:%S', time.gmtime(length))})"
                    bpm = str(round(bpm * 0.75, 2)) + f"({bpm})"

            desc = f"**Mapped by** {b['creator']}, **Song by** {b['artist']}\n**[{b['version']}]** {sr}★ \n**Aim:** {sa} **Speed:** {ss}\n**Map length:** {time.strftime('%M:%S', time.gmtime(int(b['total_length'])))} **BPM: **{bpm}"
            embed = discord.Embed(title=(b['title']), url=('https://osu.ppy.sh/b/' + id), description=desc, color=16748262)
            embed.set_author(name=(str(pp[0]) + ' pp'), icon_url=rankLink)
            embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{b['beatmapset_id']}l.jpg")
            embed.set_image(url=f"https://assets.ppy.sh/beatmaps/{b['beatmapset_id']}/covers/cover.jpg")
            embed.add_field(name='Accuracy', value=f"{acc}%", inline=True)
            embed.add_field(name='Misses', value=(f"{misses}"), inline=True)
            embed.add_field(name='Combo ', value=f"{combo}x", inline=True)
            embed.add_field(name='Mods ', value=('' + modsStr), inline=True)
            embed.add_field(name=f"CS: {cs} OD: {od}", value=f"**AR: {ar} HP: {hp}**",
                inline=True)
            embed.set_footer(text=f"▶ {b['playcount']}  ❤ {b['favourite_count']} | {status}", icon_url=f"http://s.ppy.sh/a/{b['creator_id']}")
            await ctx.send(embed=embed)
        else:
            desc = f"**Mapped by** {b['creator']}, **Song by** {b['artist']}\n**[{b['version']}]** {round(float(b['difficultyrating']), 2)}★ **Aim:** {round(float(b['diff_aim']), 2)} **Speed:** {round(float(b['diff_speed']), 2)}\n**Map length:** {time.strftime('%M:%S', time.gmtime(int(b['total_length'])))} **BPM: **{b['bpm']}"
            embed = discord.Embed(title=(b['title']), url=('https://osu.ppy.sh/b/' + id), description=desc, color=16748262)
            embed.set_author(name=(str(pp[0]) + ' pp'), icon_url=rankLink)
            embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{b['beatmapset_id']}l.jpg")
            embed.set_image(url=f"https://assets.ppy.sh/beatmaps/{b['beatmapset_id']}/covers/cover.jpg")
            embed.add_field(name='Accuracy', value=f"{acc}%", inline=True)
            embed.add_field(name='Misses', value=(f"{misses}"), inline=True)
            embed.add_field(name='Combo ', value=f"{combo}x", inline=True)
            embed.add_field(name='Mods ', value=('' + modsStr), inline=True)
            embed.add_field(name=f"CS: {b['diff_size']} OD: {b['diff_overall']}", value=f"**AR: {b['diff_approach']} HP: {b['diff_drain']}**",
                inline=True)
            embed.set_footer(text=f"▶ {b['playcount']}  ❤ {b['favourite_count']} | {status}", icon_url=f"http://s.ppy.sh/a/{b['creator_id']}")
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['osutop', 'tp'])
    async def top(self, ctx, user=None, arg=None, num=5):
        database = config.DB_PATH
        conn = create_connection(database)
        numOfPlays = 5
        if user is None:
            try:
                user = get_user_osu(conn, ctx.author.id)
            except:
                await ctx.send('user has not set a profile (`pp.osuset osuUsername`)')
                return

        if arg == '-g':
            t = api.get_user_best({'u':user,  'limit':100})
            if float(t[0]['pp']) <= num:
                await ctx.send(f"{user} has no plays worth more than {num}pp, what a noob")
                return
            for p in range(len(t)):
                if float(t[p]['pp']) <= num:
                    await ctx.send(f"{user} has {p} plays that are worth more than {num}pp")
                    return

            await ctx.send(f"{user} has at least 100 plays that are worth more than {num}pp")
            return
        print('a')
        t = api.get_user_best({'u':user,  'limit':numOfPlays})
        p = api.get_user({'u': user})
        try:
            p = p[0]
        except:
            await ctx.send('User not found')
            return
        else:
            desc = ''
            print('B')
            beatmaps = [None, None, None, None, None]
            threadList = []
            for i in range(5):
                b = t[i]
                modsDiffInt = 0
                if int(b['enabled_mods']) != 0:
                    mods = bitwiseEnum.findCombo(modDic, int(b['enabled_mods']), [])
                    modsStr = '| '
                    for m in mods:
                        if m == 'dt':
                            modsDiffInt += 64
                        elif m == 'ez':
                            modsDiffInt += 2
                        elif m == 'hr':
                            modsDiffInt += 16
                        else:
                            if m == 'nc':
                                modsDiffInt += 64

                threadList.append(threading.Thread(target=getBeatmaps, args=({'b':b['beatmap_id'],  'mods':modsDiffInt,  'limit':1}, beatmaps, i)))

            print('C')
            for i in threadList:
                i.start()

            for i in threadList:
                i.join()

            print('D')
            for i in range(0, numOfPlays):
                b = t[i]
                if int(b['enabled_mods']) == 0:
                    modsStr = ''
                else:
                    mods = bitwiseEnum.findCombo(modDic, int(b['enabled_mods']), [])
                    modsStr = '| '
                    for m in reversed(mods):
                        try:
                            modsStr += modEmotes[m]
                        except:
                            print('ah fuck')

                beatmap = beatmaps[i]
                print(modsStr)
                acc = (50 * int(b['count50']) + 100 * int(b['count100']) + 300 * int(b['count300'])) / (300 * (int(b['countmiss']) + int(b['count100']) + int(b['count50']) + int(b['count300'])))
                desc += f"**{i + 1}. [{beatmap['title']}](https://osu.ppy.sh/b/{beatmap['beatmap_id']}) \n[{beatmap['version']}] {round(float(beatmap['difficultyrating']), 2)}★**\n{rankEmotes[b['rank'].lower()]} **{round(float(b['pp']), 2)}pp** | {round(acc * 100, 2)}% **{modsStr} **\n{b['score']} **|** {b['maxcombo']}/{beatmap['max_combo']} **|** [{b['count300']}/{b['count100']}/{b['count50']}/{b['countmiss']}]\nScore set on {b['date']}\n"

            embed = discord.Embed(title=f":flag_{p['country'].lower()}: {p['username']}'s Top Plays",
              description=desc,
              url=f"https://osu.ppy.sh/u/{p['user_id']}",
              color=16748262)
            embed.set_thumbnail(url=('http://a.ppy.sh/' + p['user_id']))
            print('E')
        try:
            await ctx.send(embed=embed)
        except:
            await ctx.send('Too many for discord api to send :c')

    @commands.command()
    async def osutracklist(self, ctx):
        database = config.DB_PATH
        conn = create_connection(database)
        row = get_osutrack(conn, ctx.channel.id)
        desc = ''
        for i in row:
            desc += f"`{i[0]}` "

        embed = discord.Embed(title=f"Tracking list for this channel of {ctx.guild.name}",
          description=desc,
          color=16748262)
        await ctx.send(embed=embed)

    @commands.command()
    async def osutrack(self, ctx, user=None, limit=50):
        if not utils.has_admin(ctx.author):
            if not utils.is_owner(ctx.author):
                await ctx.send('You do not have enough permissions to do this (admin)')
                print('ERROR, Not a admin')
                return
        database = config.DB_PATH
        conn = create_connection(database)
        if user is None:
            try:
                user = get_user_osu(conn, ctx.author.id)
            except:
                await ctx.send('user has not set a profile')
                return

        user = user.lower()
        if check_exists_track(self.conn, (user,))[0][0] == 0:
            track_user(conn, (user, ctx.channel.id, limit))
        else:
            update_track(self.conn, user, ctx.channel.id)
        await ctx.send('Now tracking ' + user)

    @commands.command(pass_context=True, aliases=['strain'])
    async def strains(self, ctx, beatmapID):
        id = ''
        if beatmapID[:8] == 'https://':
            for i in range(len(beatmapID) - 1, 0, -1):
                if beatmapID[i] == '/':
                    break
                id = beatmapID[i] + id

        b = api.get_beatmaps({'b': id})[0]
        f = open('mapdata.txt', 'wb')
        f.write(requests.get('https://osu.ppy.sh/osu/' + id).text.encode('utf-8'))
        f2 = strain.graph('mapdata.txt', b['title'])
        await ctx.send(file=discord.File(f2, filename='file.png'))

    @commands.command()
    async def beatmaplink(self, ctx, arg):
        if not utils.has_admin(ctx.author):
            if not utils.is_owner(ctx.author):
                await ctx.send('You do not have enough permissions to do this (admin)')
                print('ERROR, Not a admin')
                return
        if arg == 'enable':
            try:
                utils.enable_beatmap_link(self.conn, ctx.channel.id)
                await ctx.send('Enabled')
            except Exception as e:
                try:
                    await ctx.send(str(e))
                finally:
                    e = None
                    del e

        else:
            if arg == 'disable':
                try:
                    utils.disable_beatmap_link(self.conn, ctx.channel.id)
                    await ctx.send('Disabled')
                except Exception as e:
                    try:
                        await ctx.send(str(e))
                    finally:
                        e = None
                        del e

    @commands.command()
    async def stoposutrack(self, ctx, user=None):
        if not utils.has_admin(ctx.author):
            if not utils.is_owner(ctx.author):
                await ctx.send('You do not have enough permissions to do this (admin)')
                print('ERROR, Not a admin')
                return
        if user is None:
            try:
                user = get_user_osu(self.conn, ctx.author.id)
            except:
                await ctx.send('user has not set a profile')
                return

        lst = get_servers_track(self.conn, user).split()
        if len(lst) == 1:
            remove_osutrack(self.conn, (user, ctx.channel.id))
        else:
            set_servers_track(self.conn, user, get_servers_track(self.conn, user).replace(str(ctx.channel.id), ''))
        await ctx.send('Stopped tracking ' + user)

    @commands.command(pass_context=True, aliases=['sc', 'score'])
    async def scores(self, ctx, beatmapID, user=None):
        database = config.DB_PATH
        conn = create_connection(database)
        id = ''
        if beatmapID[:8] == 'https://':
            for i in range(len(beatmapID) - 1, 0, -1):
                if beatmapID[i] == '/':
                    break
                id = beatmapID[i] + id

        if user is None:
            try:
                user = get_user_osu(conn, ctx.author.id)
            except:
                await ctx.send('user has not set a profile (`pp.osuset osuUsername`)')
                return

        try:
            r = api.get_scores({'b':id,  'u':user})[0]
        except:
            await ctx.send('**user has not passed this map**')
            return

        b = api.get_beatmaps({'b': id})[0]
        if int(r['enabled_mods']) == 0:
            modsStr = ''
        else:
            mods = bitwiseEnum.findCombo(modDic, int(r['enabled_mods']), [])
            modsStr = ''
            print(mods)
            for i in mods:
                try:
                    modsStr += modEmotes[i]
                except:
                    print('ah fuck')

        print(modsStr)
        url = 'https://osu.ppy.sh/osu/' + b['beatmap_id']
        urllib.request.urlretrieve(url, 'lib/map.txt')
        acc = (50 * int(r['count50']) + 100 * int(r['count100']) + 300 * int(r['count300'])) / (300 * (int(r['countmiss']) + int(r['count100']) + int(r['count50']) + int(r['count300'])))
        if r['perfect'] == '0':
            fc = f"(FC: {ppcalc.ppcalculate(acc * 100, int(b['max_combo']), 0, modsStr, 'lib/map.txt', False)[0]})"
        else:
            fc = ''
        ppc = ppcalc.ppcalculate(acc * 100, int(r['maxcombo']), int(r['countmiss']), modsStr, 'lib/map.txt', False)
        completed = ''
        if r['rank'] == 'F':
            completed = f"\nCompleted: {round((int(r['count50']) + int(r['count100']) + int(r['count300']) + int(r['countmiss'])) / (int(b['count_normal']) + int(b['count_slider']) + int(b['count_spinner'])) * 100, 2)}%"
        desc = f"[[{b['version']}][{ppc[6]}★]](https://osu.ppy.sh/b/{b['beatmap_id']}){modsStr}\n\n**{ppc[0]}pp** {fc} | {round(acc * 100, 2)}%\n{int(r['score']):,} | {r['maxcombo']}/{b['max_combo']} | [{r['count300']}/{r['count100']}/{r['count50']}/{r['countmiss']}]{completed}\n\n__**Beatmap Info:**__\n**BPM: **{int(float(b['bpm']) * ppc[7])} **Length:** {time.strftime('%M:%S', time.gmtime(round(int(b['total_length']) / ppc[7], 0)))}\n **CS:** {ppc[2]} **OD: **{ppc[3]} **AR: **{ppc[1]} **HP: **{ppc[8]}"
        embed = discord.Embed(title=(f"{b['title']}"), url=('https://osu.ppy.sh/b/' + b['beatmap_id']), description=desc, color=16748262)
        rankLink = rankLinks[r['rank'].lower()]
        status = int(b['approved'])
        if status == 4:
            status = 'Loved'
        else:
            if status == 3:
                status = 'Qualified'
            else:
                if status == 2:
                    status = 'Approved'
                else:
                    if status == 1:
                        status = 'Ranked'
                    else:
                        if status == 0:
                            status = 'Pending'
                        else:
                            if status == -1:
                                status = 'WIP'
                            else:
                                if status == -2:
                                    status = 'Graveyard'
        embed.set_thumbnail(url=f"http://s.ppy.sh/a/{r['user_id']}")
        embed.set_image(url=f"https://assets.ppy.sh/beatmaps/{b['beatmapset_id']}/covers/cover.jpg")
        embed.set_author(name=f"Top play of {user} on {b['title']}", icon_url=rankLink)
        embed.set_footer(text=f"▶ {b['playcount']}  ❤ {b['favourite_count']} | {status} | Score set on {r['date']}", icon_url=f"http://s.ppy.sh/a/{b['creator_id']}")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['lb'])
    async def leaderboard(self, ctx):
        database = config.DB_PATH
        conn = create_connection(database)
        all = get_allusers_osu(conn)
        top = {}
        memberIDs = []
        for i in ctx.guild.members:
            memberIDs.append(i.id)

        temp = []
        for i in range(len(all)):
            if all[i][0] in memberIDs:
                try:
                    temp.append(i)
                    top[all[i][0]] = 0
                except Exception as e:
                    try:
                        print(e)
                        continue
                    finally:
                        e = None
                        del e

        print(temp)
        print(top)
        print(all)
        threadList = []
        for i in range(len(temp)):
            threadList.append(threading.Thread(target=get_user_pp, args=(top, all, temp, i, all[temp[i]][1])))

        for i in threadList:
            i.start()

        for i in threadList:
            i.join()

        print(top)
        top = {k:v for k, v in sorted((top.items()), key=(lambda item: item[1]), reverse=True)}
        values = []
        items = []
        for i in top:
            values.append(top[i])
            items.append(i)

        desc = ''
        for i in range(len(top)):
            osuName = get_user_osu(conn, items[i])
            desc += f"{i + 1}. **[{osuName}](https://osu.ppy.sh/u/{osuName})** - {values[i]}pp\n"
            if i == 8:
                break

        embed = discord.Embed(title=f"Leaderboard for {ctx.guild.name}", description=desc, color=16748262)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['ors', 'rs', 'rc'])
    async def recent(self, ctx, user=None):
        database = config.DB_PATH
        conn = create_connection(database)
        if user is None:
            try:
                user = get_user_osu(conn, ctx.author.id)
            except:
                await ctx.send('user has not set a profile')
                return

        
        r = api.get_user_recent({'u': user})
        if not r:
            await ctx.send('cannot find user, or user has not set a score in the last 24hrs')
            return
        r = r[0]
        b = api.get_beatmaps({'b': r['beatmap_id']})[0]
        if int(r['enabled_mods']) == 0:
            modsStr = ''
        else:
            mods = bitwiseEnum.findCombo(modDic, int(r['enabled_mods']), [])
            modsStr = ''
            print(mods)
            for i in mods:
                try:
                    modsStr += modEmotes[i]
                except:
                    print('ah fuck')

        url = 'https://osu.ppy.sh/osu/' + r['beatmap_id']
        urllib.request.urlretrieve(url, 'lib/map.txt')
        acc = (50 * int(r['count50']) + 100 * int(r['count100']) + 300 * int(r['count300'])) / (300 * (int(r['countmiss']) + int(r['count100']) + int(r['count50']) + int(r['count300'])))
        if r['perfect'] == '0':
            fc = f"(FC: {ppcalc.ppcalculate(acc * 100, int(b['max_combo']), 0, modsStr, 'lib/map.txt', False)[0]})"
        else:
            fc = ''
        ppc = ppcalc.ppcalculate(acc * 100, int(r['maxcombo']), int(r['countmiss']), modsStr, 'lib/map.txt', False)
        completed = ''
        if r['rank'] == 'F':
            completed = f"\nCompleted: {round((int(r['count50']) + int(r['count100']) + int(r['count300']) + int(r['countmiss'])) / (int(b['count_normal']) + int(b['count_slider']) + int(b['count_spinner'])) * 100, 2)}%"
        desc = f"[[{b['version']}][{ppc[6]}★]](https://osu.ppy.sh/b/{b['beatmap_id']}){modsStr}\n\n**{ppc[0]}pp** {fc} | {round(acc * 100, 2)}%\n{int(r['score']):,} | {r['maxcombo']}/{b['max_combo']} | [{r['count300']}/{r['count100']}/{r['count50']}/{r['countmiss']}]{completed}\n\n__**Beatmap Info:**__\n**BPM: **{int(float(b['bpm']) * ppc[7])} **Length:** {time.strftime('%M:%S', time.gmtime(round(int(b['total_length']) / ppc[7], 0)))}\n **CS:** {ppc[2]} **OD: **{ppc[3]} **AR: **{ppc[1]} **HP: **{ppc[8]}"
        embed = discord.Embed(title=(f"{b['title']}"), url=('https://osu.ppy.sh/b/' + b['beatmap_id']), description=desc, color=16748262)
        rankLink = rankLinks[r['rank'].lower()]
        status = int(b['approved'])
        if status == 4:
            status = 'Loved'
        else:
            if status == 3:
                status = 'Qualified'
            else:
                if status == 2:
                    status = 'Approved'
                else:
                    if status == 1:
                        status = 'Ranked'
                    else:
                        if status == 0:
                            status = 'Pending'
                        else:
                            if status == -1:
                                status = 'WIP'
                            else:
                                if status == -2:
                                    status = 'Graveyard'
        embed.set_thumbnail(url=f"http://s.ppy.sh/a/{r['user_id']}")
        embed.set_image(url=f"https://assets.ppy.sh/beatmaps/{b['beatmapset_id']}/covers/cover.jpg")
        embed.set_author(name=f"Most Recent Play for {user}", icon_url=rankLink)
        embed.set_footer(text=f"▶ {b['playcount']}  ❤ {b['favourite_count']} | {status} | Score set on {r['date']}", icon_url=f"http://s.ppy.sh/a/{b['creator_id']}")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['mr', 'multiresult'])
    async def multiresults(self, ctx, beatmapID, round=None):
        id = ''
        try:
            id = int(beatmapID)
        except:
            for i in range(len(beatmapID) - 1, 0, -1):
                if beatmapID[i] == '/':
                    break
                id = beatmapID[i] + id

        print(id)
        m = api.get_match({'mp': id})
        if round == None:
            desc = ''
            blueScore = 0
            redScore = 0
            for i in m['games']:
                if int(i['team_type']) == 2:
                    red = 0
                    blue = 0
                    for s in i['scores']:
                        if int(s['team']) == 1:
                            blue += int(s['score'])
                        else:
                            red += int(s['score'])

                if red > blue:
                    desc += f"\n:red_circle: __**`{red}`**__ | `{blue}` :black_circle: [red wins!](https://osu.ppy.sh/b/{i['beatmap_id']})"
                    redScore += 1
                else:
                    desc += f"\n:black_circle: `{red}` | __**`{blue}`**__ :blue_circle: [blue wins!](https://osu.ppy.sh/b/{i['beatmap_id']})"
                    blueScore += 1

            e = discord.Embed(title=f"Results of {m['match']['name']}", url=f"https://osu.ppy.sh/community/matches/{id}", description=desc)
            footerText = ''
            if blueScore != 0 or redScore != 0:
                footerText += f"teamVS: {redScore} - {blueScore}"
            e.set_footer(text=footerText)
            await ctx.send(embed=e)
        else:
            g = m['games'][(int(round) - 1)]
            b = [{'temp': ''}]
            users = []
            threadList = []
            threadList.append(threading.Thread(target=getBeatmaps, args=({'b': g['beatmap_id']}, b, 0)))
            for i in range(len(g['scores'])):
                users.append('')
                threadList.append(threading.Thread(target=getUser, args=({'u': g['scores'][i]['user_id']}, g['scores'][i], 'user_info')))

            for i in threadList:
                i.start()

            for i in threadList:
                i.join()

            b = b[0]
            maxLen = 4
            scoreLen = 5
            comboLen = 5
            for s in g['scores']:
                if len(s['user_info']['username']) > maxLen:
                    maxLen = len(s['user_info']['username'])

            for s in g['scores']:
                s['num_score'] = s['score']
                s['score'] = f"{int(s['score']):,}"
                if len(s['score']) > scoreLen:
                    scoreLen = len(s['score'])

            for s in g['scores']:
                if len(s['maxcombo']) > comboLen:
                    comboLen = len(s['score'])

        if int(g['team_type']) == 2:
            descRed = ''
            descBlue = ''
            redScore = 0
            blueScore = 0
            for s in g['scores']:
                name = s['user_info']['username']
                for i in range(maxLen - len(s['user_info']['username'])):
                    name += ' '

                combo = s['maxcombo'] + 'x'
                for i in range(comboLen - len(s['maxcombo'])):
                    combo = ' ' + combo

                score = s['score']
                for i in range(scoreLen - len(s['score'])):
                    score = ' ' + score

                print(g['mods'])
                if int(g['mods']) == 0:
                    modsStr = ''
                    mods = bitwiseEnum.findCombo(modDic, int(s['enabled_mods']), [])
                    for i in mods:
                        try:
                            modsStr += modEmotes[i]
                        except:
                            print('ah fuck')

                else:
                    mods = bitwiseEnum.findCombo(modDic, int(g['mods']), [])
                    modsStr = ''
                    for i in mods:
                        try:
                            modsStr += modEmotes[i]
                        except:
                            print('ah fuck')

                acc = str((50 * int(s['count50']) + 100 * int(s['count100']) + 300 * int(s['count300'])) / (300 * (int(s['countmiss']) + int(s['count100']) + int(s['count50']) + int(s['count300']))) * 100)[:5]
                if int(s['team']) == 1:
                    blueScore += int(s['num_score'])
                    descBlue += f":blue_circle: :flag_{s['user_info']['country'].lower()}: [`{name}`](https://osu.ppy.sh/u/{s['user_info']['username'].replace(' ', '%20')}) `{score} {combo}  {acc}%` {modsStr}\n"
                else:
                    redScore += int(s['num_score'])
                    descBlue += f":red_circle: :flag_{s['user_info']['country'].lower()}: [`{name}`](https://osu.ppy.sh/u/{s['user_info']['username'].replace(' ', '%20')}) `{score} {combo}  {acc}%` {modsStr}\n"

            desc = descRed + descBlue
            name = 'Name'
            for i in range(maxLen - len(name)):
                name += ' '

            combo = 'Combo'
            for i in range(comboLen - len(combo)):
                combo += ' '

            score = 'Score'
            for i in range(scoreLen - len(score)):
                score += ' '

            desc = f":black_circle: :black_circle: `{name}` `{score} {combo}   Acc    Mods`\n" + desc
            if redScore > blueScore:
                desc = f":red_circle: **__`{redScore:,}`__** | `{blueScore:,}` :blue_circle:\n\n" + desc
            else:
                desc = f":red_circle: `{redScore:,}` | **__`{blueScore:,}`__** :blue_circle:\n\n" + desc
            try:
                e = discord.Embed(title=f"{b['title']}[{b['version']}]", url=f"https://osu.ppy.sh/b/{b['beatmap_id']}", description=desc)
                e.set_author(name=f"Round {round} of {m['match']['name']}", url=f"https://osu.ppy.sh/community/matches/{id}")
                e.set_thumbnail(url=f"https://b.ppy.sh/thumb/{b['beatmapset_id']}l.jpg")
                e.set_footer(text=f"Played at {g['start_time']}")
            except:
                e = discord.Embed(title='Deleted Beatmap', description=desc)
                e.set_author(name=f"Round {round} of {m['match']['name']}", url=f"https://osu.ppy.sh/community/matches/{id}")
                e.set_footer(text=f"Played at {g['start_time']}")

            await ctx.send(embed=e)

    @commands.command()
    async def testOsu(self, ctx, user=None, arg=None, num=5):
        print(utils.get_beatmaplink_all(self.conn))

    @tasks.loop(seconds=4)
    async def osutracker(self):
        try:
            self.cycle += 1
            lst = get_osutrack_all(self.conn)
            i = lst[(self.cycle % len(lst))]
            l = i[3]
            p = api.get_user_best({'u':i[0],  'limit':l})
            topPlaysNew = []
            playStr = ''
            for b in p:
                playStr += b['pp'] + ' '
                topPlaysNew.append(str(b['pp']))

            add_plays(self.conn, (playStr, i[0], i[1]))
            u = api.get_user({'u': i[0]})[0]
            oldpp = get_pp(self.conn, i[0])
            oldrank = get_rank(self.conn, i[0])
            add_pp(self.conn, (u['pp_raw'], i[0]))
            add_rank(self.conn, (u['pp_rank'], i[0]))
            topPlaysOld = set(i[2].split(' '))
            for v in range(0, l):
                if topPlaysNew[v] not in topPlaysOld:
                    r = p[v]
                    id = p[v]['beatmap_id']
                    if int(r['enabled_mods']) == 0:
                        modsStr = ''
                        modsInt = 0
                    else:
                        mods = bitwiseEnum.findCombo(modDic, int(r['enabled_mods']), [])
                        modsStr = ''
                        modsInt = 0
                        for mod in reversed(mods):
                            if mod == 'dt' or mod == 'nc':
                                modsInt += 64
                            if mod == 'ez':
                                modsInt += 2
                            if mod == 'hr':
                                modsInt += 16
                            if mod == 'ht':
                                modsInt += 256
                            try:
                                modsStr += modEmotes[mod]
                            except:
                                print('ah fuck (most likely caused by nc)')

                    b = api.get_beatmaps({'b':p[v]['beatmap_id'],  'mods':modsInt})[0]
                    acc = (50 * int(r['count50']) + 100 * int(r['count100']) + 300 * int(r['count300'])) / (300 * (int(r['countmiss']) + int(r['count100']) + int(r['count50']) + int(r['count300'])))
                    if r['perfect'] == '0':
                        fc = f"(FC: {ppcalc.ppcalculate(acc * 100, int(b['max_combo']), 0, modsStr, 'https://osu.ppy.sh/osu/' + str(id), True)[0]})"
                    else:
                        fc = ''
                    completed = ''
                    if int(b['count_normal']) + int(b['count_slider']) + int(b['count_spinner']) > int(r['count50']) + int(r['count100']) + int(r['count300']) + int(r['countmiss']):
                        completed = f"\nCompleted: {round((int(r['count50']) + int(r['count100']) + int(r['count300']) + int(r['countmiss'])) / (int(b['count_normal']) + int(b['count_slider']) + int(b['count_spinner'])) * 100, 2)}%"
                    desc = f"[[{b['version']}][{round(float(b['difficultyrating']), 2)}★]](https://osu.ppy.sh/b/{b['beatmap_id']}){modsStr}\n**{round(float(p[v]['pp']), 2)}pp** {fc} | {round(acc * 100, 2)}% | {int(r['score']):,} | {r['maxcombo']}/{b['max_combo']} | [{r['count300']}/{r['count100']}/{r['count50']}/{r['countmiss']}]{completed}"
                    embed = discord.Embed(title=(f"{b['title']}"), url=('https://osu.ppy.sh/b/' + b['beatmap_id']), description=desc, color=16748262)
                    rankLink = rankLinks[r['rank'].lower()]
                    status = int(b['approved'])
                    if status == 4:
                        status = 'Loved'
                    else:
                        if status == 3:
                            status = 'Qualified'
                        else:
                            if status == 2:
                                status = 'Approved'
                            else:
                                if status == 1:
                                    status = 'Ranked'
                                else:
                                    if status == 0:
                                        status = 'Pending'
                                    else:
                                        if status == -1:
                                            status = 'WIP'
                                        else:
                                            if status == -2:
                                                status = 'Graveyard'
                    embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{b['beatmapset_id']}l.jpg")
                    embed.set_author(name=f"New top #{v + 1} play for {u['username']}!", icon_url=rankLink)
                    embed.set_footer(text=f"{oldpp}pp → {u['pp_raw']}pp | #{oldrank} → #{u['pp_rank']}", icon_url=f"http://s.ppy.sh/a/{u['user_id']}")
                    temp = i[1].split()
                    for o in temp:
                        channelb = self.bot.get_channel(int(o))
                        await channelb.send(embed=embed)

        except Exception as e:
            try:
                if str(e) == 'list index out of range':
                    return
                print(f"{str(e)} {i[0]}")
            finally:
                e = None
                del e

    @osutracker.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()