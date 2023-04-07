import discord
from discord.ext import commands


class Chatbot(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


# blah blah blah
...


def setup(bot):
  bot.add_cog(Chatbot(bot))
