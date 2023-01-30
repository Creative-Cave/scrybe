import discord
import json
from discord.ext import commands
from discord.commands import SlashCommandGroup
from data import users

async def get_users(ctx: discord.AutocompleteContext):
    return await ctx.interaction.guild.fetch_members(limit=None)

class Users(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    pronouns = SlashCommandGroup(name="pronouns", description="Pronouns and how you want people to refer to you", guild_ids=[915996676144111706])

    @pronouns.command(guild_ids=[915996676144111706])
    async def get(self, ctx, user: discord.Option(discord.User, autocomplete=get_users)):
        pronouns = users.get_user_pronouns(user.id)
        if not pronouns:
            return await ctx.respond("This user hasn't set their pronouns yet.")
        return await ctx.respond(f"This user uses {'/'.join(pronouns)} pronouns.")


def setup(bot):
    bot.add_cog(Users(bot))
    