import discord
from discord.ext import commands
import random
import json
import os
import typing
import time

itemEmotes = [
    ":red_envelope:",
    ":candy:",
    ":tickets:",
    ":package:"
]

class Economy(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    def updateMoney(self, userid, amt):
        userid = str(userid)
        cy = self.bot.currency.get(userid)
        if (cy == None): self.bot.currency[userid] = amt
        else: self.bot.currency[userid] += amt

    def balance(self, userid, username):
        userid = str(userid)
        mbed = discord.Embed(
            title = username + " | Balance",
            description = "$" + '{:,}'.format(self.bot.currency.get(userid)),
            colour = discord.Colour.blue()
        )
        items = self.bot.items.get(userid)
        val = "None"
        if (items != None and sum(items) > 0):
            val = ""
            for i in range (4):
                if (items[i] > 0):
                    val += itemEmotes[i] + " x" + str(items[i]) + "\n"
        mbed.add_field(
            name = "Items",
            value = val,
            inline = False,
        )
        return mbed

    @commands.command()
    async def bal(self, ctx, user: typing.Optional[discord.Member] = None):
        if (user == None): 
            cy = self.bot.currency.get(str(ctx.author.id))
            if (cy == None): 
                self.updateMoney(ctx.author.id, 0)
            mbed = self.balance(ctx.author.id, str(ctx.author)[:-5])
            await ctx.send(embed = mbed)

        else:
            cy = self.bot.currency.get(str(user.id))
            if (cy == None):
                self.updateMoney(user.id, 0)
            else:
                mbed = self.balance(user.id, str(user.name))
                await ctx.send(embed = mbed)
    
    @commands.command()
    async def give(self, ctx,  user: typing.Optional[discord.Member] = None, *, amt : typing.Optional[int] = None):
        if (user == None): 
            await ctx.send("Who?")
        elif (amt == None):
            await ctx.send("🥴")
        elif (amt <= 0):
            await ctx.send("🥴")
        else:
            cy = self.bot.currency.get(str(ctx.author.id))
            if (cy == None or cy < amt):
                await ctx.send("Non-sufficient funds 😆")
                return
            self.updateMoney(ctx.author.id, -amt)
            self.updateMoney(user.id, amt)
            mbed = discord.Embed(
                title = str(ctx.author)[:-5] + " | Transaction",
                description = "Transfered $" + '{:,}'.format(amt) + " to " + str(user.name),
                colour = discord.Colour.green()
            )
            await ctx.send(embed = mbed)
    

    @commands.command()
    async def income(self, ctx):
        cy = self.bot.lastIncome.get(str(ctx.author.id))
        if (cy == None or int(time.time())-cy >= 30*60):
            mbed = discord.Embed(
                title = "You've received income",
                description = "$1,000",
                colour = discord.Colour.green()
            )
            await ctx.send(embed = mbed)
            self.bot.lastIncome[str(ctx.author.id)] = int(time.time())
            self.updateMoney(ctx.author.id, 1000)
        else:
            wait = 30*60 - (int(time.time())-cy)
            mbed = discord.Embed(
                title = "Please wait " + str(wait//60) + "m " + str(wait%60) + "s",
                description = "Last received: " + time.asctime(time.localtime(cy)) ,
                colour = discord.Colour.red()
            )
            await ctx.send(embed = mbed)


def setup(bot): bot.add_cog(Economy(bot))