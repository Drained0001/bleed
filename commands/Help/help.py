import discord
from discord.ext import commands
from utils import embeds, user, strings
import datetime
import time
import os
import traceback
from discord.ui import button, View, Button
from discord.interactions import Interaction

def cmdInfo(command, client):
    desc = lambda x : x.description if bool(x.description) else "No description added"
    aliases = lambda x : ', '.join(x.aliases) if bool(x.aliases) else "N/A"
    params = lambda x : ', '.join(x.clean_params) if bool(x.clean_params) else "N/A"
    try:
        check = command.checks[0]
        print(check(0))
    except Exception as e:
        try:
            *frames, last_frame = traceback.walk_tb(e.__traceback__)
            frame = last_frame[0]
            info = f"{embeds.data['emojis']['warn']} {', '.join([' '.join(str(a).split('_')) for a in frame.f_locals['perms']])}"
        except:
            info = 'N/A'

    embed = discord.Embed(title=f"Command: {command}", description=f"{desc(command)}")
    embed.add_field(name="Aliases", value=aliases(command))
    embed.add_field(name="Parameters", value=params(command))
    embed.add_field(name="Information", value=info)
    embed.add_field(name="Usage", value=f"```\nSyntax: {command} {command.signature}\nExample: {command.usage}```", inline=False)
    embed.set_author(name=f"{client.user.name} help", icon_url=user.av(client.user))

    return embed

class view(View):
    def __init__(self, cmds, ctx, client):
        super().__init__(timeout=15)
        self.commands = cmds
        self.page = 0
        self.ctx = ctx
        self.client = client

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @button(emoji='<:left:907492570274361354>', custom_id="back_button", style=discord.ButtonStyle.blurple)
    async def back(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:
            self.page -= 1
            if self.page < 0:
                self.page = len(self.commands) - 1

            await interaction.response.edit_message(view=self, embed=cmdInfo(self.commands[self.page], self.client))

    @button(emoji='<:right:907492572426010674>', custom_id="next_button", style=discord.ButtonStyle.blurple)
    async def next(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:
            self.page += 1
            if self.page > len(self.commands) - 1:
                self.page = 0

            await interaction.response.edit_message(view=self, embed=cmdInfo(self.commands[self.page], self.client))

    @button(emoji="<:cancel:907492568072335410>", custom_id="cancel_button", style=discord.ButtonStyle.red)
    async def cancel(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:
            await interaction.message.delete()

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dont_show = ["Help", "Dev"]


    @commands.command(aliases=["commands"])
    async def help(self, ctx, command=None):
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16)
        author_avatar = ctx.author.display_avatar

        if command:
            try:
                command = self.client.get_command(command.lower())
                if getattr(command, 'commands', None) == None:
                    await ctx.send(embed=cmdInfo(command, self.client))
                else:
                    cmds = []
                    cmds.append(command)
                    for _ in command.commands:
                        cmds.append(self.client.get_command(f"{command.name} {_.name}"))
                    await ctx.send(embed=cmdInfo(command, self.client), view=view(cmds, ctx, self.client))
            except Exception as e:
                await ctx.send(embed=embeds.warningEmbed(ctx, e))
                return
            return
        
        embed = discord.Embed(description="[invite](https://discord.com/oauth2/authorize?client_id=907444482797084672&permissions=8&scope=bot)", timestamp=discord.utils.utcnow(), color=color)
        embed.set_author(icon_url=author_avatar, name=ctx.author.name)
        embed.set_footer(text=",help [command] gives you more information on a command")

        for folder in os.listdir("./commands"):
            if folder not in self.dont_show:
                cmds = []
                for file in os.listdir(f"./commands/{folder}"):
                    if file.endswith(".py"):
                        try:
                            cmd = self.client.get_command(file[:-3])
                            if not cmd.hidden:
                                cmds.append(f"`{cmd.name}`")
                                try:
                                    for b in cmd.commands:
                                        cmds.append(f'`{cmd.name} {b.name}`')
                                except:
                                    pass
                        except:
                            pass
                try:
                    embed.add_field(name=folder, value=', '.join(cmds), inline=False)   
                except:
                    pass

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(help(client))