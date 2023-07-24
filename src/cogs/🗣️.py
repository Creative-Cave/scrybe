import discord
from discord.ext import commands


class CanvaDesign(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # add reactions in specific cases
  @commands.Cog.listener("on_message")
  async def canva(self, message):
    msg = message.content.lower()
    if "canva" in msg and "design" in msg:
      await message.add_reaction("🗣️")
      await message.add_reaction("<:a:1094403429604020294>")
    if "inkscape" in msg and "design" in msg:
      await message.add_reaction("🤦‍♂️")
      await message.add_reaction("❌")
      await message.add_reaction("❓")


def setup(bot):
  bot.add_cog(CanvaDesign(bot))
