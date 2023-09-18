import discord
import random
import json
import os
from discord.ext import commands
from discord.commands import SlashCommandGroup
from data import economy_controller as ec

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.json"))) as fn:
            self.config = json.load(fn)
            self.economy_config = self.config["economy"]
    
    economy_group = SlashCommandGroup("economy", "Staff commands for the server economy")

    # get the balance of a user
    @commands.slash_command(guild_ids=[915996676144111706], description="Get the balance of yourself or another user.")
    @discord.commands.option("user", discord.Member, required=False)
    async def balance(self, ctx, user: discord.Member):
        if not user:
            user = ctx.author

        economy = ec.get_economy()

        try:
            user_balance = economy[str(user.id)]
        except KeyError:
            ec.create_account(user.id)
            user_balance = ec.get_economy()[str(user.id)]

        embed = discord.Embed(
            title = f"Balance for {user.display_name}",
            colour = discord.Colour.green()
        )

        embed.add_field(name="Balance", value=f":coin: {user_balance:,}")
        await ctx.send_response(embed=embed)

    @commands.slash_command(guild_ids=[915996676144111706], description="Go to work to earn some money.")
    @commands.cooldown(1, 60*15, commands.BucketType.user)
    async def work(self, ctx):
        earned = random.randint(self.economy_config["min_work_income"], self.economy_config["max_work_income"])

        ec.adjust_balance(ctx.author.id, earned)
        embed = discord.Embed(
            title = "Work",
            colour = discord.Colour.green(),
            description = random.choice(self.economy_config["strings"]["work"])
        )

        embed.add_field(name="You earned", value=f"{self.economy_config['currency_emoji']} {earned:,}", inline=False)
        embed.add_field(name="New balance", value=f"{self.economy_config['currency_emoji']} {ec.get_economy()[str(ctx.author.id)]:,}", inline=False)

        await ctx.send_response(embed=embed)

    # set the balance of a user
    @commands.slash_command(guild_ids=[915996676144111706], description="Set the balance of yourself or another user.")
    @discord.commands.default_permissions(administrator=True)
    @discord.commands.option("user", discord.Member, required=True)
    @discord.commands.option("amount", int, required=False)
    async def set_balance(self, ctx, user: discord.Member, amount: int = 0):
        if not ctx.guild:
            return await ctx.send_response("This is a sensitive command, so it cannot be run in DMs. If you have permission, please run this command in the Creative Cave server instead.")
        
        economy = ec.get_economy()

        try:
            old_balance = economy[str(user.id)]
            economy[str(user.id)] = amount
        except KeyError:
            old_balance = 0
            ec.create_account(user.id)
            ec.get_economy()[str(user.id)] = amount

        ec.update_economy(economy, f"Set balance for {user.display_name}")

        embed = discord.Embed(
            title = f"Set balance for {user.display_name}",
            colour = discord.Colour.purple()
        )

        embed.add_field(name="Old balance", value=f":coin: {old_balance:,}")
        embed.add_field(name="New balance", value=f":coin: {amount:,}")

        await ctx.send_response(embed=embed)
        

def setup(bot):
    bot.add_cog(Economy(bot))
    