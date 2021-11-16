import discord
from discord.ext import commands
from utils import embeds, user
from googleapiclient import discovery
import json

API_KEY = embeds.data["api-keys"]["google-pers"]

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

class tone(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["perspective"], description="Run Google Perspective on text")
    async def tone(self, ctx, *, text):
        all_attrs = ['TOXICITY', 'UNSUBSTANTIAL', 'OBSCENE', 'LIKELY_TO_REJECT', 'INFLAMMATORY', 'OFF_TOPIC', 'ATTACK_ON_AUTHOR', 'INCOHERENT', 'ATTACK_ON_COMMENTER']
        analyze_request = {
            'comment': { 'text': text },
            'requestedAttributes': {'TOXICITY': {}, 'UNSUBSTANTIAL': {}, 'OBSCENE': {}, 'LIKELY_TO_REJECT': {}, 'INFLAMMATORY': {}, 'OFF_TOPIC': {}, 'ATTACK_ON_AUTHOR': {}, 'INCOHERENT': {}, 'ATTACK_ON_COMMENTER': {}}
        }
        try:
            response = client.comments().analyze(body=analyze_request).execute()
        except:
            return await ctx.send(embed=embeds.warningEmbed(ctx, "There was a error getting a response. Please try different text."))
        data = json.dumps(response, indent=4)
        data = json.loads(data)

        embed = discord.Embed(description=f"```{text}```", timestamp=discord.utils.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=user.av(ctx.author))
        embed.set_footer(icon_url="https://images-ext-2.discordapp.net/external/j9IPWMPnksiDEEVSu2yNVw7zEiyQ99DEg6ZHY47fg50/https/images-ext-2.discordapp.net/external/Ej-SXXwLSw8GEK2rVCZm0zTeWTys0Wt66MpT3yuoOMU/https/cdn.discordapp.com/app-icons/324663951704981505/77cd059ce8a8c7a877cf2bf89ccc1b52.jpg", text="Powered by Google Perspective")
        for a in all_attrs:
            embed.add_field(name=a, value=f'{round(data["attributeScores"][a]["summaryScore"]["value"]*100, 1)}%')

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(tone(client))