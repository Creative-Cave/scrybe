import discord
from discord.ext import commands


class ServerStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # counts the amount of bots and humans in the server and sends a message with that data
    @commands.slash_command(guild_ids=[915996676144111706], description="Counts the number of humans and bots")
    async def members(self, ctx):
        response = await ctx.send_response("Counting members...")

        members = await ctx.guild.fetch_members(limit=None).flatten()
        bots = len([m for m in members if m.bot])
        humans = len(members) - bots

        await response.edit_original_response(
            content=f"Humans - {humans}\nBots - {bots}\nTotal - {len(members)}")

    @commands.slash_command(guild_ids=[915996676144111706], description="Returns the bot's latency")
    async def ping(self, ctx):
        ping = self.bot.latency
        if round(ping * 1000) <= 50:
            colour = 0x44ff44
            tier = "<:signalgood:1132668380466401341> Good"

        elif round(ping * 1000) <= 100:
            colour = 0xffd000
            tier = "<:signalaverage:1132668378088218705> Average"

        elif round(ping * 1000) <= 200:
            colour = 0xff6600
            tier = "<:signalpoor:1132668374493700177> Poor"
            
        else:
            colour = 0x990000
            tier = "<:signalbad:1132668370647515197> Bad"

        embed = discord.Embed(title=":ping_pong: Latency", description=f"Current ping: ~{round(ping * 1000, 3)}ms", color=colour)
        embed.add_field(name="Rating", value=tier)
        
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(ServerStats(bot))
