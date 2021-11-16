import discord
from discord.ext import commands
import time as t
from utils import embeds
import asyncio

class Counter(discord.ui.View):
    def __init__(self, time, question, end):
        super().__init__(timeout=time)
        self.cache = {}
        self.message = None
        self.question = question
        self.time = time
        self.end = end
        self.yes = 0
        self.no = 0

    @discord.ui.button(label='0', emoji="<:accept:908154265162371082>", custom_id="yes", style=discord.ButtonStyle.green)
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id not in self.cache:
            number = int(button.label)
            button.label = str(number + 1)
            self.yes += 1
            self.cache[interaction.user.id] = "yes" 
            await interaction.response.edit_message(view=self)
        elif self.cache[interaction.user.id] == "no":
            for _ in self.children:
                if _.custom_id == "no":
                    number = int(_.label)
                    _.label = str(number - 1)
                    self.no -= 1
                    self.cache.pop(interaction.user.id)
                    number = int(button.label)
                    button.label = str(number + 1)
                    self.yes += 1
                    self.cache[interaction.user.id] = "yes" 
                    await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message('You already voted!', ephemeral=True)

    @discord.ui.button(label='0', emoji="<:cancel:907492568072335410>", custom_id="no", style=discord.ButtonStyle.red)
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id not in self.cache:
            number = int(button.label)
            button.label = str(number + 1)
            self.no += 1
            self.cache[interaction.user.id] = "no" 
            await interaction.response.edit_message(view=self)
        elif self.cache[interaction.user.id] == "yes":
            for _ in self.children:
                if _.custom_id == "yes":
                    number = int(_.label)
                    _.label = str(number - 1)
                    self.yes -= 1
                    self.cache.pop(interaction.user.id)
                    number = int(button.label)
                    button.label = str(number + 1)
                    self.no += 1
                    self.cache[interaction.user.id] = "no" 
                    await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message('You already voted!', ephemeral=True)

    async def on_timeout(self):
        await self.message.edit(embed=discord.Embed(description=f"**Poll results:**\n\n`Question`: {self.question}\n{embeds.data['emojis']['approve']} `Yes`: {self.yes}\n{embeds.data['emojis']['deny']} `No`: {self.no}", timestamp=discord.utils.utcnow()))

class poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Create a short poll")
    async def poll(self, ctx, time:int, *, question):
        ends = round(t.time()+time)
        view = Counter(time, question, f"<t:{ends}:R>")
        msg = await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} asks:\n{question}\n\nends <t:{ends}:R>", timestamp=discord.utils.utcnow()).set_footer(text="You may only add one vote, voting is anonymous."), view=view)
        view.message = msg
        await asyncio.sleep(time)
        await view.on_timeout()
        view.stop()

def setup(client):
    client.add_cog(poll(client))