import discord
import os
import requests
import asyncio
import Brainshop
import openai
from cleverbotfree import CleverbotAsync, Cleverbot, async_playwright
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# @Cleverbot.connect
# def generate_response(bot, prompt: str) -> str:
#     print(1)
#     chat = bot.single_exchange(prompt)
#     print(2)
#     bot.close()
#     print(3)
#     return chat

brain = Brainshop.Brain(key=os.getenv("CHATBOT_TOKEN"), bid=174308)


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[915996676144111706])
    async def ask_scrybe(self, ctx, prompt: str):
        response = await ctx.send_response("https://giphy.com/gifs/rodneydangerfield-thinking-math-rodney-gEvab1ilmJjA82FaSV")

        url = "https://acobot-brainshop-ai-v1.p.rapidapi.com"

        querystring = {"bid":"178","key":"sX5A2PcYZbsN5EY6","uid":"mashape","msg":prompt}

        headers = {
            "X-RapidAPI-Key": os.getenv("RAPID_TOKEN"),
            "X-RapidAPI-Host": "acobot-brainshop-ai-v1.p.rapidapi.com"
        }

        completion = requests.request("GET", url, headers=headers, params=querystring)

        await response.edit_original_response(content=f"**You said:**\n```{prompt}```\n**Scrybe says:\n**```{completion.text} ```")


def setup(bot):
    bot.add_cog(Chatbot(bot))
