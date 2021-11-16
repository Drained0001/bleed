import discord
from discord.ext import commands
from utils import embeds, user
from discord.ui import button, View, Button
from discord.interactions import Interaction
import random

class view(View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.key = {
            "rock": ["paper"],
            "paper": ["scissors"],
            "scissors": ["rock"]
        }
        self.choice = random.choice(["rock", "paper", "scissors"])

    def winner(self, choice):
        if self.choice == choice:
            return "we tied"
        elif choice in self.key[self.choice]:
            return "you won"
        else:
            return "you lost"

    @button(emoji='🪨', custom_id="back_button", style=discord.ButtonStyle.blurple)
    async def back(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:

            color = self.ctx.author.color or int(embeds.data["colors"]["default"], 16)
            author_avatar = user.av(self.ctx.author)

            embed = discord.Embed(title="Rock Paper Scissors", description=f"You chose rock, I chose {self.choice}. {self.winner('rock')}", color=color)
            embed.set_author(icon_url=author_avatar, name=self.ctx.author.name)

            for btn in self.children:
                if self.winner('rock') == "you won": btn.style = discord.ButtonStyle.green
                if self.winner('rock') == "you lost": btn.style = discord.ButtonStyle.red
                if self.winner('rock') == "we tied": btn.style = discord.ButtonStyle.grey
                btn.disabled = True

            await interaction.response.edit_message(view=self, embed=embed)

    @button(emoji='📄', custom_id="next_button", style=discord.ButtonStyle.blurple)
    async def next(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:

            color = self.ctx.author.color or int(embeds.data["colors"]["default"], 16)
            author_avatar = user.av(self.ctx.author)

            embed = discord.Embed(title="Rock Paper Scissors", description=f"You chose paper, I chose {self.choice}. {self.winner('paper')}", color=color)
            embed.set_author(icon_url=author_avatar, name=self.ctx.author.name)

            for btn in self.children:
                if self.winner('paper') == "you won": btn.style = discord.ButtonStyle.green
                if self.winner('paper') == "you lost": btn.style = discord.ButtonStyle.red
                if self.winner('paper') == "we tied": btn.style = discord.ButtonStyle.grey
                btn.disabled = True

            await interaction.response.edit_message(view=self, embed=embed)

    @button(emoji="✂️", custom_id="scissors", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: Button, interaction: Interaction):
        if interaction.user == self.ctx.author:

            color = self.ctx.author.color or int(embeds.data["colors"]["default"], 16)
            author_avatar = user.av(self.ctx.author)

            embed = discord.Embed(title="Rock Paper Scissors", description=f"You chose scissors, I chose {self.choice}. {self.winner('scissors')}", color=color)
            embed.set_author(icon_url=author_avatar, name=self.ctx.author.name)

            for btn in self.children:
                if self.winner('scissors') == "you won": btn.style = discord.ButtonStyle.green
                if self.winner('scissors') == "you lost": btn.style = discord.ButtonStyle.red
                if self.winner('scissors') == "we tied": btn.style = discord.ButtonStyle.grey
                btn.disabled = True

            await interaction.response.edit_message(view=self, embed=embed)

class rockpaperscissors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["rps"], description="Play rock paper scissors with me!")
    async def rockpaperscissors(self, ctx):
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16) 
        
        await ctx.send(embed=discord.Embed(color=color, description=f"{ctx.author.mention}: Choose a option below."), view=view(ctx))

def setup(client):
    client.add_cog(rockpaperscissors(client))