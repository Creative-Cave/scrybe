import discord
import random
import time
from discord.ext import commands


with open("src/assets/pickup_lines.txt", "r") as fp:
  lines = fp.read().split("\n")


class Entertainment(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command(guild_ids=[915996676144111706], name="pickup-line")
  @discord.commands.option("id", int, required=False, min_value=1, max_value=len(lines))
  @commands.has_role("Library Staff")
  async def pickup_line(self, ctx, id: int):
    if id:
      await ctx.send_response(lines[id - 1])
    else:
      await ctx.send_response(random.choice(lines))

def setup(bot):
  bot.add_cog(Entertainment(bot))