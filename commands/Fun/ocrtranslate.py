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

class ocrtranslate(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_string(self, img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        cv2.imwrite("./ocr/removed_noise.png", img)
        cv2.imwrite(img_path, img)

        pytesseract.pytesseract.tesseract_cmd = "./ocr/tess/tesseract.exe"
        
        result = pytesseract.image_to_string(Image.open(img_path))
        return result

    @commands.command(aliases=["ocrtr"], description="Translates text from image to printed text")
    async def ocrtranslate(self, ctx, language="en"):
        color = ctx.author.color or int(embeds.data["colors"]["default"], 16) 
        try:
            url = ctx.message.attachments[0].url
        except:
            return await ctx.send(embed=embeds.warningEmbed(ctx, "You need to attach a image."))
        r = requests.get(url)
        filename = "./ocr/img.png"
        with open(filename, 'wb') as out_file:
            out_file.write(r.content)
        ocr = self.get_string("./ocr/img.png")
        try:
            if not ocr:
                ocr = "No results found"
            translated = GoogleTranslator(source='auto', target=language).translate(ocr)
            embed = discord.Embed(title="Result", description=f"```{translated}```", color=color)
            embed.set_author(icon_url=user.av(ctx.author), name=ctx.author.name)
            embed.set_footer(text="Optical Character Recognition", icon_url="https://images-ext-2.discordapp.net/external/2X-ElcbGoaIJUc8yTuboiHqMF0N9C3dDUyOsT9n14po/https/bleed.bot/img/google.png")
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)
        except:
            pass

def setup(client):
    client.add_cog(ocrtranslate(client))