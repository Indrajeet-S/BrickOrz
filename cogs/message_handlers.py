import discord
import re
import random
from discord.ext import commands
from config import WELCOME_CHANNEL_ID, NOTIFICATION_CHANNEL_ID, LOG_CHANNEL_ID

class MessageHandlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.bot.process_commands(message)

        if message.channel.id == NOTIFICATION_CHANNEL_ID:
            await message.add_reaction('✅')

        if message.channel.id == WELCOME_CHANNEL_ID:
            emojis = ['👋', '<:blobbeat:1206994557137326110>', '\<:catKing:1206994563567452220>', '<:AC:1206994544306954313>', '<:ghosthug:1206994583578349598>', '\<:gigachad:1206994586636001281>', '\<:hype:1206994599885672519>', '\<:pkinglove:1206994630600818748>', '\<:prayge:1206994633305882686>', '<:proud:1206994636560670720>', '\<:redHandWin:1206994645016518656>', '\<:sir:1206994677644001361>', '\<:stickManLove:1206994683516157953>', '\<:yay:1206994703115886593>', '\<:yayy:1206994707020914719>', '\<:yesSir:1206994714570788874>']
            emoji = random.choice(emojis)
            await message.add_reaction(emoji)

        if "orz" in message.content.lower():
            await message.add_reaction('<:orz:1206994621360504852>')

        DISCORD_INVITE_PATTERN = r'discord(?:\.gg|app\.com\/invite)\/[^\s\/]+?'
        if re.search(DISCORD_INVITE_PATTERN, message.content, re.IGNORECASE):
            await self.handle_discord_invite(message)

    async def handle_discord_invite(self, message):
        try:
            await message.author.send(f"Hello {message.author.name}, 🚫 posting other Discord server invites is not allowed in '{message.guild.name}', to prevent spam! If the invite link is very important then you can send it to the respective person in DM 😳")
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(f"Invite link posted by {message.author} ({message.author.id}) in {message.channel} 🫣")
            await message.delete()
        except discord.HTTPException as e:
            print(f"Error: {e}")


