import discord
from discord.ext import commands
from config import EMOJI_BOARD_CHANNEL_NAME


class ReactionHandlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sent_messages = set()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or reaction.message.id in self.sent_messages:
            return

        if reaction.count >= 3:
            reaction_board_channel = discord.utils.get(reaction.message.guild.channels, name=EMOJI_BOARD_CHANNEL_NAME)
            if not reaction_board_channel:
                print(f"Channel not found: {EMOJI_BOARD_CHANNEL_NAME}")
                return

            embed = discord.Embed(description=reaction.message.content, color=0xffac33)

            author = reaction.message.author
            embed.set_author(name=author.name, icon_url=author.avatar.url)

            embed.add_field(name="Original", value=f"[Source]({reaction.message.jump_url})", inline=True)

            if reaction.message.attachments:
                # Attempt to attach the first image to the embed
                for attachment in reaction.message.attachments:
                    if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpeg', 'jpg', 'gif', 'webp']):
                        embed.set_image(url=attachment.url)
                        break  # Only add the first image

            try:
                await reaction_board_channel.send(embed=embed)
                self.sent_messages.add(reaction.message.id) 
            except discord.DiscordException as e:
                print(f"Failed to send message: {e}")
