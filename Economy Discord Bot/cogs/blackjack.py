import discord
from discord.ext import commands
import random
import json
import os
import math

numEmotes = [
    "<:b1:804064733119774754>",
    "<:b2:804064738127380490>",
    "<:b3:804064738816032818>",
    "<:b4:804064739566026782>",
    "<:b5:804064740690100314>",
    "<:b6:804064740871634944>",
    "<:b7:804064739809820712>",
    "<:b8:804064740790894603>",
    "<:b9:804064740820254720>",
    "<:b10:804064740518133831>",
    "<:b11:804064739315154974>",
    "<:b12:804064740921835530>",
    "<:b13:804064740372512878>",
    "<:r1:804064740778311706>",
    "<:r2:804064740749344778>",
    "<:r3:804064740879237180>",
    "<:r4:804064739957145650>",
    "<:r5:804064740833624074>",
    "<:r6:804064740884217876>",
    "<:r7:804064740112072744>",
    "<:r8:804064740979507230>",
    "<:r9:804064741286084678>",
    "<:r10:804064740892606486>",
    "<:r11:804064740103815178>",
    "<:r12:804064740971905024>",
    "<:r13:804064740258086963>"
]
suitEmotes = [
    "<:dl:804043342140669982>",
    "<:cle:804043340634259486>",
    "<:hl:804043567110160504>",
    "<:sl:804043342887387146>",
    "<:dr:804043342601650227>",
    "<:cr:804043340969410561>",
    "<:hr:804043567571533905>",
    "<:sr:804043518586650697>"
]
fdownEmotes = [
    "<:t_lt:804464133835587666>",
    "<:t_rt:804350550920658984>",
    "<:s_lt:804143989766488066>",
    "<:s_rt:804143990085648394>",
    "<:b_lt:804350550921052200>",
    "<:b_rt:804464133801246741>"
]
white = "<:wt:804033982672928828>"
activeGames = {}

