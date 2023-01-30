import discord
import sys
import asyncio

bot = None

def get_bot():
    from main import bot


def get_guild(id):
    get_bot()
    return bot.get_guild(id)


async def get_guild_members(id: int):
    guild = get_guild(id)
    members = [m async for m in await guild.fetch_members()]
    return members
