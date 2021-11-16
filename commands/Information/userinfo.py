import discord
from discord.ext import commands
from utils import embeds
import datetime

class whois(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["whois", "uinfo", "info", "user"], description="View information about a user/member")
    async def userinfo(self, ctx, member : discord.Member = None):
        member = member or ctx.author
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16)
        av = lambda x : x.avatar.url if x.avatar else x.default_avatar
        pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
        role = [r.mention for r in member.roles if r != ctx.guild.default_role]
        important = ["N/A"]
        important_perms = ['kick_members', 'ban_members', 'manage_channels', 'manage_guild', 'view_audit_log', 'manage_messages', 'mention_everyone', 'mute_members', 'deafen_members', 'move_members', 'manage_nicknames', 'manage_roles', 'manage_webhooks', 'manage_emojis']
        key_permissions = ', '.join([f"{' '.join(str(perm[0]).split('_'))}" for perm in member.guild_permissions if perm[1] and perm[0] in important_perms])

        embed = discord.Embed(title=member, description=f"`{member.id}` ∙ Join position: {pos} ∙ {len(ctx.author.mutual_guilds)} servers", color=color, timestamp=discord.utils.utcnow())
        embed.set_thumbnail(url=av(member))
        embed.set_author(icon_url=av(ctx.author), name=ctx.author.name)
        embed.add_field(name="Joined discord on", value=f"{member.created_at.strftime('%d %h %Y @ %H:%m %p')} (<t:{round(datetime.datetime.timestamp(member.created_at))}:R>)")
        embed.add_field(name="Joined guild on", value=f"{member.joined_at.strftime('%d %h %Y @ %H:%m %p')} (<t:{round(datetime.datetime.timestamp(member.joined_at))}:R>)")
        if bool(member.premium_since):
            embed.add_field(name="Boosted guild on", value=f"{member.premium_since.strftime('%d %h %Y @ %H:%m %p')} (<t:{round(datetime.datetime.timestamp(member.premium_since))}:R>)")
        else:
            embed.add_field(name="Boosted guild on", value=f"N/A")
        embed.add_field(name=f"Roles list [{len(role)}]", value=', '.join(role))
        if member.bot:
            try: important.remove("N/A")
            except: pass
            important.append("Discord Bot")
        if member.guild_permissions.administrator and not member is ctx.guild.owner:
            try: important.remove("N/A")
            except: pass
            important.append("Server Administrator")
        if member is ctx.guild.owner:
            try: important.remove("N/A")
            except: pass
            important.append("Server Owner")
        if bool(key_permissions) and not member.guild_permissions.administrator:
            embed.add_field(name="Key Permissions", value=key_permissions, inline=False)

        embed.set_footer(text=', '.join(important))

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(whois(client))