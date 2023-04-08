import discord
from discord.ext import commands


class CanvaDesign(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener("on_message")
  async def canva(self, message):
    if "canva design" in message.content.lower():
      await message.add_reaction("🗣️")
  

def setup(bot):
  bot.add_cog(CanvaDesign(bot))
