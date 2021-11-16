import discord
from discord.ext import commands
from utils import embeds
import random

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        pings = [
            "**your mother**",
            "**the chinese government**",
            "**lastfms backend**",
            "**my teeshirt**",
            "**lil mosey**",
            "**north korea**",
            "**localhost**",
            "**twitter**",
            "**the santos**",
            "**the trash**",
            "**a connection to the server**",
            "**6ix9ines ankle monitor**",
            "**fivem servers**",
            "**new york**",
            "**my black airforces**",
            "**netflix database**"
        ]
        await ctx.send(f"It took `{round(self.client.latency*1000)} ms` to ping {random.choice(pings)}")

def setup(client):
    client.add_cog(ping(client))