import discord
from discord.ext import commands


class Testing(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(guild_ids=[915996676144111706])
    async def ping(self, ctx):
        await ctx.respond("hello, world")


def setup(bot):
    bot.add_cog(Testing(bot))
    