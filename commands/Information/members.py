import discord
from discord import interactions
from discord.ext import commands
from utils import embeds
import datetime
import time
from discord.ui import button, View, Button
from discord.interactions import Interaction

class view(View):
    def __init__(self, bots, ctx):
        super().__init__(timeout=15)
        self.unlisted = bots
        self.bots = list(self.chunks(bots, 10))
        self.page = 0
        self.ctx = ctx

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @button(emoji='<:left:907492570274361354>', custom_id="back_button", style=discord.ButtonStyle.blurple)
    async def back(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:
            self.page -= 1
            if self.page < 0:
                self.page = len(self.bots) - 1

            color = self.ctx.author.color or int(embeds.data["colors"]["default"], 16)
            author_avatar = ''.join([self.ctx.author.avatar.url if self.ctx.author.avatar else self.ctx.author.default_avatar.url])
            text = '\n'.join(self.bots[self.page])

            embed = discord.Embed(title="List of members", description=text, color=color)
            embed.set_author(icon_url=author_avatar, name=self.ctx.author.name)
            embed.set_footer(text=f"Page {self.page+1}/{len(self.bots)} ({len(self.unlisted)} entries)")

            await interaction.response.edit_message(view=self, embed=embed)

    @button(emoji='<:right:907492572426010674>', custom_id="next_button", style=discord.ButtonStyle.blurple)
    async def next(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:
            self.page += 1
            if self.page > len(self.bots) - 1:
                self.page = 0

            color = self.ctx.author.color or int(embeds.data["colors"]["default"], 16)
            author_avatar = ''.join([self.ctx.author.avatar.url if self.ctx.author.avatar else self.ctx.author.default_avatar.url])
            text = '\n'.join(self.bots[self.page])

            embed = discord.Embed(title="List of members", description=text, color=color)
            embed.set_author(icon_url=author_avatar, name=self.ctx.author.name)
            embed.set_footer(text=f"Page {self.page+1}/{len(self.bots)} ({len(self.unlisted)} entries)")

            await interaction.response.edit_message(view=self, embed=embed)

    @button(emoji="<:cancel:907492568072335410>", custom_id="cancel_button", style=discord.ButtonStyle.red)
    async def cancel(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:
            await interaction.message.delete()

class members(commands.Cog):
    def __init__(self, client):
        self.client = client

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @commands.command(aliases=["inrole"], description="View members in a role")
    async def members(self, ctx, role: discord.Role = None):
        role = role or ctx.guild.default_role
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16)
        author_avatar = ''.join([ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url])
        bots = [m for m in ctx.guild.members if (role.id in [r.id for r in m.roles])]
        check_booster = lambda x : "<a:nitro:899479106884886558>" if bool(x.premium_since) else ""
        check_bot = lambda x : "<:bot:902735317709230111>" if x.bot else ""
        bots = [f"`{bots.index(m)+1}` **{m}** {check_booster(m)}{check_bot(m)}" for m in bots]

        if len(bots) < 10:
            embed = discord.Embed(title="List of members", description='\n'.join(bots), color=color)
            embed.set_author(icon_url=author_avatar, name=ctx.author.name)
            embed.set_footer(text=f"Page 1/1 ({len(bots)} entries)")
            return await ctx.send(embed=embed)
        
        embed = discord.Embed(title="List of members", description='\n'.join(list(self.chunks(bots, 10))[0]), color=color)
        embed.set_author(icon_url=author_avatar, name=ctx.author.name)
        embed.set_footer(text=f"Page 1/{len(list(self.chunks(bots, 10)))} ({len(bots)} entries)")

        await ctx.send(embed=embed, view=view(bots=bots, ctx=ctx))

def setup(client):
    client.add_cog(members(client))