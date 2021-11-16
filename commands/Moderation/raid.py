import discord
from discord.ext import commands
import json
import datetime
from utils import strings, embeds
from discord.ext.commands import BucketType, cooldown
import time as t
import asyncio
import re

timeRegex = re.compile("([0-9]+)(s|m|h)")
punishmentRegex = re.compile("(kick|ban)")

class ApproveView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=15)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(emoji="<:accept:908154265162371082>", custom_id="yes", style=discord.ButtonStyle.green)
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id is self.ctx.author.id:
            self.value = "yes"
            for btn in self.children:
                btn.style = discord.ButtonStyle.grey
                btn.disabled = True
            await interaction.response.edit_message(view=self)
            self.stop()

    @discord.ui.button(emoji="<:cancel:907492568072335410>", custom_id="no", style=discord.ButtonStyle.red)
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id is self.ctx.author.id:
            self.value = "no"
            for btn in self.children:
                btn.style = discord.ButtonStyle.grey
                btn.disabled = True
            await interaction.response.edit_message(view=self)
            self.stop()

class raid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Remove all members that joined in the time provided in the event of a raid")
    @commands.has_permissions(administrator=True)
    async def raid(self, ctx, time, punishment):
        checkRegex = lambda x, y:[y.search(x).group(a+1) for a in range(y.groups)] if y.search(x) != None else "No match"
        if checkRegex(time.lower(), timeRegex) == "No match":
            raise commands.BadArgument(f'Converting to "time regex" failed for parameter "time".') 
        if checkRegex(punishment.lower(), punishmentRegex) == "No match":
            raise commands.BadArgument(f'Converting to "time regex" failed for parameter "punishment".') 

        time = checkRegex(time.lower(), timeRegex)

        constrain = lambda val, minv, maxv:minv if val < minv else maxv if val > maxv else val
        convert = lambda x, y:constrain(x, 1, 60) if y in ["s", "m"] else constrain(x, 1, 24)
        convertTime = lambda time, conversion:time if conversion == "s" else time * 60 if conversion == "m" else time * 60 * 60

        time = convertTime(int(convert(int(time[0]), time[1])), time[1])

        mems = []
        for member in [member for member in ctx.guild.members if not member in ctx.guild.premium_subscribers]:
            date = member.joined_at
            timestamp = t.time() - datetime.datetime.timestamp(date)
            
            if time > timestamp:
                mems.append(member)

        isPlural = lambda x:"members" if x != 1 else "member"

        view = ApproveView(ctx)
        msg = await ctx.send(embed=embeds.warningEmbed(ctx, f"Are you sure you want to **{punishment} {len(mems)} {isPlural(len(mems))}**?\n`(boosters are immune to this command)`"), view=view)

        await view.wait()
        if view.value is None:
            await msg.edit(embed=embeds.warningEmbed(ctx, "You took too long to answer, the process was cancelled."))
            return
        elif view.value == "yes":
            await msg.edit(embed=embeds.approveEmbed(ctx, f"Starting to {punishment} {len(mems)} {isPlural(len(mems))}."))
        else:
            await msg.edit(embed=embeds.approveEmbed(ctx, f"Alright I wont start to {punishment} {len(mems)} {isPlural(len(mems))} unless you change your mind."))
            return

        for member in mems:
            if punishment == "kick":
                await member.kick(reason=f"Potential raid. Moderator: {ctx.author}")

            if punishment == "ban":
                await member.ban(reason=f"Potential raid. Moderator: {ctx.author}")

        getAfter = lambda x:"banned" if x == "ban" else "kicked"

        await msg.edit(embed=embeds.approveEmbed(ctx, f"Successfully {getAfter(punishment)} {len(mems)} {isPlural(len(mems))}."))

def setup(client):
    client.add_cog(raid(client))