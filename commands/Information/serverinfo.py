import discord
from discord.ext import commands
from utils import embeds
import datetime
import time

class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["si","sinfo", "ginfo", "guildinfo"], description="View information about a server")
    async def serverinfo(self, ctx):
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16) 
        guild_icon = [ctx.guild.icon.url if ctx.guild.icon else ctx.author.display_avatar][0]
        guild_banner = [ctx.guild.banner.url if ctx.guild.banner else None][0]
        guild_splash = [ctx.guild.icon.url if ctx.guild.icon else None][0]
        author_avatar = [ctx.author.avatar.url if ctx.author.avatar else self.ctx.author.default_avatar.url][0]
        max_emojis = {
            0: "50",
            1: "100",
            2: "150",
            3: "250"
        }
        features = ', '.join([f'{feature.lower()}' for feature in ctx.guild.features]) or "No features"

        embed = discord.Embed(title=ctx.guild.name, description=f"Server created on {ctx.guild.created_at.strftime('%B %d, %Y')} **<t:{round(datetime.datetime.timestamp(ctx.guild.created_at))}:R>**\n__{ctx.guild.name}__ is on bot shard ID **{ctx.guild.shard_id+1}/{len(self.client.shards)}**", timestamp=discord.utils.utcnow(), color=color)
        embed.set_author(icon_url=author_avatar, name=ctx.author.name)
        embed.set_thumbnail(url=guild_icon)
        embed.set_footer(text=f"Guild ID: {ctx.guild.id}")

        embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
        embed.add_field(name="Members", value=f"**Total:** {ctx.guild.member_count}\n**Humans:** {len([member for member in ctx.guild.members if not member.bot])}\n**Bots:** {len([member for member in ctx.guild.members if member.bot])}", inline=True)
        embed.add_field(name="Information", value=f"**Region:** {ctx.guild.region}\n**Verification:** {ctx.guild.verification_level}\n**Level:** {ctx.guild.premium_tier}/{ctx.guild.premium_subscription_count} boosts", inline=True)
        embed.add_field(name="Design", value=f"**Banner:** [Click here]({guild_banner})\n**Splash:** [Click here]({guild_splash})\n**Icon:** [Click here]({guild_icon})", inline=True)
        embed.add_field(name=f"Channels ({len(ctx.guild.channels)})", value=f"**Text:** {len(ctx.guild.text_channels)}\n**Voice:** {len(ctx.guild.voice_channels)}\n**Category:** {len(ctx.guild.categories)}", inline=True)
        embed.add_field(name="Counts", value=f"**Roles:** {len(ctx.guild.roles)}/250\n**Emojis:** {len(ctx.guild.emojis)}/{max_emojis[ctx.guild.premium_tier]}\n**Boosters:** {len(ctx.guild.premium_subscribers)}", inline=True)
        embed.add_field(name="Features", value=f"```{features}```", inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(serverinfo(client))