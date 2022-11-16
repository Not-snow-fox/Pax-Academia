# https://labs.everypixel.com/api/docs

import discord
from discord.commands import option
from discord.ext import commands
from util.EmbedBuilder import EmbedBuilder
from util.Logging import log

import os

import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("EVERYPIXEL_CLIENT_ID")
client_secret = os.getenv("EVERYPIXEL_CLIENT_SECRET")

# The user should attach an image as an input to the slash command. The bot will then send a message with the keywords that the image contains.

class Lens(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="lens", description="Returns the keywords of an image."
    )
    @option(
        name="image",
        description="The image to be analyzed.",
        type=11,
        required=True,
    )
    async def lens(self, ctx: commands.Context, image: discord.File) -> None:
        """
        It sends a message with the keywords that the image contains.

        :param ctx: commands.Context
        :type ctx: commands.Context
        :param image: str
        :type image: str
        :return: The return type is None.
        """
        url = "https://api.everypixel.com/v1/keywords"
        files = {"image": image.read()}
        response = requests.post(
            url, files=files, auth=(client_id, client_secret)
        )
        keywords = response.json()["keywords"]
        embed = EmbedBuilder(
            title="Lens",
            description=f"Keywords: {', '.join(keywords)}",
        )
        await ctx.send(embed=embed.build())



# {
#   "keywords": [
#     {"keyword": "Domestic Cat", "score": 0.98873621225357056},
#     {"keyword": "Pets", "score": 0.97396981716156006},
#     {"keyword": "Animal", "score": 0.94135761260986328},
#     {"keyword": "Cute", "score": 0.86750519275665283},
#     {"keyword": "Kitten", "score": 0.83549922704696655},
#     {"keyword": "Feline", "score": 0.74918556213378906},
#     {"keyword": "Domestic Animals", "score": 0.71088212728500366},
#     {"keyword": "Young Animal", "score": 0.703544020652771},
#     {"keyword": "Mammal", "score": 0.67086690664291382},
#     {"keyword": "Fur", "score": 0.61061191558837891}
#   ],
#   "status": "ok"
# }

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Lens(bot))