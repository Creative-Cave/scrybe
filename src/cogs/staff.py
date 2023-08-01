import discord
from discord.ext import commands


class Staff(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command(guild_ids=[915996676144111706], description="Sends a message as Scrybe")
  @discord.commands.default_permissions(administrator=True)
  async def say(self, ctx, message: str):
    sent_message = await ctx.channel.send(message)
    await ctx.send_response("Sent message: {sent_message.jump_url}", ephemeral=True, delete_after=3)

  @commands.slash_command(guild_ids=[915996676144111706], description="Throw an intentional error for testing")
  async def error(self, ctx):
    await ctx.send(wrong_message)


def setup(bot):
  bot.add_cog(Staff(bot))
