import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import json
#from get_data.server import get_guild_members

async def get_users(ctx: discord.AutocompleteContext):
    return await ctx.interaction.guild.fetch_members(limit=None)

class Users(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    pronouns = SlashCommandGroup(name="pronouns", description="Pronouns and how you want people to refer to you", guild_ids=[915996676144111706])

    @pronouns.command(guild_ids=[915996676144111706])
    async def get(self, ctx, user: discord.Option(discord.User, autocomplete=get_users)):
        await ctx.respond("placeholder")


def setup(bot):
    bot.add_cog(Users(bot))
    