import discord
from discord.commands import SlashCommandGroup
from data import library_controller as lc
from discord.ext import commands




class Library(discord.Cog):

  def __init__(self, bot):
    self.bot = bot

  library_group = SlashCommandGroup("library", "Commands to do with our server library")
  
  genres = [
    "Fantasy", "Horror", "Mystery", "Comedy", "Romance", "Crime/Thriller",
    "Sci-Fi", "Non-Fiction", "Poetry"
  ]
  
  @library_group.command(guild_ids=[915996676144111706])
  async def view(self, ctx):
    await ctx.respond(
      "You can find the server library through the link below. It'll be fully embedded into the bot soon!\n:link: <https://github.com/Writers-Cave/data/blob/main/library/library.json>"
    )

  @library_group.command(guild_ids=[915996676144111706])
  @discord.commands.default_permissions(administrator=True)
  async def raw_library(self, ctx):
    await ctx.respond(lc.get_library())

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
    embed.add_field(name="Submitted by", value=f"{ctx.author.mention} ({ctx.author.id}")

    submission_message = await ls_channel.send(embed=embed)
    await submission_message.add_reaction("👍")
    await submission_message.add_reaction("👎")

    await response.edit_original_response(content="Submission sent!")


def setup(bot):
  bot.add_cog(Library(bot))
