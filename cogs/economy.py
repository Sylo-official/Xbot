import discord
from discord.ext import commands
import random
import asyncio
import time

# =========================
# GLOBAL STATE (WORLD SAVE)
# =========================

balances = {}
bank = {}

stocks = {}
portfolio = {}

user_jobs = {}
cooldowns = {}

loans = {}
property_owned = {}

inventory = {}

laws = {}
revolution_votes = set()

government = {
    "leader": None,
    "tax_rate": 5
}

economy_index = 100.0
inflation = 1.0

# =========================
# CONFIG
# =========================

WORK_COOLDOWN = 60


# =========================
# WORLD ENGINE (AUTO SIMULATION)
# =========================

async def world_loop():
    global economy_index, inflation

    while True:
        await asyncio.sleep(1)

        # 📈 STOCK MARKET SIM
        for stock in stocks.values():
            stock["price"] = max(
                0.01,
                stock["price"] + random.uniform(-0.10, 0.32)
            )

            # 💀 crash
            if random.randint(1, 400) == 1:
                stock["price"] *= random.uniform(0.3, 0.7)

        # 📊 ECONOMY INDEX
        economy_index += random.uniform(-1.5, 2.0)

        # 📉 INFLATION SYSTEM
        inflation *= random.uniform(0.999, 1.002)

        # 🧾 TAX SYSTEM (AUTO GOV)
        tax = government["tax_rate"] / 100

        for uid in list(balances.keys()):
            balances[uid] = max(
                0,
                int(balances.get(uid, 0) - balances.get(uid, 0) * tax)
            )

        # 🧠 INSIDER EVENT
        if random.randint(1, 800) == 1:
            mult = random.uniform(0.5, 1.8)
            for s in stocks:
                stocks[s]["price"] *= mult


# =========================
# LOAN SYSTEM
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
    # BALANCE / BANK
    # =====================

    @commands.command()
    async def balance(self, ctx):
        await ctx.send(f"💰 ${balances.get(ctx.author.id, 0)}")

    @commands.command()
    async def bank(self, ctx):
        await ctx.send(f"🏦 ${bank.get(ctx.author.id, 0)}")

    @commands.command()
    async def deposit(self, ctx, amount: int):
        uid = ctx.author.id

        if balances.get(uid, 0) < amount:
            return await ctx.send("❌ not enough cash")

        balances[uid] -= amount
        bank[uid] = bank.get(uid, 0) + amount

        await ctx.send("🏦 deposited")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        uid = ctx.author.id

        if bank.get(uid, 0) < amount:
            return await ctx.send("❌ not enough bank")

        bank[uid] -= amount
        balances[uid] = balances.get(uid, 0) + amount

        await ctx.send("💸 withdrawn")

    # =====================
    # JOB SYSTEM
    # =====================

    jobs = {
        "miner": (25, 100),
        "trader": (50, 200),
        "developer": (100, 300),
        "robber": (0, 400)
    }

    @commands.command()
    async def job(self, ctx, name: str):
        name = name.lower()

        if name not in self.jobs:
            return await ctx.send("❌ miner, trader, developer, robber")

        user_jobs[ctx.author.id] = name
        await ctx.send(f"👷 Job set: {name}")

    @commands.command()
    async def work(self, ctx):
        uid = ctx.author.id

        if uid not in user_jobs:
            return await ctx.send("💀 no job")

        job = user_jobs[uid]
        low, high = self.jobs[job]

        earn = random.randint(low, high)
        balances[uid] = balances.get(uid, 0) + earn

        await ctx.send(f"💼 +${earn}")

    # =====================
    # CASINO (SPIN)
    # =====================

    @commands.command()
    async def spin(self, ctx, amount: int):
        uid = ctx.author.id

        if balances.get(uid, 0) < amount:
            return await ctx.send("❌ no money")

        balances[uid] -= amount
        roll = random.randint(1, 100)

        if roll == 100:
            win = amount * 10
        elif roll > 85:
            win = int(amount * 2.5)
        elif roll > 55:
            win = int(amount * 1.3)
        else:
            win = 0

        balances[uid] += win

        if win == 0:
            return await ctx.send(f"🎰 lost -${amount}")

        await ctx.send(f"🎰 won +${win}")

    # =====================
    # STOCK MARKET
    # =====================

    @commands.command()
    async def addstocks(self, ctx, name: str, price: float):
        stocks[name] = {"price": price}
        await ctx.send(f"📈 stock added {name}")

    @commands.command()
    async def stocks(self, ctx):
        msg = "📊 MARKET:\n"
        for n, d in stocks.items():
            msg += f"{n}: ${round(d['price'],2)}\n"
        await ctx.send(msg)

    @commands.command()
    async def invest(self, ctx, name: str, shares: int):
        uid = ctx.author.id

        if name not in stocks:
            return await ctx.send("❌ no stock")

        cost = stocks[name]["price"] * shares

        if balances.get(uid, 0) < cost:
            return await ctx.send("❌ no money")

        balances[uid] -= cost
        portfolio.setdefault(uid, {})
        portfolio[uid][name] = portfolio[uid].get(name, 0) + shares

        await ctx.send("📈 invested")

    @commands.command()
    async def sell(self, ctx, name: str, shares: int):
        uid = ctx.author.id

        if portfolio.get(uid, {}).get(name, 0) < shares:
            return await ctx.send("❌ not enough")

        gain = stocks[name]["price"] * shares

        balances[uid] += gain
        portfolio[uid][name] -= shares

        await ctx.send(f"💸 sold +${round(gain,2)}")

    @commands.command()
    async def portfolio(self, ctx):
        data = portfolio.get(ctx.author.id, {})
        if not data:
            return await ctx.send("empty")

        msg = "📊 portfolio:\n"
        for n, s in data.items():
            msg += f"{n}: {s}\n"

        await ctx.send(msg)

    # =====================
    # GOVERNMENT
    # =====================

    @commands.command()
    async def becomegov(self, ctx):
        if government["leader"]:
            return await ctx.send("❌ exists")

        government["leader"] = ctx.author.id
        await ctx.send("👑 gov set")

    @commands.command()
    async def settax(self, ctx, rate: int):
        if ctx.author.id != government["leader"]:
            return await ctx.send("❌ not gov")

        government["tax_rate"] = rate
        await ctx.send("🧾 tax updated")

    @commands.command()
    async def addlaw(self, ctx, *, law: str):
        if ctx.author.id != government["leader"]:
            return await ctx.send("❌ not gov")

        laws[len(laws)+1] = law
        await ctx.send("⚖️ law added")

    @commands.command()
    async def laws(self, ctx):
        if not laws:
            return await ctx.send("none")

        msg = "\n".join([f"{i}. {l}" for i, l in laws.items()])
        await ctx.send(msg)

    # =====================
    # REVOLUTION
    # =====================

    @commands.command()
    async def revolt(self, ctx):
        revolution_votes.add(ctx.author.id)

        if len(revolution_votes) >= 3:
            government["leader"] = None
            revolution_votes.clear()
            await ctx.send("🔥 GOV OVERTHROWN")
        else:
            await ctx.send("🪧 vote added")

    # =====================
    # ECONOMY INFO
    # =====================

    @commands.command()
    async def economy(self, ctx):
        await ctx.send(
            f"📊 index: {round(economy_index,2)} | inflation: {round(inflation,3)}"
        )


async def setup(bot):
    await bot.add_cog(Economy(bot))
