import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from utils import embeds, strings, user
import motor
import motor.motor_asyncio

def getconv(arg):
    final = "Unknown Argument"
    if arg == "str":
        final = "Text"
    if arg == "int":
        final = "a Number"
    return final

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        bucket = self.cd_mapping.get_bucket(ctx)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return
        try:
            if isinstance(error, commands.CommandNotFound):
                return
            elif isinstance(error, commands.BadArgument):
                remove = "\"."
                return await ctx.send(embed=embeds.warningEmbed(ctx, f"You didn't give a **valid {strings.remove_characters(str(error).split('parameter ')[1], remove)}** for the {ctx.command}"))
            elif isinstance(error, commands.MissingRequiredArgument):
                desc = lambda x : x.description if bool(x.description) else "No description added"
                embed = discord.Embed(title=f"Command: {ctx.command}", description=f"{desc(ctx.command)}\n```\nSyntax: {ctx.command} {ctx.command.signature}\nExample: {ctx.command.usage}```")
                embed.set_author(name=f"{self.client.user.name} help", icon_url=user.av(self.client.user))
                return await ctx.send(embed=embed)
            elif isinstance(error, commands.MissingPermissions):
                perm = str(error).split("missing ")[1].split(" permission(s)")[0]
                return await ctx.send(embed=embeds.warningEmbed(ctx, f"You're **missing** the permission: `{perm}`"))

            elif isinstance(error, commands.BotMissingPermissions):
                return await ctx.send(embed=embeds.warningEmbed(ctx, error.args))
            
            await ctx.send(embed=embeds.warningEmbed(ctx, error))
        except Exception as e:
            await ctx.send(embed=embeds.warningEmbed(ctx, e))

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(f"{ctx.command} -|- {ctx.author} -|- {ctx.guild}")

def setup(client):
    client.add_cog(Events(client))