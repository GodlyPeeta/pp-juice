import discord
from discord.ext import commands
from discord.ext import tasks
from discord import Webhook, RequestsWebhookAdapter, File
from discord.utils import get
import cogs
import time

class VOICE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def proudsimp(self, ctx):
        channel = ctx.message.author.voice.channel
        if channel!= None:
            vclient =await channel.connect()
            vclient.play(discord.FFmpegPCMAudio('lib/proudsimp.mp3'))
            while vclient.is_playing():
                time.sleep(1)
            await vclient.disconnect()
        else:
            await ctx.send("User is not in a voice channel")