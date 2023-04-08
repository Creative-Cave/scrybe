import discord
import os
from dotenv import load_dotenv

print("starting bot...")

bot = discord.Bot(intents = discord.Intents.all())

# register cogs in cogs dir
exts_to_load = len(
  [fn for fn in os.listdir('./src/cogs') if fn.endswith('.py')])

for i, fn in enumerate(os.listdir('./src/cogs')):
  if fn.endswith('.py'):
    bot.load_extension(f'cogs.{fn[:-3]}')
    print(
      f"loaded {fn} - {(i+1)/exts_to_load*100}% - {i+1} of {exts_to_load} completed"
    )
print("done")


@bot.event
async def on_ready():
  print("bot is online")





load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))

#    _._     _,-'""`-._ <>
#   (,-.`._,'(       |\`-/|
#       `-.-' \ )-`( , o o)   _______
#             `-    \`_`"'-  /_layla_\
