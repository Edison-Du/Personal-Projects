import discord
from discord.ext import tasks, commands
import random
import json
import os

class Ready(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.dirPath = os.path.dirname(os.path.realpath(__file__))
    
    def save(self):

        data = self.dirPath[:-5] + "/data"

        with open(data + "/currency.JSON", "w") as f: 
            json.dump(self.bot.currency, f, indent = 4, sort_keys=True)
        with open(data + "/highscore.JSON", "w") as f: 
            json.dump(self.bot.highscores, f, indent = 4, sort_keys=True)
        with open(data + "/activePaylines.JSON", "w") as f: 
            json.dump(self.bot.activePaylines, f, indent = 4, sort_keys=True)
        with open(data + "/items.JSON", "w") as f: 
            json.dump(self.bot.items, f, indent = 4, sort_keys=True)
        with open(data + "/lastIncome.JSON", "w") as f: 
            json.dump(self.bot.lastIncome, f, indent = 4, sort_keys=True)

    @commands.Cog.listener()
    async def on_ready(self): 
        
        print("Online")

        data = self.dirPath[:-5] + "/data"

        with open(data + "/currency.JSON", "r") as f: 
            self.bot.currency = json.load(f)
        with open(data + "/highscore.JSON", "r") as f: 
            self.bot.highscores = json.load(f)
        with open(data + "/activePaylines.JSON", "r") as f: 
            self.bot.activePaylines = json.load(f)
        with open(data + "/items.JSON", "r") as f: 
            self.bot.items = json.load(f)
        with open(data + "/lastIncome.JSON", "r") as f: 
            self.bot.lastIncome = json.load(f)

        if (not self.autosave.is_running()):
            self.autosave.start()
            
    @commands.command(name = "save")
    @commands.is_owner()
    async def saveCommand(self, ctx):
        self.save()
        await ctx.send(f"{ctx.author.mention} Saved all.")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        self.save()
        await ctx.send("Shutting Down.")
        await self.bot.close()

    @saveCommand.error
    async def saveCommand_error(self, ctx, error):
        if isinstance(error, (commands.CommandError)):
            await ctx.send(f"{ctx.author.mention} You are not allowed to use owner commands.")

    @shutdown.error
    async def shutdown_error(self, ctx, error):
        if isinstance(error, (commands.CommandError)):
            await ctx.send(f"{ctx.author.mention} You are not allowed to use owner commands.")

    @tasks.loop(minutes=5.0)
    async def autosave(self):
        self.save()


    @commands.command()
    async def img(self, ctx):
        dirr = self.dirPath[:-5] + "/Face.png"
        with open(dirr, "rb") as f: 
            picture = discord.File(dirr)
            await ctx.send(file=picture)


def setup(bot): bot.add_cog(Ready(bot))