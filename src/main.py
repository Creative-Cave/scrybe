import discord
import os
from dotenv import load_dotenv

bot = discord.Bot(intents=discord.Intents.all())

# count cogs in cogs dir
exts_to_load = len(
  [fn for fn in os.listdir(os.path.join("scrybe", "src", "cogs")) if fn.endswith('.py')])

# iterate through the cogs folder to load each one
for i, fn in enumerate(os.listdir(os.path.join("scrybe", "src", "cogs"))):
  if fn.endswith('.py'):
    bot.load_extension(f'cogs.{fn[:-3]}')
    print(f"loaded {fn} - {i+1} of {exts_to_load} completed")

if "🗣️.py" not in os.listdir(os.path.join("scrybe", "src", "cogs")):
  raise SyntaxError("CANVA DESIGN 🗣️(s) not found")

print("done")


@bot.event
async def on_ready():  # print to console once bot is up and ready
  print("bot is online")
  await bot.change_presence(activity=discord.Game(
    name=f"Running on host {os.getenv('HOST')}"))


@bot.event
async def on_error(error):
  log_channel = await bot.fetch_channel(1044725850702102528)
  await log_channel.send(f"Error:```{error}```")


@bot.event
async def on_application_command_error(ctx, error):
  log_channel = await bot.fetch_channel(1044725850702102528)
  await log_channel.send(f"Error:```{error}```\nFrom command </{ctx.command}:{ctx.command.qualified_id}>\nUser {ctx.author}")
  print(f"Error:\n{error}\n\nFrom command /{ctx.command}\nUser {ctx.author}")


def run():  # function to start the bot to either be run directly or though app.py
  load_dotenv()
  bot.run(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":  # check if this file is being run directly. if so, start the bot with run()
  run()

#    _._     _,-~~*-._ <>
#   (,-.`._,'(       |\`-/|  Fly high <3
#       `-.-' \ )-`( , ^ ^)   ________
#             `-    \`_`"'-  /  𝓛𝓪𝔂𝓵𝓪  \
