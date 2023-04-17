import discord
import requests
import json
import random
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class Chatbot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[915996676144111706])
    @discord.commands.default_permissions(administrator=True)
    @discord.commands.option("message", description="The prompt that the bot will use to generate a response", max_length=1024)
    async def ask_scrybe(self, ctx, message: str):
        response = await ctx.send_response("Scrybe is thinking...")

        embed = discord.Embed(title="Ask Scrybe", colour=discord.Colour.blue())
        embed.add_field(name="You said:", value=message, inline=False)

        data = {
            "application": random.choice(os.getenv("BL_IDS").split("_")),
            "instance": "47118083",
            "message": message
        }

        r = requests.post(
            "https://www.botlibre.com/rest/json/chat", json=data).text
        try:
            bot_message = json.loads(r)["message"]
        except json.decoder.JSONDecodeError:
            bot_message = r

        embed.add_field(name="Scrybe says:", value=bot_message, inline=False)

        await response.edit_original_response(content="", embed=embed.set_footer(text=f"ID: {data['application']}"))


def setup(bot):
    bot.add_cog(Chatbot(bot))