class Game:
    def __init__ (self, bet):
        self.deck = []
        for i in range (1, 14):
            for j in range (1, 5): 
                self.deck.append((i, j))
        random.shuffle(self.deck)

        self.bet = bet
        self.canDouble = True

        self.dealer = [self.deck.pop(),self.deck.pop()]
        self.player = [self.deck.pop(),self.deck.pop()]
        self.playerFirst = []
        self.playerSecond = []

    def getMessage(self, ctx, stood):

        curName = f"=========< DEALER : {self.sumHand(self.dealer)} >========="

        mbed = discord.Embed(
            title = "𝐵𝐿𝒜𝒞𝒦𝒥𝒜𝒞𝒦 | " + str(ctx.author)[:-5],
            colour = discord.Colour.dark_green()
        )
        if (stood):
            for cnt in range ((len(self.dealer)+5)//6):
                val = ""
                for i, j in self.dealer[cnt*6: min(len(self.dealer), cnt*6+6)]: 
                    val += str(numEmotes[(i-1)+13*(j%2)] + white + " ")
                val += "\n"
                for i, j in self.dealer[cnt*6: min(len(self.dealer), cnt*6+6)]: 
                    val += str(suitEmotes[j-1] + suitEmotes[j+3] + " ")
                val += "\n"
                for i, j in self.dealer[cnt*6: min(len(self.dealer), cnt*6+6)]: 
                    val += str(white + numEmotes[(i-1)+13*(j%2)] + " ")
                mbed.add_field(
                    name = curName, 
                    value = val, 
                    inline=False
                ) 
                curName = "‎‎-------------------------------------------------"
        else:
            val = ""
            f, s = self.dealer[0]
            val += str(numEmotes[(f-1)+13*(s%2)] + white + " " + fdownEmotes[0] + fdownEmotes[1] + "\n")
            val += str(suitEmotes[s-1] + suitEmotes[s+3] + " " + fdownEmotes[2] + fdownEmotes[3] + "\n")
            val += str(white + numEmotes[(f-1)+13*(s%2)] + " " + fdownEmotes[4] + fdownEmotes[5])
            mbed.add_field(
                name = "=========< DEALER : ?? >=========",
                value = val,
                inline = False
            )

        curName = f"=========< PLAYER : {self.sumHand(self.player)} >========="

        for cnt in range ((len(self.player)+5)//6):
            val = ""
            for i, j in self.player[cnt*6: min(len(self.player), cnt*6+6)]: 
                val += str(numEmotes[(i-1)+13*(j%2)] + white + " ")
            val += "\n"
            for i, j in self.player[cnt*6: min(len(self.player), cnt*6+6)]: 
                val += str(suitEmotes[j-1] + suitEmotes[j+3] + " ")
            val += "\n"
            for i, j in self.player[cnt*6: min(len(self.player), cnt*6+6)]: 
                val += str(white + numEmotes[(i-1)+13*(j%2)] + " ")

            mbed.add_field(
                name = curName, 
                value = val, 
                inline=False
            ) 
            curName = "‎‎-------------------------------------------------"

        return mbed

    def sumHand(self, arr):
        tot, aces = 0, 0
        for i, j in arr:
            if (i == 1): aces += 1
            else: tot += min(i, 10)
        if (aces > 0):
            tot += (aces-1)
            if (21-tot >= 11): tot += 11
            else: tot += 1
        return tot
                
    def draw(self):
        self.player.append(self.deck.pop())
    
    def stand(self):
        while (self.sumHand(self.dealer) < 17): 
            self.dealer.append(self.deck.pop())

# Main code, commands and events

class Blackjack(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    def updateMoney(self, userid, amt):
        userid = str(userid)
        cy = self.bot.currency.get(userid)
        if (cy == None): self.bot.currency[userid] = amt
        else: self.bot.currency[userid] += amt

    @commands.command(name = "21")
    async def _21(self, ctx, bet):
        global activeGames

        cy = self.bot.currency.get(str(ctx.author.id))
        currentGame = activeGames.get(ctx.author.id)

        if (cy == None): 
            await ctx.send("Non-sufficient funds 😆")

        try: 
            bet = int(bet)
        except:
            if (bet == "all"): bet = cy
            else:
                await ctx.send("?")
                return

        if (cy < bet): 
            await ctx.send("Non-sufficient funds 😆")

        elif (bet <= 0):
            await ctx.send("🥴")

        elif (currentGame == None):
            activeGames[ctx.author.id] = Game(bet)
            currentGame = activeGames.get(ctx.author.id)
            valPlayer = currentGame.sumHand(currentGame.player)
            valDealer = currentGame.sumHand(currentGame.dealer)
            mbed = currentGame.getMessage(ctx, True)
            if (valPlayer == 21 and valDealer == 21):
                mbed.add_field(
                    name = "Push", 
                    value = "You've Won $0", 
                    inline=False
                ) 
                del activeGames[ctx.author.id]
            elif (valPlayer == 21):
                mbed.add_field(
                    name = "NATURAL!", 
                    value = "You've Won $" + '{:,}'.format(math.ceil(currentGame.bet*1.5)), 
                    inline=False
                ) 
                self.updateMoney(ctx.author.id, math.ceil(currentGame.bet*1.5))
                del activeGames[ctx.author.id]
            elif (valDealer == 21):
                mbed.add_field(
                    name = "Dealer Natural", 
                    value = "You've Lost $" + '{:,}'.format(currentGame.bet), 
                    inline=False
                ) 
                self.updateMoney(ctx.author.id, -currentGame.bet)
                del activeGames[ctx.author.id]
            else:
                await ctx.send(embed = currentGame.getMessage(ctx, False))
                return
            await ctx.send(embed = mbed)

        else:
            mbed = currentGame.getMessage(ctx, False)
            mbed.add_field(
                name = "Why are you running?",
                value = "Please finish this game", 
                inline=False
            )
            await ctx.send(embed = mbed)

    async def hit(self, ctx, currentGame):
        currentGame.draw()
        currentGame.canDouble = False
        val = currentGame.sumHand(currentGame.player)
        mbed = currentGame.getMessage(ctx, True)
        if (val > 21):
            mbed.add_field(
                name = "Busted", 
                value = "You've Lost $" + '{:,}'.format(currentGame.bet), 
                inline=False
            ) 
            self.updateMoney(ctx.author.id, -currentGame.bet)
            del activeGames[ctx.author.id]
        else: return False
        await ctx.send(embed = mbed)
        return True

    async def stand(self, ctx, currentGame):
        currentGame.stand()
        valPlayer = currentGame.sumHand(currentGame.player)
        valDealer = currentGame.sumHand(currentGame.dealer)

        mbed = currentGame.getMessage(ctx, True)
        if (valPlayer > valDealer):
            mbed.add_field(
                name = "Your score is higher!", 
                value = "You've Won $" + '{:,}'.format(currentGame.bet), 
                inline=False
            ) 
            self.updateMoney(ctx.author.id, currentGame.bet)

        elif (valDealer > 21):
            mbed.add_field(
                name = "DEALER BUSTED!", 
                value = "You've Won $" + '{:,}'.format(currentGame.bet), 
                inline=False
            ) 
            self.updateMoney(ctx.author.id, currentGame.bet)

        elif (valDealer == valPlayer):
            mbed.add_field(
                name = "Push", 
                value = "You've Won $0", 
                inline=False
            ) 

        elif (valDealer > valPlayer):
            mbed.add_field(
                name = "Unlucky", 
                value = "You've Lost $" + '{:,}'.format(currentGame.bet), 
                inline=False
            ) 
            self.updateMoney(ctx.author.id, -currentGame.bet)

        await ctx.send(embed = mbed)
        del activeGames[ctx.author.id]
        return True

    @commands.command(name = "hit")
    async def hitCommand(self, ctx):
        global activeGames
        currentGame = activeGames.get(ctx.author.id)
        if (currentGame != None):
            state = await self.hit(ctx, currentGame)
            if (not state):
                await ctx.send(embed = currentGame.getMessage(ctx, False))
        else: 
            await ctx.send("Not in game")

    @commands.command(name = "stand")
    async def standCommand(self, ctx):
        global activeGames
        currentGame = activeGames.get(ctx.author.id)
        if (currentGame != None):
            await self.stand(ctx, currentGame)
        else: 
            await ctx.send("Not in game")

    @commands.command(name = "double")
    async def doubleCommand(self, ctx):
        global activeGames
        currentGame = activeGames.get(ctx.author.id)
        cy = self.bot.currency.get(str(ctx.author.id))

        if (currentGame != None):
            mbed = currentGame.getMessage(ctx, False)
            if (currentGame.canDouble == False): 
                mbed.add_field(
                    name = "Oops",
                    value = "You cannot double after you hit",
                    inline = False
                )
                await ctx.send(embed = mbed)
                return
            if (cy < currentGame.bet * 2):
                mbed.add_field(
                    name = "Oops",
                    value = "Non-sufficient funds 😆",
                    inline = False
                )
                await ctx.send(embed = mbed)
                return

            currentGame.bet *= 2
            state = await self.hit(ctx, currentGame)
            if (state): return
            await self.stand(ctx, currentGame)
        else: await ctx.send("Not in game")

def setup(bot): bot.add_cog(Blackjack(bot))