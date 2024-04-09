import discord
import random
import re
from dtoken import BOT_TOKEN

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

# Brick Orz code
@client.event

async def on_message(message):
    # 1) Adding random welcome reaction emojis to each message in a particular channel 
    if message.channel.id == 1191356341885878302 and not message.author.bot:
        emojis = ['<:blobbeat:1206994557137326110>', '\<:catKing:1206994563567452220>', '<:AC:1206994544306954313>', '<:ghosthug:1206994583578349598>', '\<:gigachad:1206994586636001281>', '\<:hype:1206994599885672519>', '\<:pkinglove:1206994630600818748>', '\<:prayge:1206994633305882686>', '<:proud:1206994636560670720>', '\<:redHandWin:1206994645016518656>', '\<:sir:1206994677644001361>', '\<:stickManLove:1206994683516157953>', '\<:yay:1206994703115886593>', '\<:yayy:1206994707020914719>', '\<:yesSir:1206994714570788874>', '👋'] # 16 emojis
        emoji = random.choice(emojis)

        try:
            await message.add_reaction(emoji)
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")


    # 2) Reacting with "orz" emoji 
    if not message.author.bot:  # Check if the message is not sent by a bot
        # Check if "orz" is in the message content
        if "orz" in message.content.lower():  # This makes it case-insensitive
            custom_emoji = '<:orz:1206994621360504852>'
            
            try:
                await message.add_reaction(custom_emoji)
            except discord.HTTPException as e:
                print(f"Failed to add reaction: {e}")


    # 3) Reacting with "✅" to notification msgs 
    if message.channel.id == 1206991455164440647 and not message.author.bot:
        try:
            await message.add_reaction('✅')  
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")


    # 4) 
    # Discord invite link pattern
    DISCORD_INVITE_PATTERN = r'discord(?:\.gg|app\.com\/invite)\/[^\s\/]+?'

    # ID of the private channel where you want to log the invite links
    LOG_CHANNEL_ID = 1194697094733246464 

    # Check for Discord invite links in the message
    if re.search(DISCORD_INVITE_PATTERN, message.content, re.IGNORECASE):
        try:
            # Send a warning message directly to the user, including the server name and an emoji
            await message.author.send(f"Hello {message.author.name}, 🚫 posting other Discord server invites is not allowed in '{message.guild.name}'! If the invite link is very important then you can send it to the respective person in DM & not here on the server 😳 ")

            # Log the details of the message in the designated private channel
            log_channel = client.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(f"User {message.author} ({message.author.id}) posted a disallowed invite link in {message.channel}: {message.content}")

            # Delete the message containing the invite link
            await message.delete()
        except discord.Forbidden:
            print(f"Could not send a DM to {message.author.name} or post in the log channel. They might have DMs disabled for non-friends, or the bot might not have permissions.")
        except discord.HTTPException as e:
            print(f"Failed to send message or log due to an HTTP exception: {e}")



# Run the bot 
client.run(BOT_TOKEN)
