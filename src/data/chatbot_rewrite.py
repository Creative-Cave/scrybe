import discord
import requests
import json
from discord.ext import commands


class Chatbot(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  @commands.slash_command(guild_ids=[ 915996676144111706])
  @discord.commands.default_permissions(administrator=True)
  async def ask_scrybe(self, ctx, message: str):
    response = await ctx.send_response("Scrybe is thinking...")

    data = {
      "application": "8583352252014867612",
      "instance": "47089143",
      "message": message
    }

    r = requests.post("https://www.botlibre.com/rest/json/chat", json=data).text
    bot_message = json.loads(r)["message"]
    await response.edit_original_response(content=f"You said: ```{message}```\nScrybe says: ```{bot_message}```")


def setup(bot):
  bot.add_cog(Chatbot(bot))
