import discord
from discord.ext import commands


class CanvaDesign(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # add reactions in specific cases
    @commands.Cog.listener("on_message")
    async def canva(self, message):
        if "canva" in message.content.lower() and "design" in message.content.lower():
            await message.add_reaction("🗣️")
            await message.add_reaction("<:a:1094403429604020294>")
        if "inkscape" in message.content.lower() and "design" in message.content.lower():
            await message.add_reaction("🤦‍♂️")
            await message.add_reaction("❌")
            await message.add_reaction("❓")


def setup(bot):
    bot.add_cog(CanvaDesign(bot))
