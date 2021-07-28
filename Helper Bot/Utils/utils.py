import sqlite3
import discord
import os
from prsaw import RandomStuff
import builtins
from discord.ext import commands
from builtins import bot, db


rs = RandomStuff(async_mode=True, api_key=os.getenv("PRSAW_KEY"))


async def generate_table():
    db.execute("drop table if exists guilds")
    db.execute("""
    CREATE TABLE guilds (
        GuildID integer PRIMARY KEY,
        AIChannel integer
    );""")
    db.commit()

def get_ai_channel(guild_id):
    data = db.execute("select AIChannel from guilds where GuildId = ?", (guild_id,)).fetchone()
    if data is None:
        db.execute("insert into guilds (GuildID) values (?)", (guild_id,))
        db.commit()
    else:
        return data[0]