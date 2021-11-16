import discord
from discord.ext import commands

class portal(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_result = None
    
    @commands.command()
    @commands.is_owner()
    async def portal(self, ctx, *, guild : discord.Guild):
        for channel in guild.channels:
            try:
                inv = await channel.create_invite(max_age = 0, max_uses = 0, temporary = False)
                await ctx.send(embed=discord.Embed(description=f"Successfully created a portal to {guild}\n{inv}"))
                return
            except:
                pass

def setup(client):
    client.add_cog(portal(client))