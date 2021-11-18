import discord
from discord.ext import commands
from utils import embeds
import random

class invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(f"https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot **invite me**")

def setup(client):
    client.add_cog(invite(client))