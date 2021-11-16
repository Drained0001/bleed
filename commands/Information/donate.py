import discord
from discord.ext import commands
from utils import embeds
import datetime
import time

class donate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Donate to the bot hosting server")
    async def donate(self, ctx):
        color = int(embeds.data["colors"]["default"], 16) 

        embed = discord.Embed(title="DONATE", description=f"There are no current donor perks, donations are appriciated though. In that case that **donor perks do come out** all donors will get their perks. Join our server [**here**](https://discord.gg/ugly) to learn more.", color=color)
        embed.set_footer(text=f"All payments go directly to the bot for hosting, API expenses and more")
        embed.add_field(name="Donation methods", value="**Bitcoin**: `bc1qxuz4l45wgc2razyxkhcgv990c5askeaac3mymd`\n**Ethereum**: `0xC64f06120FACD6D516456D6E213DaFcdc1C5b8f1`", inline=True)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(donate(client))