import os
import asyncio
import threading
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

print("TOKEN FOUND:", TOKEN is not None)

# -------------------
# Flask setup (health check)
# -------------------
app = Flask(__name__)

@app.route("/health")
def health():
    return "ok", 200

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# -------------------
# Discord bot setup
# -------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

async def load_extensions():
    """Load all extensions from the cogs folder."""
    if not os.path.isdir("./cogs"):
        print("Error: cogs folder not found.")
        return

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded extension: {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

async def main():
    if not TOKEN:
        print("Error: No DISCORD_TOKEN found.")
        return

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

async def main():
    if not TOKEN:
        print("Error: No DISCORD_TOKEN found.")
        return

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
