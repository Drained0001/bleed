import discord
from discord.ext import commands
from utils import embeds

class snipe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.last_snipe = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.last_snipe[message.channel.id] = message

    @commands.command(aliases=["s"])
    async def snipe(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            msg = self.last_snipe[channel.id]
        except:
            return await ctx.send(embed=embeds.warningEmbed(ctx, "Nothing to snipe for now"))

        await ctx.send(embed=discord.Embed(description=f"```{msg.content[:3500]}```", color=msg.author.color).set_author(name=str(msg.author), icon_url=str(msg.author.display_avatar)))

def setup(client):
    client.add_cog(snipe(client))