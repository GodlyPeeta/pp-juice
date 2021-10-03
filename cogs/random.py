import discord
from discord.ext import commands
from discord.ext import tasks
import cogs
from utils.init_utils import config
import sqlite3
from sqlite3 import Error
import utils
import random

class RANDOM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = config['DB_PATH']
        # create a database connection
        self.conn = utils.create_connection(self.database)
        print("Loading 10k words...")
        self.wordsList = []
        with open("lib/commonwords.txt", "r") as f:
            for i in f:
                b = i[:-1]
                self.wordsList.append(b)
                #print(b)
        self.romanised_numbers = {
            1:"one",
            2:"two",
            3:"three",
            4:"four",
            5:"five",
            6:"six",
            7:"seven",
            8:"eight",
            9:"nine"
        }
    @commands.command()
    async def minesweeper(self, ctx, mines = 5, lx=7, ly=7):
        if mines<0 or lx<0 or ly<0:
            await ctx.send("bruh")
            return
        if lx*ly <= mines:
            await ctx.send("no blank squares")
            return
        if lx*ly>225:
            await ctx.send("too large!")
            return
        arr=[]
        for i in range(ly):
            arr.append([])
            for v in range(lx):
                arr[i].append(0)
        v=0
        while v < mines:
            x = random.randint(0, lx-1)
            y = random.randint(0, ly-1)
            if arr[y][x] == 0:
                #print(f"{x} {y}")
                arr[y][x] = 9
            else:
                print("kdfjkdsf")
                v-=1
            v+=1
        
        for i in range(ly):
            for v in range(lx):
                if arr[i][v] == 9:
                    for k in range(-1, 2):
                        for o in range(-1, 2):
                            if not (k==0 and o==0):
                                if i+k >=0 and i+k < ly:
                                    if v+o >=0 and v+o < ly:
                                        if arr[i+k][v+o] != 9:
                                            arr[i+k][v+o]+=1
        for v in arr:
            print(v)
        
        flag = False
        for i in range(ly):
            for v in range(lx):
                if arr[i][v]==0:
                    flag = True
                    break
        
        if flag == False:
            await ctx.send("Warning: No blank squares")

        while True:
            x = random.randint(0, lx-1)
            y = random.randint(0, ly-1)
            if flag:
                if arr[y][x] == 0:
                    arr[y][x] = 10
                    break
            else:
                if arr[y][x] != 9:
                    arr[y][x] = 10+arr[y][x]
                    break

        prt = f"Click on a spoiler to begin ({lx}x{ly}, {mines} bombs)\n"
        for i in range(ly):
            for v in range(lx):
                if arr[i][v] == 9:
                    prt+="||:bomb:||"
                elif arr[i][v] == 0:
                    prt+="||:blue_square:||"
                elif arr[i][v] == 10:
                    prt+=":blue_square:"
                elif arr[i][v] > 10:
                    prt+=f":{self.romanised_numbers[arr[i][v]-10]}:"
                else:
                    prt+=f"||:{self.romanised_numbers[arr[i][v]]}:||"
            prt+='\n'
        
        try:
            await ctx.send(prt)
        except Exception as e:
            if e == "400 Bad Request (error code: 50035): Invalid Form Body\nIn content: Must be 2000 or fewer in length.":
                await ctx.send("Too long/large!")
                return
            await ctx.send(e)
        
        #for v in arr:
        #    print(v)



    @commands.command()
    async def wpm(self, ctx, words=30):
        if words > 75:
            await ctx.send("Too many words (max is 75)")
            return
        snd = ""
        for i in range(int(words)):
            snd += self.wordsList[random.randint(0, 9883)]+" "
        img = utils.generate_image_text(snd)
        await ctx.send(file = img)
        try:
            msg = await self.bot.wait_for(
                "message",
                timeout = 300,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
        except asyncio.Timeouterror:
            ctx.send("You took too long to type out those words!")
            return
        time = (msg.created_at.timestamp() - ctx.message.created_at.timestamp() - 0.1)/60
        avrgLength = (len(snd)-words)/words
        wpm = words/time
        acc = utils.text_similarity(snd[:-1], msg.content)
        if acc < 1:
            results = (
                f"{round(wpm, 1)} ➔ **{round(wpm*acc*acc, 1)}** wpm\n"
                f"{round(acc*100, 1)}% Accuracy"
            )
        else:
            results = f"{round(wpm, 1)} wpm **100%** acc"

        e = discord.Embed(description=results, title=f"{ctx.author.name}'s typing test results", colour=0x4557CD)

        e.add_field(
            name="Text information",
            value=(
                f"Length: {len(snd)-words} characters\n"
                f"Avg. word length: {round(avrgLength, 2)} characters\n"
            )
        )
        await ctx.send(embed=e)

    @commands.command()
    async def testRandom(self, ctx):
        await ctx.send("got")