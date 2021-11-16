
from discord.ext import commands
import discord
from typing import List

class Flags(commands.FlagConverter, delimiter=' ', prefix="--"):
    member: discord.Member = None
    text: str = None

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def flagTest(self, ctx, *, flags: Flags):
        await ctx.send(flags)
        await ctx.send(flags.member or "No member")
        await ctx.send(flags.text or "No text")

    @commands.command()
    async def cloneProgress(self, ctx):
        await ctx.send(embed=discord.Embed(description=f"{(len(self.client.commands)-8)/428:.2%} done cloning bleed"))

    @commands.command()
    @commands.is_owner()
    async def guilds(self, ctx):
        g = '\n'.join([g.name for g in self.client.guilds])
        await ctx.send(embed=discord.Embed(title="guilds", description=f"```{g}```"))

def setup(client):
    client.add_cog(test(client))