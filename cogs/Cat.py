import requests
from discord.ext import commands


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Cat(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="cat", description="Returns a random cat image.")
    async def cat(self, ctx: commands.Context) -> None:
        """
        It gets a random cat picture from the internet and sends it to the channel

        :param ctx: The context of where the command was used
        :type ctx: commands.Context
        """
        response = requests.get("https://aws.random.cat/meow")
        data = response.json()
        await ctx.respond(data["file"])


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Cat(bot))
