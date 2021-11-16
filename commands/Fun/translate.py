import discord
from discord.ext import commands
from utils import embeds, user
import os
import psutil
import pytesseract
import cv2
import numpy as np
from PIL import Image
import requests
from deep_translator import GoogleTranslator

class translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["tr"], description="Translates text from image to printed text")
    async def translate(self, ctx, language="en", *, text):
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16) 
        translated = GoogleTranslator(source='auto', target=language).translate(text)
        embed = discord.Embed(title="Result", description=f"```{translated}```", color=color)
        embed.set_author(icon_url=user.av(ctx.author), name=ctx.author.name)
        embed.set_footer(text="Powered by Google Translate", icon_url="https://images-ext-2.discordapp.net/external/2X-ElcbGoaIJUc8yTuboiHqMF0N9C3dDUyOsT9n14po/https/bleed.bot/img/google.png")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(translate(client))