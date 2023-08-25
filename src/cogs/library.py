import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from data import library_controller as lc


class Library(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    library_group = SlashCommandGroup("library", "Commands to do with our server library")

    # list of genres to select from when submitting
    genres = [
        "Fantasy", "Horror", "Mystery", "Comedy", "Romance", "Crime/Thriller",
        "Sci-Fi", "Non-Fiction", "Poetry"
    ]

    # stand-in command so users can see the library
    @library_group.command(guild_ids=[915996676144111706])
    async def view(self, ctx):
        await ctx.respond("You can find the server library through the link below. It'll be fully embedded into the bot soon!\n:link: <https://github.com/Writers-Cave/data/blob/main/library/library.json>")

    # debug command to send the contents of library.json in the data repo
    @library_group.command(guild_ids=[915996676144111706])
    @discord.commands.default_permissions(administrator=True)
    async def raw_library(self, ctx):
        await ctx.respond(lc.get_library())

    # submission command which sends works in to be reviewed by admins
    @commands.slash_command(guild_ids=[915996676144111706], description="Submit your work to be reviewed and potentially added to our library")
    @commands.cooldown(1, 120, commands.BucketType.user)
    @discord.option("title", description="The title of your work")
    @discord.option("author", description="The name/nickname of the work's author")
    @discord.option("genre", description="The genre that suits this work the best", choices=genres)
    @discord.option("url", description="The url that this work can be read at")
    async def submit(self, ctx, title: str, author: str, genre: str, url: str):
        response = await ctx.send_response("Sending your submission...")
        ls_channel = await self.bot.fetch_channel(1096127028970918048)

        id = lc.create_submission(title, author, genre, url, ctx.author.id) # create a new submission, using the create_submission() function to return the submission ID

        embed = discord.Embed(title=f"New Submission - #{id}", colour=discord.Colour.blue())

        embed.add_field(name="Title", value=title)
        embed.add_field(name="Author", value=author)
        embed.add_field(name="Genre", value=genre)
        embed.add_field(name="URL", value=url)
        embed.add_field(name="Submitted by", value=f"{ctx.author.mention} ({ctx.author.id}")

        submission_message = await ls_channel.send(embed=embed)
        await submission_message.add_reaction("👍")
        await submission_message.add_reaction("👎")
        await submission_message.create_thread(name=f"Submission: {title}", auto_archive_duration=10080)

        await response.edit_original_response(content="Submission sent!")

    @library_group.command(guild_ids=[915996676144111706], description="Approves a member's work")
    @discord.commands.default_permissions(administrator=True)
    @discord.option("id", description="The id for the submission to approve")
    @discord.option("change_title", description="Change the work's title (correct grammar/remove anything against rules)", required=False)
    async def approve(self, ctx, id: int, change_title: str):
        if not ctx.guild:
            return await ctx.send_response("This is a sensitive command, so it cannot be run in DMs. If you have permission, please run this command in the Creative Cave server instead.")

        response = await ctx.send_response("Working...")

        try:
            sub = lc.approve_submission(id, change_title)
        except KeyError:
            return await response.edit_original_response(content="That ID isn't valid, please try again")

        await response.edit_original_response(content="Approved submission. Notifying the author...")

        user = await self.bot.fetch_user(sub["submitted_by"])
        await user.send(f"Congratulations {user.mention}, your submission \"{sub['title']}\" was approved! It'll appear in our library soon.") # notify the author of the approved work

        await response.edit_original_response(content="Done!", delete_after=3)


def setup(bot):
    bot.add_cog(Library(bot))
