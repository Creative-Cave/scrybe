from discord.ext import commands


class Server(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # simple command to send the link to the rules website
  @commands.slash_command(guild_ids=[915996676144111706])
  async def rules(self, ctx):
    await ctx.send_response(
      "You can read the server rules here: https://web.writerscave.repl.co/rules/"
    )


def setup(bot):
  bot.add_cog(Server(bot))
