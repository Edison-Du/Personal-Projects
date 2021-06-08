import discord
from discord.ext import commands
import random
import json
import os
import math

paylines = [
    [1,1,1,1,1],
    [0,0,0,0,0],
    [2,2,2,2,2],
    [0,1,2,1,0],
    [2,1,0,1,2],
    [0,0,1,2,2],
    [2,2,1,0,0],
    [1,0,1,2,1],
    [1,2,1,0,1]
]

symbols = [
    ":cherries:",
    ":bell:",
    ":shamrock:",
    ":trophy:",
    ":gem:",
    ":red_envelope:",
    ":candy:",
    ":tickets:",
    ":package:"
]
multiplier = [10, 50, 100, 500, 1000]

class Game:

    # all inclusive
    # 1/10 (1-100) cherry
    # 1/50  (101-120) bell
    # 1/100 (121-130) shamrock
    # 1/500 (131-132)  trophy
    # 1/1000 (133-133) gem

    def __init__ (self, bet, active, username):

        self.reels = [
            random.choices([0,1,2,3,4,5,6,7,8], weights = [20,18,16,14,12,1,1,1,1], k = 5) 
            for i in range (3)]
        
        self.active = active
        self.bet = bet
        self.activePaylines = sum(active)
        self.foundItems = [0,0,0,0]

        self.gameEmbed = discord.Embed(
            title = "𝒮𝐿𝒪𝒯𝒮 | " + username,
            description = "Bet: $" + '{:,}'.format(self.bet) + "\nActive Paylines: " + str(self.activePaylines),
            colour = discord.Colour.gold()
        )

    def construct(self):

        self.reelOutput = ""
        for i in self.reels:
            for j in i: self.reelOutput += symbols[j] + " "
            self.reelOutput += "\n"
        
        self.gameEmbed.add_field(
            name = "===<  Spin  >===",
            value = self.reelOutput,
            inline = False
        )
    
    def rigWin (self):
        for i in range(3):
            winningLine = random.randint(1,2500)
            if (winningLine <= 100): winningLine = 0
            elif (winningLine <= 120): winningLine = 1
            elif (winningLine <= 130): winningLine = 2
            elif (winningLine <= 132): winningLine = 3
            elif (winningLine == 133): winningLine = 4
            else: continue

            for j in range (5):
                self.reels[paylines[i][j]][j] = winningLine

    def spin(self):

        self.rigWin()

        wonPaylines = ""
        netGain = 0
        curWin = 0
        
        
        for i in range(3):
            if (self.active[i]==1):
                last = self.reels[paylines[i][0]][0]
                won = True
                for j in range (5):
                    ind = self.reels[paylines[i][j]][j]
                    if (ind != last): won = False 
                    if (ind > 4): self.foundItems[ind-5] += 1

                if (won):
                    if (last < 5):
                        curWin = multiplier[last]*self.bet
                        wonPaylines += symbols[last] + " x" + str(multiplier[last]) + " -> $" + '{:,}'.format(curWin) + "\n"
                        netGain += curWin

        self.construct()

        if (netGain == 0):
            self.gameEmbed.add_field(
                name = "Unlucky",
                value = "No winning paylines.",
                inline = False
            )
        else:
            self.gameEmbed.add_field(
                name = "You've won $" + '{:,}'.format(netGain),
                value = wonPaylines,
                inline = False
            )

        if (sum(self.foundItems) > 0):
            val = ""
            for i in range(4):
                if (self.foundItems[i] > 0): 
                    val += "x" + str(self.foundItems[i]) + " " + symbols[i+5] + " "

            self.gameEmbed.add_field(
                name = "You've Found",
                value = val,
                inline = False,
            )

        netGain -= self.bet * self.activePaylines

        self.gameEmbed.add_field(
            name = "Net gain",
            value = "$ " + '{:,}'.format(netGain),
            inline = False,
        )

        return netGain

        
class Slots(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    def updateMoney(self, userid, amt):
        userid = str(userid)
        cy = self.bot.currency.get(userid)
        if (cy == None): self.bot.currency[userid] = amt
        else: self.bot.currency[userid] += amt

    def updatePaylines(self, userid, num):
        num -= 1
        userid = str(userid)
        cy = self.bot.activePaylines.get(userid)
        if (cy == None): self.bot.activePaylines[userid] = [0,0,0]
        self.bot.activePaylines[userid][num] = 1-self.bot.activePaylines[userid][num]

    def updateItems(self, userid, foundItems):
        userid = str(userid)
        cy = self.bot.items.get(userid)
        if (cy == None): self.bot.items[userid] = [0,0,0,0]
        for i in range(4):
            self.bot.items[userid][i] += foundItems[i]

    def getPaylines(self, ctx):
        active = self.bot.activePaylines.get(str(ctx.author.id))
        if (active == None): active = [0,0,0]
        mbed = discord.Embed(
            title = "𝒮𝐿𝒪𝒯 𝒫𝒜𝒴𝐿𝐼𝒩𝐸𝒮 | " + str(ctx.author)[:-5],
            colour = discord.Colour.gold()
        )
        for i in range (3):
            val = ""
            check = "🔴 - "
            if (active[i]==1): check = "🟢 - "
            for j in (paylines[i]):
                if (j==0): val += ":orange_square:"
                else: val += ":white_large_square:"
            val += "\n"
            for j in (paylines[i]):
                if (j==1): val += ":orange_square:"
                else: val += ":white_large_square:"
            val += "\n"
            for j in (paylines[i]):
                if (j==2): val += ":orange_square:"
                else: val += ":white_large_square:"
            
            mbed.add_field(
                name = check+str(i+1), 
                value = val, 
                inline=True
            ) 
        return mbed

    @commands.command()
    async def paylines(self, ctx):
        await ctx.send(embed = self.getPaylines(ctx))
    
    @commands.command(name = "setline")
    async def setPayline(self, ctx, num):
        try:
            num = int(num)
        except:
            await ctx.send("?")
            return
        if (num > 3):
            await ctx.send("Only 3 paylines man")
            return
        self.updatePaylines(ctx.author.id, num)
    
    @commands.command()
    async def slot(self, ctx, bet):

        userPaylines = self.bot.activePaylines.get(str(ctx.author.id))
        cy = self.bot.currency.get(str(ctx.author.id))

        if (cy == None):
            await ctx.send("Non-sufficient funds 😆")
            return

        elif (userPaylines == None or sum(userPaylines) == 0):
            await ctx.send("You have no active paylines.")
            return

        try: 
            bet = int(bet)
        except:
            if (bet == "max"): bet = cy//sum(userPaylines)
            else:
                await ctx.send("?")
                return

        if (cy < (sum(userPaylines)*bet)):
            await ctx.send("Non-sufficient funds 😆")

        elif (bet <= 0):
            await ctx.send("🥴")
        
        else:
            game = Game(bet, userPaylines, str(ctx.author)[:-5])
            netGain = game.spin()

            self.updateMoney(ctx.author.id, netGain)
            self.updateItems(ctx.author.id, game.foundItems)
            await ctx.send(embed = game.gameEmbed)

def setup(bot): bot.add_cog(Slots(bot))