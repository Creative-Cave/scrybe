import discord
import requests
import aiohttp
import os
import asyncio
import json
from discord import Webhook
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class chatbot():
    def __init__(self, api_url=None):
        self.past_inputs = []
        self.past_outputs = []
        if not api_url:
            self.api_url = os.getenv("CHATBOT_HOST")
        else:
            self.api_url = api_url

    async def generate_response(self, prompt: str, client: str = "c") -> str:
        print(self.api_url)
        print(prompt)

        r = requests.post(
            self.api_url,
            json={
                "inputs": {
                    "past_user_inputs": self.past_inputs,
                    "generated_responses": self.past_outputs[-5:],
                    "text": prompt
                }
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CHATBOT_KEY')}"
            }
        )

        # print(r.status_code)
        # return r.json()["data"]["conversation"]["output"][:1000]

        print(json.dumps(r.json(), indent=4))
        print(r.status_code)
        try:
            output = r.json()["generated_text"]
        except KeyError:
            output = "Chatbot is setting up. Try again in a few seconds."

        self.past_inputs.append(prompt)
        self.past_outputs.append(output)
        return output or "Cool story, bro."


command_chatbot = chatbot()
channel_chatbot = chatbot()


class Chatbot(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.last_replied = 0

    @commands.slash_command(guild_ids=[915996676144111706], description="Talk to Scrybe (alternative to Discord's Clyde)")
    @commands.guild_only()
    @discord.commands.default_permissions(administrator=True)
    @discord.commands.option("message", description="The prompt that the bot will use to generate a response", max_length=1024)
    async def ask_scrybe(self, ctx, message: str):
        response = await ctx.send_response("Scrybe is thinking...")

        embed = discord.Embed(title="Ask Scrybe", colour=discord.Colour.blue())
        embed.add_field(name="You said:", value=message, inline=False)
        chatbot_response = await command_chatbot.generate_response(message)

        embed.add_field(name="Scrybe says:", value=chatbot_response, inline=False)
        embed.set_footer(text="Alpha build. Bugs may occur and Scrybe may say things that are incorrect or offensive.") # alpha disclaimer footer

        await response.edit_original_response(content="", embed=embed)

    @commands.Cog.listener("on_message")
    async def channel_chatbot(self, message):
        if message.channel.id not in [1131307096634298490, 1134120291765846066] or message.author.bot or message.content.startswith("^") or message.flags.suppress_notifications:
            return

        async with message.channel.typing():
            message.content = message.content.replace("#", "")

            chatbot_response = await channel_chatbot.generate_response(message.clean_content)
            chatbot_response = chatbot_response.replace("||", "") # remove spoilers automatically added by the api

            if not message.content:
                return # don't send anything if the message being read has no content (e.g. media)

            if message.channel.id == 1131307096634298490:
                async with aiohttp.ClientSession() as session: # create a new "session" for the webhook
                    webhook = Webhook.from_url(os.getenv("CLIVE_WEBHOOK_URL"), session=session)

                    if self.last_replied == message.author.id: # only ping the author if responding to a new person
                        await webhook.send(chatbot_response, username="Clive")
                    else:
                        await webhook.send(
                            f"> *Replying to {message.author.mention}:*\n{chatbot_response}", username="Clive")
            else:
                if self.last_replied == message.author.id: # only ping the author if responding to a new person
                    await message.channel.send(chatbot_response)
                else:
                        await message.channel.send(f"> *Replying to {message.author.mention}:*\n{chatbot_response}")

        self.last_replied = message.author.id

        print(f"FROM {message.author.name}:\n{message.content}\n") # logging for moderation purposes
        print(f"RESPONSE: {chatbot_response}\n")


def setup(bot):
    bot.add_cog(Chatbot(bot))
