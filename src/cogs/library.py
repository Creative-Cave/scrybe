import discord
from discord.commands import SlashCommandGroup
from data import library_controller as lc


class Library(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    # create a slash command group so each library command is prefixed with /library
    library_group = SlashCommandGroup(
        "library", "Commands to do with our server library")

    # list of genres to select from when submitting
    genres = [
        "Fantasy", "Horror", "Mystery", "Comedy", "Romance", "Crime/Thriller",
        "Sci-Fi", "Non-Fiction", "Poetry"
    ]

    # stand-in command so users can see the library
    @library_group.command(guild_ids=[915996676144111706])
    async def view(self, ctx):
        await ctx.respond(
            "You can find the server library through the link below. It'll be fully embedded into the bot soon!\n:link: <https://github.com/Writers-Cave/data/blob/main/library/library.json>"
        )

    # debug command to send the contents of library.json in the data repo
    @library_group.command(guild_ids=[915996676144111706])
    @discord.commands.default_permissions(administrator=True)
    async def raw_library(self, ctx):
        await ctx.respond(lc.get_library())

    # submission command which sends works in to be reviewed by admins
    @library_group.command(guild_ids=[915996676144111706])
    @discord.commands.default_permissions(administrator=True)
    @discord.option("title", description="The title of your work")
    @discord.option("author", description="The name/nickname of the work's author")
    @discord.option("genre",
                    description="The genre that suits this work the best",
                    choices=genres)
    @discord.option("url", description="The url that this work can be read at")
    async def submit(self, ctx, title: str, author: str, genre: str, url: str):
        response = await ctx.send_response("Sending your submission...")
        ls_channel = await self.bot.fetch_channel(1096127028970918048)

        id = lc.create_submission(title, author, genre, url, ctx.author.id)

        embed = discord.Embed(title=f"New Submission - #{id}",
                              colour=discord.Colour.blue())

        embed.add_field(name="Title", value=title)
        embed.add_field(name="Author", value=author)
        embed.add_field(name="Genre", value=genre)
        embed.add_field(name="URL", value=url)
        embed.add_field(name="Submitted by",
                        value=f"{ctx.author.mention} ({ctx.author.id}")

        submission_message = await ls_channel.send(embed=embed)
        await submission_message.add_reaction("👍")
        await submission_message.add_reaction("👎")

        await response.edit_original_response(content="Submission sent!")

    @library_group.command(guild_ids=[915996676144111706])
    @discord.commands.default_permissions(administrator=True)
    @discord.option("id", description="The id for the submission to approve")
    async def approve(self, ctx, id: int):
        response = await ctx.send_response("Working...")

        try:
            sub = lc.approve_submission(id)
        except KeyError:
            return await response.edit_original_response(content="That ID isn't valid.")

        await response.edit_original_response(content="Approved submission. Notifying the author...")

        user = await self.bot.fetch_user(sub["submitted_by"])
        await user.send(f"Congratulations {user.mention}, your submission \"{sub['title']}\" was approved! It'll appear in our library soon.")

        await response.edit_original_response(content="Done!", delete_after=3)


def setup(bot):
    bot.add_cog(Library(bot))
