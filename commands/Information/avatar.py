import discord
from discord.ext import commands
from utils import embeds

class avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["av", "ab", "ag", "avi", "pfp"], description="Get avatar of a member or yourself")
    async def avatar(self, ctx, member : discord.Member = None):
        color = int(embeds.data["colors"]["default"], 16) 
        member = member or ctx.author

        author_avatar = ''.join([ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url])
        avatar = ''.join([member.avatar.url if member.avatar else member.default_avatar.url])

        embed = discord.Embed(description=f"[**{member.name}'s avatar**]({avatar})", color=color)
        embed.set_image(url=avatar)
        embed.set_author(name=ctx.author.name, icon_url=author_avatar)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(avatar(client))