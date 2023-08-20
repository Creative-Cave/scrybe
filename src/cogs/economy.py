import discord
from discord.ext import commands
from data import economy_controller as ec

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # get the balance of a user
    @commands.slash_command(guild_ids=[915996676144111706], description="Get the balance of yourself or another user.")
    @discord.commands.option("user", discord.Member, required=False)
    async def balance(self, ctx, user: discord.Member):
        if not user:
            user = ctx.author

        try:
            user_balance = ec.get_economy()[str(user.id)]
        except KeyError:
            ec.create_account(user.id)
            user_balance = ec.get_economy()[str(user.id)]

        embed = discord.Embed(
            title = f"Balance for {user.display_name}",
            colour = discord.Colour.green()
        )

        embed.add_field(name="Balance", value=user_balance)
        await ctx.send_response(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))
    