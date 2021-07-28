import discord
import builtins
import sqlite3
import time
import os
from dotenv import load_dotenv
from prsaw import RandomStuff
from discord.ext import commands

db = sqlite3.connect("database.db")
builtins.db = db

class DevTools(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Let's us know when the bot comes online
    async def on_ready(self):
        print("Bot is ready.")


load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True

bot = DevTools(command_prefix="!", intents=intents, command_incensitive=True)
builtins.bot = bot

bot.launch_time = time.time()

from Cogs import chatbot, compile, music
bot.add_cog(chatbot.AIChatBot())
bot.add_cog(compile.Compiler())
bot.add_cog(music.Music())

bot.run(TOKEN)