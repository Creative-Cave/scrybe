import discord
from discord.ext import commands


class ServerStats(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # counts the amount of bots and humans in the server and sends a message with that data
  @commands.slash_command(guild_ids=[915996676144111706])
  async def members(self, ctx):
    response = await ctx.send_response("Counting members...")

    members = await ctx.guild.fetch_members(limit=None).flatten()
    bots = len([m for m in members if m.bot])
    humans = len(members) - bots

    await response.edit_original_response(content = f"Humans - {humans}\nBots - {bots}\nTotal - {len(members)}")


def setup(bot):
  bot.add_cog(ServerStats(bot))
