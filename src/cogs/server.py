import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from ext import pronouns_page as pp


class Server(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    pronouns_group = SlashCommandGroup("pronouns", "Commands relating to user pronouns and preferences.")

    # simple command to send the link to the rules website - omitted while the rules website is being built
    # @commands.slash_command(guild_ids=[915996676144111706])
    # async def rules(self, ctx):
    #     await ctx.send_response("You can read the server rules here: https://web.writerscave.repl.co/rules/")

    @pronouns_group.command(
        name="get",
        description="Gets the pronouns of a user from pronouns.page",
        guild_ids=[915996676144111706]
    )
    @discord.commands.option(
        name="user",
        type=discord.Member
    )
    @discord.commands.option(
        name="ephemeral",
        type=bool,
        default=True
    )
    async def get_pronouns(self, ctx, user: discord.Member, ephemeral: bool = True):
        pp_username = pp.get_pp_username(user.id)
        embed = discord.Embed(title=f"{user.display_name}'s Preferred Pronouns", colour=discord.Colour.blue())
        if user.bot:
            embed.description = ":robot: it/its"
            return await ctx.respond(embed=embed, ephemeral=ephemeral)

        if pp_username:
            pronouns = [item["value"] for item in pp.get_pronouns(pp_username) if item["opinion"] == "yes"]

            if not pronouns:
                embed.description = "This user has added a pronouns.page account, but it doesn't look like they have selected what pronouns they prefer."
            else:
                embed_content = ""
                for pronoun in pronouns:
                    embed_content += f"- {pronoun}\n"
                embed.description = embed_content
            embed.set_footer(text="Provided by en.pronouns.page")

            await ctx.respond(embed=embed, ephemeral=ephemeral)

        else:
            embed.description = "It doesn't look like this user has linked a pronouns.page profile yet.\n[Create an account here](<https://en.pronouns.page/account>)"
            await ctx.respond(embed=embed, ephemeral=ephemeral)


    @pronouns_group.command(
        name="add",
        description="Add your pronouns.page username",
        guild_ids=[915996676144111706]
    )
    @discord.commands.option(
        name="username",
        type=str
    )
    async def add_pronouns(self, ctx, username: str):
        msg = await ctx.send_response("Please wait...")
        async with ctx.typing():
            if pp.get_user_if_exists(username):
                pp.add_pp_username(ctx.author.id, username)
                await msg.edit_original_response(content=f"Added your pronouns.page username: @{username}")
            else:
                await msg.edit_original_response(content="It doesn't look like that pronouns.page account exists. [Create an account here](<https://en.pronouns.page/account>)")


def setup(bot):
    bot.add_cog(Server(bot))
