import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    """Loads all extensions from the cogs directory."""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded extension: {filename}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

async def main():
    async with bot:
        await load_extensions()
        if TOKEN:
            await bot.start(TOKEN)
        else:
            print("Error: No DISCORD_TOKEN found in .env file.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
