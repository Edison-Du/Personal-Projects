import discord
from discord.ext import commands
import os
import json

bot = commands.Bot(command_prefix = ".")
dirPath = os.path.dirname(os.path.realpath(__file__))

bot.remove_command("help")

for i in os.listdir(dirPath+"\cogs"):
    if (i.endswith(".py")):
        bot.load_extension(f"cogs." + i[:-3])

async def is_owner(ctx):
    return (ctx.author.id == 331852390426869770)

#=================== Commands ===================#
@bot.command()
async def help(ctx, cmdtype = ""):
    mbed = discord.Embed(
        title = "Help Command",
        colour = discord.Colour.orange()
    )
    if (cmdtype == "2048"):
        mbed.add_field(
            name = "2048", 
            value = ".2048 -> Start game\n.cont -> Resend board\n.end -> End game\n.high2048 -> Highscore", 
            inline=True
        ) 
    elif (cmdtype == "blackjack"):
        mbed.add_field(
            name = "Blackjack", 
            value = ".21 <bet> -> Start game\n.hit -> Draw card\n.stand -> End turn\n.double -> Double bet, then draw and end", 
            inline=True
        ) 
    elif (cmdtype == 'slots'):
        mbed.add_field(
            name = "Slots", 
            value = ".slot <bet> -> Spin\n.paylines -> View active paylines\n.setline <line #> -> Activates/deactivates a payline", 
            inline=True
        ) 
    else:  
        mbed.add_field(
            name = "Commands", 
            value = ".help 2048\n.help blackjack\n.help slots", 
            inline=True
        ) 
    await ctx.send(embed = mbed)

@bot.command()
@commands.check(is_owner)
async def load(ctx, extension): 
    try: 
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"{ctx.author.mention} Successfully loaded {extension}")
    except: await ctx.send(f"{ctx.author.mention} No such extension.")

@bot.command()
@commands.check(is_owner)
async def unload(ctx, extension): 
    try: 
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"{ctx.author.mention} Successfully unloaded {extension}")
    except: await ctx.send(f"{ctx.author.mention} No such extension.")

#==================== Errors ====================#

@load.error
async def load_error(ctx, error):
  if isinstance(error, (commands.CommandError)):
    await ctx.send(f"{ctx.author.mention} You are not allowed to use owner commands.")

@unload.error
async def unload_error(ctx, error):
  if isinstance(error, (commands.CommandError)):
    await ctx.send(f"{ctx.author.mention} You are not allowed to use owner commands.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.MissingRequiredArgument)):
        await ctx.send(f"{ctx.author.mention} Please input all necessary parameters")
    elif isinstance(error, (commands.CommandNotFound)):
        await ctx.send(f"{ctx.author.mention} Command '{ctx.message.content}' not found. Please type a valid command.")
    else: raise error

bot.run('<YOUR TOKEN HERE>')