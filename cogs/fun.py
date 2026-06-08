import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with Pong!"""
        await ctx.send('Pong!')

    @commands.command(name='getout')
    async def getout(self, ctx):
        """Sends a GIF that says 'GET OUT!!!'"""
        # A popular "Get Out" GIF link
        gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2J6Znd4ZzR6NHR4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0HlMSVVYMZ8lWGpW/giphy.gif"
        await ctx.send(gif_url)

async def setup(bot):
    await bot.add_cog(Fun(bot))
