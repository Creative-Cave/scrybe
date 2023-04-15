import discord
from discord.ext import commands


class Staff(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[915996676144111706])
    @discord.commands.default_permissions(administrator=True)
    async def say(self, ctx, message: str):
        await ctx.send_response("Sending...", ephemeral=True, delete_after=0)
        await ctx.channel.send(message)

def setup(bot):
    bot.add_cog(Staff(bot))
    