import discord
import requests
import aiohttp
import os
from discord import Webhook
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class chatbot():

  def __init__(self, api_url=None):
    if api_url == None:
      self.api_url = "https://clydeapi.happyenderyt123.repl.co/clyde/message"
    else:
      self.api_url = api_url

  def generate_response(self, prompt):
    r = requests.get(self.api_url + f"?prompt={prompt}")
    return r.text


command_chatbot = chatbot()
channel_chatbot = chatbot()


class Chatbot(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.last_replied = 0

  @commands.slash_command(guild_ids=[915996676144111706])
  @discord.commands.default_permissions(administrator=True)
  @discord.commands.option(
    "message",
    description="The prompt that the bot will use to generate a response",
    max_length=1024)
  async def ask_scrybe(self, ctx, message: str):
    response = await ctx.send_response("Scrybe is thinking...")

    embed = discord.Embed(title="Ask Scrybe", colour=discord.Colour.blue())
    embed.add_field(name="You said:", value=message, inline=False)
    chatbot_response = command_chatbot.generate_response(message)

    embed.add_field(name="Scrybe says:", value=chatbot_response, inline=False)

    await response.edit_original_response(
      content="",
      embed=embed.set_footer(
        text=
        "Test build. Bugs may occur and Scrybe may say things that are incorrect or offensive."
      ))

  @commands.Cog.listener("on_message")
  async def channel_chatbot(self, message):
    if message.channel.id != 1131307096634298490 or message.author.bot:
      return

    chatbot_response = channel_chatbot.generate_response(
      message.content).replace("||", "")

    async with aiohttp.ClientSession() as session:
      webhook = Webhook.from_url(os.getenv("CLIVE_WEBHOOK_URL"),
                                 session=session)
      if self.last_replied == message.author.id:
        await webhook.send(chatbot_response, username="Clive")
      else:
        await webhook.send(
          f"> *Replying to {message.author.mention}:*\n{chatbot_response}",
          username="Clive")

    self.last_replied = message.author.id

    print(f"FROM {message.author.name}:\n{message.content}\n")
    print(f"RESPONSE: {chatbot_response}")


def setup(bot):
  bot.add_cog(Chatbot(bot))
