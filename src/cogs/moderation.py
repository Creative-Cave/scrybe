import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.message_command(name="Report Message")
    async def report_message(self, ctx, message: discord.Message):
        content = message.content.encode("unicode_escape")
        attachments = message.attachments

        logging_channel = await self.bot.fetch_channel(1168140394324836374)
        await logging_channel.send(f"## Reported message (reported by {ctx.author.mention})\n\nMessage from {message.author.mention}```{message.content}```\nJump link: {message.jump_url}\n{'Attached file(s):' if attachments else ''}\n", files=[await f.to_file() for f in attachments])
        await ctx.send_response("Thank you for reporting. We'll take a look at this message and take the appropriate action as soon as possible.\nPlease be aware that repeated false reports will result in your ability to report messages revoked.", ephemeral=True)


def setup(bot):
    bot.add_cog(Moderation(bot))