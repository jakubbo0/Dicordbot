# fun.py

from discord.ext import commands

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command()
    async def roll_dice(self, ctx):
        await ctx.send('Rolling dice...')

def setup(bot):
    bot.add_cog(FunCog(bot))