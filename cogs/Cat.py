from io import BytesIO

import aiohttp
import discord
from discord.ext import commands

from util.EmbedBuilder import EmbedBuilder


class Cat(commands.Cog):
    @commands.slash_command(name="cat", description="Sends a random cat image.")
    async def cat(self, ctx: commands.Context) -> None:
        """
        It gets a random cat image from the internet and sends it to the channel

        :param ctx: commands.Context
        :type ctx: commands.Context
        :return: None.
        """
        api = "https://cataas.com/cat"
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as resp:
                if resp.status != 200:
                    await ctx.send(
                        embed=EmbedBuilder(
                            title="Cat",
                            description="An error occurred while processing the image.",
                        ).build()
                    )
                    return
                data = await resp.read()
                await ctx.send(
                    file=discord.File(fp=BytesIO(data), filename="cat.png")
                )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Cat())
