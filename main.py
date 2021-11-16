import discord
from discord.ext import commands
import os
import json
import ast
import inspect
import re
import time
import pymongo
import motor
import motor.motor_asyncio

with open("./utils/config.json", "r") as f:
    data = json.load(f)

cluster = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{data['database']['username']}:{data['database']['password']}@cluster0.bp4ii.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["bleed"]["prefix"]

async def get_prefix(bleed, message):
    info = await database.find_one({"_id": message.guild.id})
    if not info:
        return ","
    return info['p']

bleed = commands.AutoShardedBot(command_prefix=get_prefix, intents=discord.Intents.all(), help_command=None, shard_count=1)
bleed.start_time = time.time()

bleed.load_extension(f"handlers.errors")
bleed.load_extension(f"handlers.join")
bleed.load_extension(f"test")

for folder in os.listdir("./commands"):
    for file in os.listdir(f"./commands/{folder}"):
        if file.endswith(".py"):
            bleed.load_extension(f"commands.{folder}.{file[:-3]}")

def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)

source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',  # hh this regex
    r"\1Discord Android\2",  # s: https://luna.gitlab.io/discord-unofficial-docs/mobile_indicator.html
    source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]

@bleed.event
async def on_ready():
    os.system("cls")
    print("Bleed is online")
    await bleed.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="the budget bleed"))

@bleed.check
async def no_dms(ctx):
    return ctx.guild is not None or await bleed.is_owner(ctx.author)

@bleed.command()
@commands.is_owner()
async def load(ctx, *, args):
    cogs = args.split(" ")
    errs = []
    msg = await ctx.send(embed = discord.Embed(description=f"Loading {len(cogs)} cogs", color=0x000001))
    for _ in cogs:
        try:
            bleed.load_extension(_)
            errs.append(f"load {_} | Success")
        except Exception as e:
            errs.append(f"{_} | {e}")

    e = "\n".join(errs)
    await msg.edit(embed = discord.Embed(description=f"Attempted to load cogs, logs:```\u200b{e}```", color=0x000001))

@bleed.command()
@commands.is_owner()
async def unload(ctx, *, args):
    cogs = args.split(" ")
    errs = []
    msg = await ctx.send(embed = discord.Embed(description=f"Unloading {len(cogs)} cogs", color=0x000001))
    for _ in cogs:
        try:
            bleed.unload_extension(_)
            errs.append(f"unload {_} | Success")
        except Exception as e:
            errs.append(f"{_} | {e}")

    e = "\n".join(errs)
    await msg.edit(embed = discord.Embed(description=f"Attempted to load cogs, logs:```\u200b{e}```", color=0x000001))

@bleed.command()
@commands.is_owner()
async def reload(ctx, *, args):
    cogs = args.split(" ")
    errs = []
    msg = await ctx.send(embed = discord.Embed(description=f"Reloading {len(cogs)} cogs", color=0x000001))
    for _ in cogs:
        try:
            bleed.unload_extension(_)
            errs.append(f"unload {_} | Success")
        except Exception as e:
            errs.append(f"{_} | {e}")
        try:
            bleed.load_extension(_)
            errs.append(f"load {_} | Success")
        except Exception as e:
            errs.append(f"{_} | {e}")

    e = "\n".join(errs)
    await msg.edit(embed = discord.Embed(description=f"Attempted to load cogs, logs:```\u200b{e}```", color=0x000001))

bleed.run(data["token"])