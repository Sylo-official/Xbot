import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

print("TOKEN FOUND:", TOKEN is not None)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

bot.remove_command("help")

async def load_extensions():
    if not os.path.isdir("./cogs"):
        print("❌ No cogs folder found")
        return

    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
                print(f"Loaded extension: {file}")
            except Exception as e:
                print(f"Failed to load {file}: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

async def main():
    if not TOKEN:
        print("❌ No DISCORD_TOKEN found")
        return

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
