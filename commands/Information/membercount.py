import discord
from discord.ext import commands
from utils import embeds
import datetime
import time

class membercount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["memberscount"], description="View server member count")
    async def membercount(self, ctx):
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16) 
        guild_icon = [ctx.guild.icon.url if ctx.guild.icon else "https://fi.pinterest.com/pin/787074472372724511/"][0]

        embed = discord.Embed(color=color)
        embed.Empty
        embed.set_author(icon_url=guild_icon, name=f"{ctx.guild.name} daily statistics")
        embed.set_footer(text="{member_count} members, {message_count} messages (command is unfinished and left purposely like this)")

        embed.add_field(name="Users", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Humans", value=len([member for member in ctx.guild.members if not member.bot]), inline=True)
        embed.add_field(name="Bots", value=len([member for member in ctx.guild.members if member.bot]), inline=True)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(membercount(client))