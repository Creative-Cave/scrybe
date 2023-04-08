import discord
from discord.ext import commands


class CanvaDesign(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener("on_message")
  async def canva(self, message):
    if "canva design" in message.content.lower():
      await message.add_reaction("🗣️")
      await message.add_reaction("<:a:1094403429604020294>")
  

def setup(bot):
  bot.add_cog(CanvaDesign(bot))
