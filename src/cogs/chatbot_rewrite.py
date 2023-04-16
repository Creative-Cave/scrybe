import discord
import requests
import json
from discord.ext import commands


class Chatbot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[915996676144111706])
    @discord.commands.default_permissions(administrator=True)
    async def ask_scrybe(self, ctx, message: str):
        response = await ctx.send_response("Scrybe is thinking...")

        embed = discord.Embed(title="Ask Scrybe", colour=discord.Colour.teal())
        embed.add_field(name="You said:", value=message, inline=False)

        data = {
            "application": "8583352252014867612",
            "instance": "46045911",
            "message": message
        }

        r = requests.post(
            "https://www.botlibre.com/rest/json/chat", json=data).text
        try:
            bot_message = json.loads(r)["message"]
        except json.decoder.JSONDecodeError:
            bot_message = r

        embed.add_field(name="Scrybe says:", value=bot_message, inline=False)

        await response.edit_original_response(content="", embed=embed)


def setup(bot):
    bot.add_cog(Chatbot(bot))
