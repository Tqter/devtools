import discord
import datetime
import re
from builtins import bot, db
from discord.ext import commands
import Utils.utils as utils

class Compiler(commands.Cog):
    def __init__(self):
        self.bot = bot
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

    @property
    def session(self):
        return self.bot.http._HTTPClient__session

    async def _run_code(self, *, lang: str, code: str):
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code},
        )
        return await res.json()

    @commands.command()
    async def run(self, ctx: commands.Context, *, codeblock: str):
        """
        Run code and get results instantly
        **Note**: You must use codeblocks around the code
        """
        matches = self.regex.findall(codeblock)
        if not matches:
            return await ctx.reply(
                embed=discord.Embed(
                    title=":octagonal_sign:Whoops!", description="Make sure you put your code in a codeblock!", color=discord.Color.red()
                )
            )
        lang = matches[0][0] or matches[0][1]
        if not lang:
            return await ctx.reply(
                embed=discord.Embed(
                    title=":octagonal_sign:Whoops!",
                    description="Couldn't find the language hinted in the codeblock or before it!!",
                    color=discord.Color.red()
                )
            )
        code = matches[0][2]
        result = await self._run_code(lang=lang, code=code)

        await self._send_result(ctx, result)

    @commands.command()
    async def runl(self, ctx: commands.Context, lang: str, *, code: str):
        """
        Run a single line of code, **must** specify language as first argument
        """
        result = await self._run_code(lang=lang, code=code)
        await self._send_result(ctx, result)

    async def _send_result(self, ctx: commands.Context, result: dict):
        if "message" in result:
            return await ctx.reply(
                embed=discord.Embed(
                    title=":octagonal_sign:Whoops!", description=result["message"], color=discord.Color.red()
                )
            )
        output = result["output"]
        #        if len(output) > 2000:
        #            url = await create_guest_paste_bin(self.session, output)
        #            return await ctx.reply("Your output was too long, so here's the pastebin link " + url)
        embed = discord.Embed(title=f"Ran your {result['language']} code!", color=discord.Color.green())
        output = output[:500]
        shortened = len(output) > 500
        lines = output.splitlines()
        shortened = shortened or (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * "\n\n**Output shortened**"
        embed.add_field(name="Output:", value=f"`{output}`" or "**No output**")

        await ctx.reply(embed=embed)