import discord
from discord.ext import commands

def setup(bot):
    @bot.command(name='ping')
    async def ping(ctx):
        await ctx.send("Pong!")
