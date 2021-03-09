import discord
from discord.ext import commands
from discord.ext import tasks
from discord import Webhook, RequestsWebhookAdapter, File
from discord.utils import get
import cogs
import config
import time
import utils
#1-0 sparkl
class YOUTUBE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = config.DB_PATH
        self.counter = 0
        self.conn = utils.create_connection(self.database)
        #self.ytnotifs.start()
    
    @commands.command()
    async def ytest(self, ctx):
        await ctx.send("bkdsfjklsdfjlsdafjlksdajflsdajfl")

    @commands.command()
    async def ytadd(self, ctx, link, channelid=None):
        if not utils.has_admin(ctx.author):
            if not utils.is_owner(ctx.author):
                await ctx.send('You do not have enough permissions to do this (admin)')
                print('ERROR, Not a admin')
                return
        id = link.split('/')[4]
        print(id)

        if channelid==None:
            channelid=ctx.channel.id

        try:
            utils.add_yt_channel_notif(self.conn, (id, f" {channelid}"))
        except:
            ch = utils.yt_notif_getchannels(self.conn, (id,))
            print(ch)
            ch+=f" {channelid}"
            utils.del_yt_channel_notif(self.conn, (id,))
            utils.add_yt_channel_notif(self.conn, (id, ch))
        await ctx.send(f'added')

    @commands.command()
    async def ytdel(self, ctx, link, channelid=None):
        if not utils.has_admin(ctx.author):
            if not utils.is_owner(ctx.author):
                await ctx.send('You do not have enough permissions to do this (admin)')
                print('ERROR, Not a admin')
                return
                
        if channelid==None:
            channelid=ctx.channel.id
        id = link.split('/')[4]
        ch = utils.yt_notif_getchannels(self.conn, (id,))
        if len(ch.split(' ')) == 2:
            utils.del_yt_channel_notif(self.conn, (id,))
        else: 
            print(channelid)
            print(ch)
            ch = ch.replace(f' {channelid}', "", 1)
            print(ch)
            utils.del_yt_channel_notif(self.conn, (id,))
            utils.add_yt_channel_notif(self.conn, (id, ch))
        await ctx.send("removed")
        
    @tasks.loop(seconds=60)
    async def ytnotifs(self):
        self.counter+=1
        lst = utils.yt_notif_getAll(self.conn)
        self.counter = self.counter % len(lst)
        v = utils.getLastVid(lst[self.counter][0])
        print(lst[self.counter][1])
        #print(v['etag'])
        if lst[self.counter][1] != v['items'][0]['id']['videoId']:
            for i in lst[self.counter][2].split(' '):
                try:
                    channelb = self.bot.get_channel(int(i))
                except: 
                    continue
                t=v['items'][0]['snippet']['channelTitle']
                link = v['items'][0]['id']['videoId']
                await channelb.send(f"{t} has posted a new video go watch it or you are retard faggot\n\nhttps://www.youtube.com/watch?v={link}")
            utils.yt_notif_lastVid(self.conn, (v['items'][0]['id']['videoId'], lst[self.counter][0]))
        #print(v)
        #print(lst)
    
    @ytnotifs.before_loop
    async def before(self):
        print('ytnotifs waiting...')
        await self.bot.wait_until_ready()