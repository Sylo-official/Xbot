import discord
from discord.ext import commands
import random
import asyncio

# -----------------------
# DATA STORAGE
# -----------------------
balances = {}
stocks = {}
portfolio = {}  # user_id -> {stock: shares}

# -----------------------
# STOCK ENGINE
# -----------------------
async def stock_engine():
    while True:
        await asyncio.sleep(1)

        for name, stock in stocks.items():
            # normal random movement
            change = random.uniform(-0.10, 0.32)
            stock["price"] = max(0.01, round(stock["price"] + change, 2))

            # 💥 crash event (rare)
            if random.randint(1, 120) == 1:
                crash_drop = random.uniform(0.3, 0.7)  # 30%–70% drop
                stock["price"] = round(stock["price"] * (1 - crash_drop), 2)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(stock_engine())

    # -----------------------
    # BALANCE
    # -----------------------
    @commands.command()
    async def balance(self, ctx):
        bal = balances.get(ctx.author.id, 0)

        embed = discord.Embed(
            title="💰 Wallet",
            description=f"${bal}",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    # -----------------------
    # PORTFOLIO
    # -----------------------
    @commands.command()
    async def portfolio(self, ctx):
        user_id = ctx.author.id
        user_port = portfolio.get(user_id, {})

        embed = discord.Embed(
            title="📊 Your Portfolio",
            color=discord.Color.blurple()
        )

        if not user_port:
            embed.description = "You own no stocks yet."
            return await ctx.send(embed=embed)

        total_value = 0

        for stock_name, shares in user_port.items():
            if stock_name in stocks:
                price = stocks[stock_name]["price"]
                value = price * shares
                total_value += value

                embed.add_field(
                    name=stock_name,
                    value=f"{shares} shares | Value: ${round(value,2)}",
                    inline=False
                )

        embed.add_field(
            name="Total Portfolio Value",
            value=f"${round(total_value,2)}",
            inline=False
        )

        await ctx.send(embed=embed)

    # -----------------------
    # INVEST (BUY STOCK)
    # -----------------------
    @commands.command()
    async def invest(self, ctx, name: str, amount: int = 1):
        user_id = ctx.author.id

        if name not in stocks:
            return await ctx.send("❌ Stock not found.")

        cost = stocks[name]["price"] * amount
        bal = balances.get(user_id, 0)

        if bal < cost:
            return await ctx.send(f"💸 Need ${cost}, you have ${bal}")

        balances[user_id] = bal - cost

        if user_id not in portfolio:
            portfolio[user_id] = {}

        portfolio[user_id][name] = portfolio[user_id].get(name, 0) + amount

        embed = discord.Embed(
            title="📈 Investment Made",
            description=f"Bought {amount}x **{name}** for ${round(cost,2)}",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    # -----------------------
    # SELL STOCK
    # -----------------------
    @commands.command()
    async def sell(self, ctx, name: str, amount: int = 1):
        user_id = ctx.author.id

        if user_id not in portfolio or name not in portfolio[user_id]:
            return await ctx.send("❌ You don't own this stock.")

        owned = portfolio[user_id][name]

        if amount > owned:
            return await ctx.send("❌ You don't own that many shares.")

        sell_price = stocks[name]["price"] * amount
        balances[user_id] = balances.get(user_id, 0) + sell_price

        portfolio[user_id][name] -= amount

        if portfolio[user_id][name] <= 0:
            del portfolio[user_id][name]

        embed = discord.Embed(
            title="💸 Sold Stock",
            description=f"Sold {amount}x {name} for ${round(sell_price,2)}",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)

    # -----------------------
    # STOCK LIST
    # -----------------------
    @commands.command()
    async def stocks(self, ctx):
        embed = discord.Embed(
            title="📊 Market",
            color=discord.Color.blurple()
        )

        if not stocks:
            embed.description = "No stocks available."
            return await ctx.send(embed=embed)

        for name, data in stocks.items():
            embed.add_field(
                name=name,
                value=f"${data['price']}",
                inline=False
            )

        await ctx.send(embed=embed)

    # -----------------------
    # ADD STOCK (ADMIN)
    # -----------------------
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addstocks(self, ctx, name: str, price: float):

        stocks[name] = {
            "price": price,
            "owner": ctx.author.id
        }

        await ctx.send(f"📈 Created stock **{name}** at ${price}")


async def setup(bot):
    await bot.add_cog(Economy(bot))
