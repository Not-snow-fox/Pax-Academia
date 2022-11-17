# https://labs.everypixel.com/api/docs

import os
import string

import discord
import requests
from discord.commands import option
from discord.ext import commands
from dotenv import load_dotenv

from util.EmbedBuilder import EmbedBuilder
from util.Logging import log

load_dotenv()

CLIENT_ID = os.getenv("EVERYPIXEL_CLIENT_ID")
CLIENT_SECRET = os.getenv("EVERYPIXEL_CLIENT_SECRET")

class Lens(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="lens", description="Returns the keywords of an image."
    )
    @option(
        name="image",
        description="The image to be analyzed.",
        required=True,
    )
    async def lens(self, ctx: commands.Context, attachment: discord.Attachment) -> None:
        """
        It takes an image attachment, sends it to the EveryPixel API, and returns the keywords of the image
        
        :param ctx: The context of the command
        :type ctx: commands.Context
        :param attachment: discord.Attachment
        :type attachment: discord.Attachment
        :return: The response is a JSON object.
        """
        url = "https://api.everypixel.com/v1/keywords"
        files = {"data": await attachment.read()}
        response = requests.post(
            url, files=files, auth=(CLIENT_ID, CLIENT_SECRET)
        )
        if response.json()["status"] == "error":
            await ctx.respond(
                embed=EmbedBuilder(
                    title="Lens",
                    description="An error occurred while processing the image.",
                ).build()
            )
            return
        keywords = response.json()

        embed = EmbedBuilder(
            title="Lens",
            description="The keywords of the image are:",
            image=attachment.url,
            fields=[
                [string.capwords(keyword["keyword"]), f"{keyword['score'] * 100:.2f}%", True]
                for keyword in keywords["keywords"]
            ],
        ).build()
        await ctx.respond(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Lens(bot))