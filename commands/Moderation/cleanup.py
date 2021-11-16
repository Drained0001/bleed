import discord
from discord.ext import commands
import time as t
from utils import embeds
import asyncio

class cleanup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["c"], description="Clean up the bot's messages in a channel")
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx, amount : int):
        try:
            await ctx.channel.purge(limit=amount, check=lambda message: message.author == self.client.user)
            await ctx.send(embed=embeds.approveEmbed(ctx, f"I was able to clean {amount} messages from myself"))
        except:
            await ctx.send(embed=embeds.warningEmbed(ctx, f"There was a error cleaning {amount} messages from myself"), delete_after=5)

def setup(client):
    client.add_cog(cleanup(client))