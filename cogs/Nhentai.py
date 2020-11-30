import discord
from discord.ext import commands
import nhentai


class nh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nhsearch(self, ctx, arg):  # searches nhentai for hentais :flushed:
        results = [d for d in nhentai.search(arg, 1)]

        try:
            dsc = str(results[0].pages) + "pages\n\n"
        except:
            await ctx.send("No results")
            return

        i = 1
        while i < 5:
            dsc += "[" + str(results[i].name) + "](https://nhentai.net/g/" + str(results[i])[7:] + ")\n" + str(
                results[i].pages) + "pages\n\n"
            i += 1
        embed = discord.Embed(title=results[0].name, url="https://nhentai.net/g/" + str(results[0])[7:],
                              description=dsc, color=0xd90005)
        embed.set_author(name="Search results for " + arg, url="https://nhentai.net/search/?q=" + arg,
                         icon_url="https://i.kym-cdn.com/entries/icons/facebook/000/026/029/8P68F-_I_400x400.jpg")
        embed.set_thumbnail(url=results[0].cover)
        embed.set_footer(text="you horny fuck")
        await ctx.send(embed=embed)
