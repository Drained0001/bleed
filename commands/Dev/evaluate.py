import discord
from discord.ext import commands
from contextlib import redirect_stdout
import traceback
import textwrap
import io
import inspect
from pyfiglet import figlet_format
import json
import motor
import motor.motor_asyncio
from io import StringIO

class evaluate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_result = None

    @commands.command(pass_context=True, hidden=True, name="eval", description='Evaluates code (owner only')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates python code"""
        env = {
            "client": self.client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
            "source": inspect.getsource,
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        err = out = None
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            return await err.add_reaction("❌")
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            file=discord.File(StringIO(str(value)), "response.txt")
            await ctx.send(file=file)
        if out:
            await out.add_reaction("✔")
        if err:
            await err.add_reaction("❌")

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    def get_syntax_error(self, e):
        if e.text is None:
            return f"```py\n{e.__class__.__name__}: {e}\n```"
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

def setup(client):
    client.add_cog(evaluate(client))