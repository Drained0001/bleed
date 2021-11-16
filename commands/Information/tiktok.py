import discord
from discord.ext import commands
from utils import embeds
from TikTokApi import TikTokApi
import asyncio

class tiktok(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_user(self, username):
        try:
            api = TikTokApi.get_instance(custom_verifyFp="verify_63340ca6bf434df5cb6e38238b4407d7", use_test_endpoints=True)
            return api.get_user(username, custom_verifyFp="verify_63340ca6bf434df5cb6e38238b4407d7")
        except:
            return "err"
    
    @commands.command(aliases=["tt"], description="Shows information on a tiktok account")
    async def tiktok(self, ctx, username):
        
        async with ctx.channel.typing():
            user = self.get_user(username)
            if user == "err":
                return await ctx.send(embed=embeds.warningEmbed(ctx, f"[**{username}**](https://tiktok.com/@{username}) is an invalid **TikTok** account"))

            color = discord.Color.dark_magenta()
            stats = user['userInfo']['stats']
            avatar = user['userInfo']['user']['avatarThumb']
            av = lambda x : x.avatar.url if x.avatar else x.default_avatar

            embed = discord.Embed(description=f"[**{username}**](https://tiktok.com/@{username})", color=color)
            embed.set_thumbnail(url=avatar)
            embed.set_author(name=ctx.author.name, icon_url=av(ctx.author))
            embed.add_field(name="Likes", value="{:,}".format(stats["heart"]), inline=True)
            embed.add_field(name="Followers", value="{:,}".format(stats["followerCount"]), inline=True)
            embed.add_field(name="Following", value="{:,}".format(stats["followingCount"]), inline=True)

            await ctx.send(embed=embed)
            return
        

def setup(client):
    client.add_cog(tiktok(client))