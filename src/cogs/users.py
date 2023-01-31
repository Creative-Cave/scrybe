import discord
import json
from discord.ext import commands
from discord.commands import SlashCommandGroup
from data import users


class Users(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    pronouns = SlashCommandGroup(name="pronouns", description="Pronouns and how you want people to refer to you", guild_ids=[915996676144111706])

    @pronouns.command(description="Get the preferred pronouns a specific member wants used.", guild_ids=[915996676144111706])
    async def get(self, ctx, user: discord.Option(discord.User)):
        pronouns = users.get_user_pronouns(user.id)
        if not pronouns:
            return await ctx.send_response("This user hasn't set their pronouns yet; ask them or use `they/them` as an alternative.", ephemeral=True)
        return await ctx.send_response(f"This user goes by `{'/'.join(pronouns)}` pronouns.", ephemeral=True)


def setup(bot):
    bot.add_cog(Users(bot))
    