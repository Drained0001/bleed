import discord
import json

with open("./utils/config.json", "r") as f:
    data = json.load(f)

def approveEmbed(ctx, text):
    return discord.Embed(description=f"{data['emojis']['approve']} {ctx.author.mention}: {text}", color=int(data['colors']['approve'], 16))
    
def denyEmbed(ctx, text):
    return discord.Embed(description=f"{data['emojis']['deny']} {ctx.author.mention}: {text}", color=int(data['colors']['deny'], 16))

def warningEmbed(ctx, text):
    return discord.Embed(description=f"{data['emojis']['warn']} {ctx.author.mention}: {text}", color=int(data['colors']['warn'], 16))

def normalEmbed(ctx, text):
    return discord.Embed(description=f"{ctx.author.mention}: {text}", color=int(data['colors']['default'], 16))