import discord
from discord.ext import commands
import random
import json
import os

tileEmotes = {
    0 : "<:tile0:751646127673049251>",
    2 : "<:tile2:751645113746456671>",
    4 : "<:tile4:751646127782101072>",
    8 : "<:tile8:751646127757197392>",
    16: "<:tile16:751646127790751845>",
    32: '<:tile32:751806236676194335>',
    64: '<:tile64:751806236801892403>',
    128: '<:tile128:751806237284499506>',
    256: '<:tile256:751806238152589434>',
    512: '<:tile512:751806238777671830>',
    1024: '<:tile1024:751806238848974930>',
    2048: '<:tile2048:751806239863996427>',
    4096: '<:tile4096:751806240941670451>',
    8192: '<:tile8192:751806242154086440>'
}
directionEmotes = ['⬅️', '⬆️', '⬇️', '➡️']
activeGames = {}

class Game:
    def __init__(self):
        self.grid = [[0]*4 for i in range (4)]
        self.vis = [[False]*4 for i in range (4)]
        self.moved = False
        self.empty = [] 
        self.msg = None
        self.score = 0

    def displayGrid(self):
        outGrid = ""
        for i in self.grid:
            for j in i: outGrid += tileEmotes[j] 
            outGrid += "\n"
        return outGrid

    def move(self, x, y, dx, dy):
        nx, ny = x+dx, y+dy
        if (nx >= 0 and ny >= 0 and nx < 4 and ny < 4):
            if (self.grid[nx][ny] == 0):
                self.moved = True
                self.grid[nx][ny] = self.grid[x][y]
                self.grid[x][y] = 0
                self.move(nx, ny, dx, dy)
            elif (self.grid[nx][ny] == self.grid[x][y] and self.vis[nx][ny] == False):
                self.moved = True
                self.grid[nx][ny] *= 2
                self.grid[x][y] = 0
                self.vis[nx][ny] = True
                self.score += self.grid[nx][ny]

    def push(self, neg, hor):
        self.vis = [[False]*4 for i in range (4)]
        if (not neg):
            for i in range (3, -1, -1):
                for j in range (3, -1, -1):
                    if (self.grid[i][j] != 0 and hor): self.move(i, j, 0, 1)
                    elif (self.grid[i][j] != 0 and not hor): self.move(i, j, 1, 0)
        else:
            for i in range (4):
                for j in range (4):
                    if (self.grid[i][j] != 0 and hor): self.move(i, j, 0, -1)
                    elif (self.grid[i][j] != 0 and not hor): self.move(i, j, -1, 0)

    def canMove(self):
        self.moved = False
        temp = [i[:] for i in self.grid]
        temp2 = self.score
        yes = False
        for i, j in [(1, 0), (1, 1), (0, 0), (0, 1)]: 
            self.push(i, j)
            self.grid = [i[:] for i in temp]
            if (self.moved == True): 
                yes = True
                break
        self.grid = [i[:] for i in temp]
        self.score = temp2
        self.moved = False
        return yes

    def computerTurn(self):
        self.empty = []
        for i in range (4):
            for j in range (4):
                if (self.grid[i][j] == 0): self.empty.append((i, j))
        if (len(self.empty) == 0): return False
        s1, s2 = random.choice(self.empty)
        self.grid[s1][s2] = random.choice([2, 4])
        return True

class Twentyfortyeight(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    def updateHigh(self, userid, amt):
        userid = str(userid)
        hs = self.bot.highscores.get(userid)
        if (hs == None): self.bot.highscores[userid] = amt
        else: 
            if (hs < amt):
                self.bot.highscores[userid] = amt
                return True
            return False
    
    def updateMoney(self, userid, amt):
        userid = str(userid)
        cy = self.bot.currency.get(userid)
        if (cy == None): self.bot.currency[userid] = amt
        else: self.bot.currency[userid] += amt

    def gameEnd(self, userid, username, score):
        curName = username + " | Game Over!"
        if (self.updateHigh(userid, score)): curName = username + " | New Highscore!"
        mbed = discord.Embed(
            title = curName,
            description = "Your score was " + '{:,}'.format(score) + ".\nYou've made $" + '{:,}'.format(score*3) + ".",
            colour = discord.Colour.orange()
        )
        self.updateMoney(userid, score*3)
        del activeGames[userid]
        return mbed

    @commands.command(name = "2048")
    async def _2048(self, ctx):
        global activeGames
        activeGames[ctx.author.id] = Game()
        currentGame = activeGames.get(ctx.author.id)
        startembed = discord.Embed(
            title = "2048 | " + str(ctx.author)[:-5],
            description = "Use reactions to play",
            colour = discord.Colour.orange()
        )
        await ctx.send(embed = startembed)
        currentGame.computerTurn()
        currentGame.msg = await ctx.send(currentGame.displayGrid())
        for i in directionEmotes:
            await currentGame.msg.add_reaction(i)
    
    @commands.command()
    async def end(self, ctx):
        global activeGames
        currentGame = activeGames.get(ctx.author.id)
        if (currentGame != None):
            mbed = self.gameEnd(ctx.author.id, ctx.author.name, currentGame.score)
            await ctx.send(embed = mbed)
        else:
            await ctx.send(f"{ctx.author.mention} Not currently in game lol")
    
    @commands.command()
    async def cont(self, ctx):
        global activeGames
        currentGame = activeGames.get(ctx.author.id)
        if (currentGame != None):
            await ctx.send(f"{ctx.author.mention} Game continued, use reactions to play.")   
            currentGame.msg = await ctx.send(currentGame.displayGrid())
            for i in directionEmotes:
                await currentGame.msg.add_reaction(i)
        else:
            await ctx.send(f"{ctx.author.mention} Not currently in game lol")

    @commands.command()
    async def high2048 (self, ctx):
        hs = self.bot.highscores.get(str(ctx.author.id))
        if (hs == None): await ctx.send(f"{ctx.author.mention} Your high score is 0")
        else: await ctx.send(f"{ctx.author.mention} Your high score is " + '{:,}'.format(hs))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global activeGames
        currentGame = activeGames.get(user.id)
        if (user.bot or currentGame == None): return
        channel = reaction.message.channel
        if (reaction.message.id == currentGame.msg.id):
            if (reaction.emoji == "⬆️"): currentGame.push(1, 0)
            elif (reaction.emoji == "⬇️"): currentGame.push(0, 0)
            elif (reaction.emoji == "⬅️"): currentGame.push(1, 1)
            elif (reaction.emoji == "➡️"): currentGame.push(0, 1)
            else: return
            if (currentGame.moved == True):
                c = currentGame.computerTurn()
                if (c == False):
                    mbed = self.gameEnd(user.id, user.name, currentGame.score)
                    await channel.send(embed = mbed)
                else:
                    await currentGame.msg.edit(content = currentGame.displayGrid())
                    if (currentGame.canMove() == False):
                        mbed = self.gameEnd(user.id, user.name, currentGame.score)
                        await channel.send(embed = mbed)
            await reaction.remove(user)

def setup(bot): bot.add_cog(Twentyfortyeight(bot))