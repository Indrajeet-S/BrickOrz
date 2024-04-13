import discord
from discord.ext import commands
from config import BOT_TOKEN
import tracemalloc

tracemalloc.start()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='^', intents=intents)

async def load_extensions():
    cogs = [
        'cogs.events.Events',
        'cogs.message_handlers.MessageHandlers',
        'cogs.reaction_handlers.ReactionHandlers'
    ]

    for cog in cogs:
        try:
            # Split the module from the class dynamically, handling nested modules
            module_name, class_name = cog.rsplit('.', 1)
            module = __import__(module_name, fromlist=[class_name])
            cog_class = getattr(module, class_name)
            await bot.add_cog(cog_class(bot))
        except Exception as e:
            print(f'Failed to load cog {cog}: {e}')

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_extensions())
    bot.run(BOT_TOKEN)
