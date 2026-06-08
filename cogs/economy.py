import discord
from discord.ext import commands
import random
import asyncio

# -----------------------
# Storage (temporary)
# -----------------------
balances = {}
stocks = {}

# -----------------------
# Stock updater loop
# -----------------------
async def update_stocks():
    while True:
        await asyncio.sleep(1)
        for stock in stocks.values():
            change = random.uniform(-0.10, 0.32)
            stock["price"] = max(0.01, round(stock["price"] + change, 2))


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stock_task = bot.loop.create_task(update_stocks())

    # -----------------------
    # BALANCE
    # -----------------------
    @commands.command()
    async def balance(self, ctx):
        user_id = ctx.author.id
        bal = balances.get(user_id, 0)

        embed = discord.Embed(
            title="💰 Wallet",
            description=f"{ctx.author.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Balance", value=f"${bal}", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)

        await ctx.send(embed=embed)

    # -----------------------
    # SPIN
    # -----------------------
    @commands.command()
    async def spin(self, ctx):
        user_id = ctx.author.id

        win = random.choice([True, False])
        amount = random.randint(10, 200)

        if win:
            balances[user_id] = balances.get(user_id, 0) + amount

            embed = discord.Embed(
                title="🎰 Spin Result",
                description=f"You won **${amount}**!",
                color=discord.Color.green()
            )
        else:
            balances[user_id] = max(0, balances.get(user_id, 0) - amount)

            embed = discord.Embed(
                title="🎰 Spin Result",
                description=f"You lost **${amount}**...",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

    # -----------------------
    # STOCK LIST
    # -----------------------
    @commands.command()
    async def stocks(self, ctx):
        if not stocks:
            embed = discord.Embed(
                title="📉 Stock Market",
                description="No stocks available yet.",
                color=discord.Color.dark_grey()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="📊 Stock Market",
            color=discord.Color.blurple()
        )

        for name, data in stocks.items():
            embed.add_field(
                name=f"📈 {name}",
                value=f"Price: **${data['price']}**",
                inline=False
            )

        await ctx.send(embed=embed)

    # -----------------------
    # ADD STOCK (ADMIN)
    # -----------------------
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addstocks(self, ctx, name: str, price: float):

        if name in stocks:
            embed = discord.Embed(
                title="⚠️ Error",
                description="Stock already exists.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        stocks[name] = {
            "price": price,
            "owner": ctx.author.id
        }

        embed = discord.Embed(
            title="📈 Stock Created",
            description=f"**{name}** launched at **${price}**",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Created by {ctx.author}")

        await ctx.send(embed=embed)

    # -----------------------
    # BUY STOCK
    # -----------------------
    @commands.command()
    async def buy(self, ctx, name: str, amount: int = 1):
        user_id = ctx.author.id

        if name not in stocks:
            embed = discord.Embed(
                title="❌ Error",
                description="Stock not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        cost = stocks[name]["price"] * amount
        bal = balances.get(user_id, 0)

        if bal < cost:
            embed = discord.Embed(
                title="💸 Not Enough Money",
                description=f"You need **${cost}** but only have **${bal}**",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        balances[user_id] = bal - cost

        embed = discord.Embed(
            title="📈 Investment Successful",
            description=f"Bought **{amount}x {name}** for **${cost}**",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))
