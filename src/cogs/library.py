import discord
from data import library_controller
from discord.ext import commands


class Library(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[915996676144111706])
    async def library(self, ctx):
        await ctx.respond("You can find the server library through the link below. It'll be fully embedded into the bot soon!\n:link: <https://github.com/Writers-Cave/data/blob/main/library/library.json>")

    @commands.slash_command(guild_ids=[915996676144111706])
    async def raw_library(self, ctx):
        await ctx.respond(library_controller.get_library())


def setup(bot):
    bot.add_cog(Library(bot))
