import os
import Brainshop
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


brain = Brainshop.Brain(key=os.getenv("CHATBOT_TOKEN"), bid=174308)


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[915996676144111706])
    async def ask_scrybe(self, ctx, prompt: str):
        response = await ctx.send_response("https://giphy.com/gifs/watchallblk-double-cross-allblk-dc-yeWfJK4cvMtSh8wrXP")

        await response.edit_original_response(content=f"**You said:**\n```{prompt}```\n**Scrybe says:\n**```{brain.ask(prompt)} ```")


def setup(bot):
    bot.add_cog(Chatbot(bot))
