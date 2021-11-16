import discord
from discord.ext import commands
from utils import embeds, user
import os
import psutil

class about(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["botinfo", "uglyinfo"], description="Shows bot information")
    async def about(self, ctx, member : discord.Member = None):
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16) 
        mem = (str(round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2  ))+" MB")
        
        embed = discord.Embed(description=f"Bot statistics, developed by ps#0001\n**Memory:** {mem}, **Commands:** {len(self.client.commands)}", timestamp=discord.utils.utcnow())
        embed.set_author(name=self.client.user.name, icon_url=user.av(self.client.user))
        embed.add_field(name="Members", value=f"{sum([g.member_count for g in self.client.guilds])} total\n{len(self.client.users)} unique", inline=True)
        embed.add_field(name="Channels", value=f"{sum([len(g.channels) for g in self.client.guilds])} total\n{sum([len(g.text_channels) for g in self.client.guilds])} text\n{sum([len(g.voice_channels) for g in self.client.guilds])} voice", inline=True)
        embed.add_field(name="Guilds", value=f"{len(self.client.guilds)} (private)", inline=True)
        embed.add_field(name="Uptime", value=f"Online since <t:{round(self.client.start_time)}:R>", inline=True)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(about(client))