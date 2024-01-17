import discord
import random
import os
from pathlib import Path
from discord.ext import commands


class Entertainment(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Entertainment(bot))
