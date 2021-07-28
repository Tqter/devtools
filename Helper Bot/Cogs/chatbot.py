import discord
import datetime
from builtins import bot, db
from discord.ext import commands
import Utils.utils as utils
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement

chatbot = ChatBot("HentAI", storage_adapter="chatterbot.storage.SQLStorageAdapter")

trainer = ChatterBotCorpusTrainer(chatbot)
 

class AIChatBot(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await bot.get_context(message)

        async with ctx.typing():

            if self.bot.user == message.author:
                return

            if message.content.startswith("!"):
                return

            if message.channel.id == utils.get_ai_channel(ctx.guild.id):
        
                try:
                    bot_input = chatbot.get_response(message.content)
                    await message.channel.send(bot_input)

                except(KeyboardInterrupt, EOFError, SystemExit):
                    await ctx.send("Error")

        await bot.process_commands(message)

    @commands.command()
    async def setchannel(self, ctx):
        db.execute("UPDATE guilds SET AIChannel = ? WHERE GuildID = ?", (ctx.channel.id, ctx.guild.id))
        db.commit()
        await ctx.send(f"Set AI Channel to `{ctx.channel.name}`!")