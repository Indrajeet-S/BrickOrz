import discord
from discord.ext import commands
import random
import re
from dtoken import BOT_TOKEN


# Define which intents your bot requires
intents = discord.Intents.default()
intents.messages = True  # Allows the bot to receive messages
intents.message_content = True  # This is the crucial part for your warning


# Initialize your bot with the specified intents
bot = commands.Bot(command_prefix='/', intents=intents)




# ----------------------BOT COMMANDS code ------------------------------------
@bot.command()
async def testt(ctx):
    """Responds with a simple message to show the command is working."""
    await ctx.send('This is a test command!')



# ----------------------BOT EVENTS code ------------------------------------
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')



# The rest of your event listeners can remain under this Bot instance
@bot.event
async def on_message(message):
    # Make sure to process commands, otherwise commands won't work.
    await bot.process_commands(message)

    # Your existing on_message code here
    # Remember, the rest of your on_message logic goes here
    if message.author.bot:
        return
    
    # print(f'Message from {message.author}: {message.content}')
    # Add your logic for message reactions and other responses

    ### 1) Adding random welcome reaction emojis to each message in a particular channel 
    if message.channel.id == 1191356341885878302:
        emojis = ['<:blobbeat:1206994557137326110>', '\<:catKing:1206994563567452220>', '<:AC:1206994544306954313>', '<:ghosthug:1206994583578349598>', '\<:gigachad:1206994586636001281>', '\<:hype:1206994599885672519>', '\<:pkinglove:1206994630600818748>', '\<:prayge:1206994633305882686>', '<:proud:1206994636560670720>', '\<:redHandWin:1206994645016518656>', '\<:sir:1206994677644001361>', '\<:stickManLove:1206994683516157953>', '\<:yay:1206994703115886593>', '\<:yayy:1206994707020914719>', '\<:yesSir:1206994714570788874>', '👋'] # 16 emojis
        emoji = random.choice(emojis)

        try:
            await message.add_reaction(emoji)
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")



    ### 2) Reacting with "orz" emoji 
    orz_emoji = '<:orz:1206994621360504852>'
    # Check if "orz" is in the message content
    if "orz" in message.content.lower():  # This makes it case-insensitive
            
        try:
            await message.add_reaction(orz_emoji)
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")

    # Add orz reaction emoji to orz emoji 
    specific_emoji_pattern = r'<:orz:\d+>'
    if re.search(specific_emoji_pattern, message.content):

        try:
            await message.add_reaction(orz_emoji)
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")

    # Add orz reaction emoji to 🛐
    required_emoji = '🛐'
    if required_emoji in message.content:
        try:
            await message.add_reaction(orz_emoji)
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")




    ### 3) Reacting with "✅" to notification msgs 
    if message.channel.id == 1206991455164440647:
        try:
            await message.add_reaction('✅')  
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")



    ### 4)  Discord invite link pattern
    DISCORD_INVITE_PATTERN = r'discord(?:\.gg|app\.com\/invite)\/[^\s\/]+?'

    # ID of the private channel where you want to log the invite links
    LOG_CHANNEL_ID = 1194697094733246464 

    # Check for Discord invite links in the message
    if re.search(DISCORD_INVITE_PATTERN, message.content, re.IGNORECASE):
        try:
            # Send a warning message directly to the user, including the server name and an emoji
            await message.author.send(f"Hello {message.author.name}, 🚫 posting other Discord server invites is not allowed in '{message.guild.name}'! If the invite link is very important then you can send it to the respective person in DM & not here on the server 😳 ")

            # Log the details of the message in the designated private channel
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(f"User {message.author} ({message.author.id}) posted a disallowed invite link 🫣 in {message.channel}: {message.content}")

            # Delete the message containing the invite link
            await message.delete()
        except discord.Forbidden:
            print(f"Could not send a DM to {message.author.name} or post in the log channel. They might have DMs disabled for non-friends, or the bot might not have permissions.")
        except discord.HTTPException as e:
            print(f"Failed to send message or log due to an HTTP exception: {e}")



    ### 69 importance msg
    if message.content == '!69':
            youtube_url = '<https://youtu.be/B6_iQvaIjXw?si=LoF4q1b1T_Bfybnf>'  # Ariana Grande - 34+35 (official video)
            # add two carets around the link, e.g. <https://youtu.be/B6_iQvaIjXw\>, and it'll stop being embedded on YT link
            await message.channel.send("The number **69** is interesting!\n"
                                        "Here's a fun fact: **(6*9)+6+9 = 69**\n"
                                        "**[34 + 35](" + youtube_url + ") = 69**  \n"
                                    )




# Send the msg to reaction-board when one emoji's reaction count reaches >=4
@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is not from a bot
    if not user.bot:
        # Check if the reaction count meets or exceeds the threshold (4 or more in this case)
        if reaction.count >= 4:
            # Find the channel named "reaction-board" in the server
            reactionboard_channel = discord.utils.get(reaction.message.guild.channels, name="⚡︱reaction-board")
            if reactionboard_channel:
                # Prepare the message to send to the reaction-board channel
                embed = discord.Embed(description=reaction.message.content, color=0xffac33)
                embed.add_field(name="Author", value=f"{reaction.message.author.name}", inline=True)
                embed.add_field(name="Original", value=f"[Jump to message]({reaction.message.jump_url})", inline=True)
                await reactionboard_channel.send(embed=embed)



@bot.event
async def on_message_delete(message):
    # Check if the message was deleted in a guild and not a DM
    if message.guild:
        log_channel_id = 1194697094733246464
        log_channel = bot.get_channel(log_channel_id)

        if log_channel:
            # Format the message
            author = message.author
            content = message.content or "[Message had no text]"
            response = f" Deleted message by/of **{author.name}** 🧹 :\n{content}"

            # Send the message to the log channel
            await log_channel.send(response)




# Run the bot
bot.run(BOT_TOKEN)
