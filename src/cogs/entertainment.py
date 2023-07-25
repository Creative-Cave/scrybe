import discord
import random
import os
from discord.ext import commands

with open(os.path.join("scrybe", "src", "assets", "pickup_lines.txt"), "r", encoding="utf-8") as fp:
  lines = fp.read().split("\n")


class Entertainment(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # select a random pickup line from assets/pickup_lines.txt and send it
  @commands.slash_command(guild_ids=[915996676144111706], description="Send a pickup line that you should never use to find a mate.")
  @discord.commands.option("id", int, required=False, min_value=1, max_value=len(lines))
  async def pickup_line(self, ctx, id: int):
    if id:
      await ctx.send_response(lines[id - 1])
    else:
      await ctx.send_response(random.choice(lines))


def setup(bot):
  bot.add_cog(Entertainment(bot))
