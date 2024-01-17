import discord
import os
import math
import humanize
import time
import asyncio
import traceback
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent

bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Activity(type=1, name="Goat Simulator 2"))

# iterate through the cogs folder to load each one
for i, fn in enumerate(os.listdir(os.path.join(ROOT_DIR, "cogs"))):
    if fn.endswith('.py'):
        bot.load_extension(f'cogs.{fn[:-3]}')

if "🗣️.py" not in os.listdir(os.path.join(ROOT_DIR, "cogs")):
    raise SyntaxError("CANVA DESIGN 🗣️(s) not found")

print("done")

@bot.event
async def on_ready():
    print("bot is online")


@bot.event
async def on_error(error: Exception):
    log_channel = await bot.fetch_channel(1044725850702102528)
    await log_channel.send(f"An error occurred:```{error}```")


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title=":hourglass: You're on cooldown!",
            description=f"It looks like you're on cooldown for this command. Try again <t:{round(time.time()) + math.ceil(error.retry_after)}:R>.",
            color=discord.Colour.red()
        )
        return await ctx.send_response(embed=embed, ephemeral=True, delete_after=math.ceil(error.retry_after))

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="<:no:1097504076977156207> You can't run this command in DMs.",
            description="You do not have the required permissions to run this command.\n\n##Missing permissions:\n" + '\n'.join(error.missing_permissions),
            color=discord.Colour.red()
        )
        return await ctx.send_response(embed=embed)

    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(
            title="<:no:1097504076977156207> You can't run this command in DMs.",
            description="For security reasons, you must run this command in the Creative Cave server.",
            color=discord.Colour.red()
        )
        return await ctx.send_response(embed=embed)

    if isinstance(error, asyncio.TimeoutError):
        pass
    
    log_channel = await bot.fetch_channel(1044725850702102528)
    await log_channel.send(f"An error occurred:```{error}```\nFrom command </{ctx.command}:{ctx.command.qualified_id}>\nUser {ctx.author}")
    print(f"Error:\n{''.join(traceback.format_exception(error))}\n\nFrom command /{ctx.command}\nUser {ctx.author}")


def run(): # function to start the bot to either be run directly or though app.py
    load_dotenv()
    bot.run(os.getenv("BOT_TOKEN"))


if __name__ == "__main__": # check if this file is being run directly. if so, start the bot with run()
    run()

#  _._     _,-'""`-._ <>
# (,-.`._,'(       |\`-/|    Fly high <3
#     `-.-' \ )-`( , o o) 
#           `-    \`_`"'-  /_LAYLA_\
