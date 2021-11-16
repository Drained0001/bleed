import discord
from discord.ext import commands
from utils import embeds

class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=discord.Embed(description='Thanks for adding me. Start using me with `,help`'))
            break
        data = embeds.data
        channel = self.client.get_channel(898781782080643112)
        await channel.send(embed=discord.Embed(description=f"{data['emojis']['approve']} : Joined `{guild.name}` owned by `{guild.owner} ({guild.owner.id})` Member count: `{guild.member_count}`\nServer count: `{len(self.client.guilds)}`", color=int(data['colors']['approve'], 16)))
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        data = embeds.data
        channel = self.client.get_channel(898781782080643112)
        await channel.send(embed=discord.Embed(description=f"{data['emojis']['deny']} : Left `{guild.name}` owned by `{guild.owner} ({guild.owner.id})` Member count: `{guild.member_count}`\nServer count: `{len(self.client.guilds)}`", color=int(data['colors']['deny'], 16)))

def setup(client):
    client.add_cog(Join(client))