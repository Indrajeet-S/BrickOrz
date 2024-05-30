from discord.ext import commands
from config import LOG_CHANNEL_ID
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged on as {self.bot.user}!')
        await self.bot.change_presence(activity=discord.CustomActivity(name='QBit'))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if message.guild:
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                escaped_content = message.content.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                response = f"Deleted message by or of **{message.author}** 🧹 :\n{escaped_content}"
                await log_channel.send(response)

