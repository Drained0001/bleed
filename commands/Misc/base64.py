import discord
from discord.ext import commands
import time
from utils import embeds
import asyncio
import base64 as b64

class base64(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(hidden=True, description="BASE64 command group")
    async def base64(self, ctx):
        return

    @base64.command(description="Encode a BASE64 string")
    async def encode(self, ctx, *, string):
        string = bytes(string, "UTF-8")
        string = b64.b64encode(string)
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16)
        await ctx.send(embed=discord.Embed(description=f'**BASE64 ENCODE**: {string.decode("UTF-8")}', color=color))

    @base64.command(description="Decode a BASE64 string")
    async def decode(self, ctx, *, string):
        string = bytes(string, "UTF-8")
        string = b64.b64decode(string)
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16)
        await ctx.send(embed=discord.Embed(description=f'**BASE64 DECODE**: {string.decode("UTF-8")}', color=color))

def setup(client):
    client.add_cog(base64(client))