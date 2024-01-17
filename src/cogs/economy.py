import discord
import random
import os
import json
from discord.ext import commands
from discord.commands import SlashCommandGroup
from ext import economy_controller as ec


with open(os.path.join("src", "config.json")) as fn:
    config = json.load(fn)


class Economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    shop_group = SlashCommandGroup("shop", "View and buy from the server shop")
    
    @commands.slash_command(
        name="balance",
        description="Gets the balance of a user",
        guild_ids=[915996676144111706]
    )
    @discord.commands.option(
        name="user",
        type=discord.Member,
        required=False
    )
    async def balance(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        
        async with ctx.typing():
            eco = ec.get_economy()
            if str(user.id) not in eco.keys():
                balance = ec.create_account(user.id)["balance"]
            else:
                balance = eco[str(user.id)]["balance"]
        
        embed = discord.Embed(
            title="User Balance",
            colour=discord.Colour.blue()
        )
        embed.add_field(
            name=f"{user.display_name}'s Balance",
            value=balance
        )

        await ctx.respond(embed=embed)

    
    @commands.slash_command(
        name="inventory",
        description="View your or another member's inventory",
        guild_ids=[915996676144111706]
    )
    @discord.commands.option(
        name="user",
        type=discord.Member,
        required=False
    )
    async def inventory(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author

        async with ctx.typing():
            eco = get_economy()
            if str(user.id) not in eco.keys():
                inventory = ec.create_account(user.id)["inventory"]
            else:
                inventory = eco[str(user.id)]["inventory"]
        
        await ctx.respond("The shop is still a WIP - please be patient!")


    @commands.slash_command(
        name="coinflip",
        description="Flip a coin",
        guild_ids=[915996676144111706],
    )
    @discord.commands.option(
        name="guess",
        choices=["Heads", "Tails"]
    )
    @discord.commands.option(
        name="bet",
        type=int,
        default=0,
        min_value=0
    )
    async def coinflip(self, ctx, guess: str, bet: int):
        result = random.choice(["Heads", "Tails"])
        if random.randint(1, 500) == 1:
            result = "Side"

        if bet > ec.get_economy()[str(ctx.author.id)]["balance"]:
            return await ctx.respond("You can't afford to make a bet this high.")

        response_strings = config["economy"]["strings"]["coinflip"]
        
        if guess == result:
            response = random.choice(response_strings["win"]).format(result)
            prize = bet

        elif guess != result and result != "Side":
            response = random.choice(response_strings["loss"]).format(result)
            prize = bet * -1

        else:
            response = random.choice(response_strings["side"]).format(result)
            prize = 0
        
        if prize:
            ec.adjust_balance(ctx.author.id, prize)
        
        if bet and result != "Side":
            response += f"\nYou {['lost', 'won'][guess == result]} {bet}"
            
        elif bet and result == "Side":
            response += "\nYou won nothing"
        
        embed = discord.Embed(
            title="Coinflip",
            description=response,
            colour=discord.Colour.yellow()
        )

        await ctx.respond(embed=embed)

        
def setup(bot):
    bot.add_cog(Economy(bot))
