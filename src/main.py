import discord
import os
from dotenv import load_dotenv

bot = discord.Bot(intents=discord.Intents.all())

# count cogs in cogs dir
exts_to_load = len(
  [fn for fn in os.listdir('./src/cogs') if fn.endswith('.py')])

# iterate through the cogs folder to load each one
for i, fn in enumerate(os.listdir('./src/cogs')):
  if fn.endswith('.py'):
    bot.load_extension(f'cogs.{fn[:-3]}')
    print(f"loaded {fn} - {i+1} of {exts_to_load} completed")

if "🗣️.py" not in os.listdir("./src/cogs"):
  raise SyntaxError("CANVA DESIGN 🗣️(s) not found")

print("done")


@bot.event
async def on_ready():  # print to console once bot is up and ready
  print("bot is online")
  await bot.change_presence(activity=discord.Game(
    name=f"Running on host {os.getenv('HOST')}"))


def run(
):  # function to start the bot to either be run directly or though app.py
  load_dotenv()
  bot.run(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":  # check if this file is being run directly. if so, start the bot with run()
  run()

#    _._     _,-'""`-._ <>
#   (,-.`._,'(       |\`-/|
#       `-.-' \ )-`( , o o)   _______
#             `-    \`_`"'-  /_layla_\
