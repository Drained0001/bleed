import discord
from discord.ext import commands
import time
from utils import embeds
import json
import pymongo
import motor
import motor.motor_asyncio

with open("./utils/config.json", "r") as f:
    data = json.load(f)

cluster = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{data['database']['username']}:{data['database']['password']}@cluster0.bp4ii.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["bleed"]["prefix"]

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(description="View prefix", invoke_without_command=True)
    async def prefix(self, ctx):
        info = await database.find_one({"_id": ctx.guild.id})
        getPrefix = lambda x:x["p"] if x else ","
        await ctx.send(embed=embeds.normalEmbed(ctx, f"Guild prefix: `{getPrefix(info)}`"))

    @prefix.command(description="Set command prefix for guild", aliases=["add"])
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, prefix):
        info = await database.find_one({"_id": ctx.guild.id})
        getPrefix = lambda x:x if x else "No prefix"
        if getPrefix(info) == "No prefix":
            await database.insert_one({"_id": ctx.guild.id, "p": prefix})
        await database.update_one({"_id": ctx.guild.id}, {"$set":{"p": prefix}})
        await ctx.send(embed=embeds.approveEmbed(ctx, f"Replaced your current guild's prefix to `{prefix}`"))

    @prefix.command(description="Remove command prefix for guild", aliases=["delete", "del", "clear"])
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx):
        info = await database.find_one({"_id": ctx.guild.id})
        getPrefix = lambda x:x if x else "No prefix"
        if getPrefix(info) == "No prefix":
            return await ctx.send(embed=embeds.warningEmbed(ctx, "You dont currently have a custom prefix"))
        await database.update_one({"_id": ctx.guild.id}, {"$set":{"p": ","}})
        await ctx.send(embed=embeds.approveEmbed(ctx, f"Your guild's prefix has been **removed**. You can set a **new prefix** using `,prefix add <prefix>`"))

def setup(client):
    client.add_cog(prefix(client))