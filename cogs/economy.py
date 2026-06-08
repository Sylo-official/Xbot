import discord
from discord.ext import commands
import random
import asyncio

# =========================
# GLOBAL STATE
# =========================

balances = {}
bank = {}
stocks = {}
portfolio = {}
user_jobs = {}
loans = {}
laws = {}

government = {"leader": None, "tax_rate": 5}

economy_index = 100.0


# =========================
# WORLD ENGINE
# =========================

async def world_loop():
    global economy_index

    while True:
        await asyncio.sleep(1)

        for stock in stocks.values():
            stock["price"] = max(0.01, stock["price"] + random.uniform(-0.10, 0.32))

            if random.randint(1, 350) == 1:
                stock["price"] *= random.uniform(0.3, 0.8)

        economy_index += random.uniform(-1.2, 1.8)

        tax = government["tax_rate"] / 100

        for uid in list(balances.keys()):
            balances[uid] = max(0, int(balances.get(uid, 0) * (1 - tax)))


# =========================
# LOANS
# =========================

async def loan_loop():
    while True:
        await asyncio.sleep(300)

        for uid in loans:
            loans[uid] = int(loans.get(uid, 0) * 1.05)


# =========================
# COG
# =========================

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(world_loop())
        bot.loop.create_task(loan_loop())

    # =====================
    # BALANCE
    # =====================
    @commands.command()
    async def balance(self, ctx):
        embed = discord.Embed(
            title="💰 Balance",
            description=f"${balances.get(ctx.author.id, 0)}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    # =====================
    # BANK
    # =====================
    @commands.command()
    async def bank(self, ctx):
        embed = discord.Embed(
            title="🏦 Bank",
            description=f"${bank.get(ctx.author.id, 0)}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def deposit(self, ctx, amount: int):
        uid = ctx.author.id

        if balances.get(uid, 0) < amount:
            return await ctx.send("❌ Not enough cash")

        balances[uid] -= amount
        bank[uid] = bank.get(uid, 0) + amount

        await ctx.send(embed=discord.Embed(
            title="🏦 Deposited",
            description=f"+${amount}",
            color=discord.Color.blue()
        ))

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        uid = ctx.author.id

        if bank.get(uid, 0) < amount:
            return await ctx.send("❌ Not enough bank")

        bank[uid] -= amount
        balances[uid] = balances.get(uid, 0) + amount

        await ctx.send(embed=discord.Embed(
            title="💸 Withdrawn",
            description=f"+${amount}",
            color=discord.Color.green()
        ))

    # =====================
    # JOBS
    # =====================
    jobs = {
        "miner": (25, 100),
        "trader": (50, 200),
        "dev": (100, 300),
        "robber": (0, 400)
    }

    @commands.command()
    async def job(self, ctx, name: str):
        name = name.lower()

        if name not in self.jobs:
            return await ctx.send("❌ miner / trader / dev / robber")

        user_jobs[ctx.author.id] = name

        await ctx.send(embed=discord.Embed(
            title="👷 Job Set",
            description=f"You are now a **{name}**",
            color=discord.Color.orange()
        ))

    @commands.command()
    async def work(self, ctx):
        uid = ctx.author.id

        if uid not in user_jobs:
            return await ctx.send("💀 No job")

        job = user_jobs[uid]
        low, high = self.jobs[job]

        earn = random.randint(low, high)
        balances[uid] = balances.get(uid, 0) + earn

        await ctx.send(embed=discord.Embed(
            title="💼 Work Done",
            description=f"+${earn} as {job}",
            color=discord.Color.teal()
        ))

    # =====================
    # CASINO
    # =====================
    @commands.command()
    async def spin(self, ctx, amount: int):
        uid = ctx.author.id

        if balances.get(uid, 0) < amount:
            return await ctx.send("❌ No money")

        balances[uid] -= amount

        roll = random.randint(1, 100)

        if roll == 100:
            win = amount * 10
            result = "JACKPOT 🎉"
        elif roll > 85:
            win = int(amount * 2.5)
            result = "BIG WIN 🔥"
        elif roll > 55:
            win = int(amount * 1.3)
            result = "WIN 👍"
        else:
            win = 0
            result = "LOSS 💀"

        balances[uid] += win

        await ctx.send(embed=discord.Embed(
            title="🎰 Spin Result",
            description=result,
            color=discord.Color.gold()
        ).add_field(name="Won", value=f"${win}", inline=True)
         .add_field(name="Bet", value=f"${amount}", inline=True))

    # =====================
    # STOCKS
    # =====================
    @commands.command()
    async def addstocks(self, ctx, name: str, price: float):
        stocks[name] = {"price": price}

        await ctx.send(embed=discord.Embed(
            title="📈 Stock Added",
            description=f"{name} @ ${price}",
            color=discord.Color.green()
        ))

    @commands.command()
    async def stocks(self, ctx):
        embed = discord.Embed(title="📈 Market", color=discord.Color.gold())

        if not stocks:
            embed.description = "No stocks yet"
            return await ctx.send(embed=embed)

        for n, d in stocks.items():
            embed.add_field(name=n, value=f"${round(d['price'],2)}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def invest(self, ctx, name: str, shares: int):
        uid = ctx.author.id

        if name not in stocks:
            return await ctx.send("❌ No stock")

        cost = stocks[name]["price"] * shares

        if balances.get(uid, 0) < cost:
            return await ctx.send("❌ No money")

        balances[uid] -= cost
        portfolio.setdefault(uid, {})
        portfolio[uid][name] = portfolio[uid].get(name, 0) + shares

        await ctx.send(embed=discord.Embed(
            title="📈 Invested",
            description=f"{shares} shares of {name}",
            color=discord.Color.green()
        ))

    @commands.command()
    async def sell(self, ctx, name: str, shares: int):
        uid = ctx.author.id

        if portfolio.get(uid, {}).get(name, 0) < shares:
            return await ctx.send("❌ Not enough shares")

        gain = stocks[name]["price"] * shares
        balances[uid] += gain

        portfolio[uid][name] -= shares

        await ctx.send(embed=discord.Embed(
            title="💸 Sold",
            description=f"+${round(gain,2)}",
            color=discord.Color.blue()
        ))

    # =====================
    # ECONOMY INFO
    # =====================
    @commands.command()
    async def economy(self, ctx):
        await ctx.send(embed=discord.Embed(
            title="📊 Economy Index",
            description=f"{round(economy_index,2)}",
            color=discord.Color.blurple()
        ))


async def setup(bot):
    await bot.add_cog(Economy(bot))
