import discord
from discord.ext import commands
import random
import asyncio
import time

# =========================
# CORE DATA
# =========================
balances = {}
bank = {}

stocks = {}
portfolio = {}

user_jobs = {}
cooldowns = {}

loans = {}

property_owned = {}

laws = {}
revolution_votes = set()

government = {
    "leader": None,
    "tax_rate": 5,
}

economy_index = 100.0

central_bank = {
    "reserve": 100000
}

# =========================
# CONFIG
# =========================
WORK_COOLDOWN = 60


# =========================
# WORLD SIM ENGINE
# =========================
async def world_sim():
    global economy_index

    while True:
        await asyncio.sleep(1)

        # 📈 STOCK MOVEMENT
        for stock in stocks.values():
            stock["price"] = max(
                0.01,
                round(stock["price"] + random.uniform(-0.10, 0.32), 2)
            )

            # 💀 crash
            if random.randint(1, 250) == 1:
                stock["price"] *= random.uniform(0.3, 0.7)

        # 🧠 global shock
        if random.randint(1, 300) == 1:
            mult = random.uniform(0.5, 1.8)
            for stock in stocks.values():
                stock["price"] = round(stock["price"] * mult, 2)

        # 📊 economy index drift
        economy_index = max(10, economy_index + random.uniform(-1.5, 2.0))

        # 🧾 TAX SYSTEM
        tax = government["tax_rate"] / 100

        for uid in list(balances.keys()):
            balances[uid] = max(
                0,
                balances.get(uid, 0) - int(balances.get(uid, 0) * tax)
            )


# =========================
# LOAN INTEREST SYSTEM
# =========================
async def loan_system():
    while True:
        await asyncio.sleep(300)

        for uid in loans:
            loans[uid] = int(loans.get(uid, 0) * 1.05)


# =========================
# ECONOMY COG
# =========================
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        bot.loop.create_task(world_sim())
        bot.loop.create_task(loan_system())

    # =====================
    # BALANCE
    # =====================
    @commands.command()
    async def balance(self, ctx):
        await ctx.send(f"💰 ${balances.get(ctx.author.id, 0)}")

    # =====================
    # WORK
    # =====================
    @commands.command()
    async def work(self, ctx):
        uid = ctx.author.id
        now = time.time()

        if uid in cooldowns and now - cooldowns[uid] < WORK_COOLDOWN:
            return await ctx.send("⏳ Cooldown")

        cooldowns[uid] = now

        job = user_jobs.get(uid, "unemployed")
        if job == "unemployed":
            return await ctx.send("💀 Get a job first")

        earn = random.randint(25, 150)
        balances[uid] = balances.get(uid, 0) + earn

        await ctx.send(f"💼 +${earn}")

    # =====================
    # JOBS
    # =====================
    @commands.command()
    async def job(self, ctx, name: str):
        user_jobs[ctx.author.id] = name
        await ctx.send(f"👷 Job: {name}")

    # =====================
    # BANK
    # =====================
    @commands.command()
    async def deposit(self, ctx, amount: int):
        uid = ctx.author.id

        if balances.get(uid, 0) < amount:
            return await ctx.send("❌ No cash")

        balances[uid] -= amount
        bank[uid] = bank.get(uid, 0) + amount

        await ctx.send("🏦 Deposited")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        uid = ctx.author.id

        if bank.get(uid, 0) < amount:
            return await ctx.send("❌ No bank")

        bank[uid] -= amount
        balances[uid] = balances.get(uid, 0) + amount

        await ctx.send("💸 Withdrawn")

    # =====================
    # STOCKS
    # =====================
    @commands.command()
    async def addstocks(self, ctx, name: str, price: float):
        stocks[name] = {"price": price}
        await ctx.send(f"📈 Stock added: {name}")

    @commands.command()
    async def stocks(self, ctx):
        msg = "📊 Market:\n"

        for n, d in stocks.items():
            msg += f"{n}: ${round(d['price'],2)}\n"

        await ctx.send(msg)

    # =====================
    # INVEST / SELL
    # =====================
    @commands.command()
    async def invest(self, ctx, name: str, shares: int):
        uid = ctx.author.id

        if name not in stocks:
            return await ctx.send("❌ Not found")

        cost = stocks[name]["price"] * shares

        if balances.get(uid, 0) < cost:
            return await ctx.send("❌ No money")

        balances[uid] -= cost

        portfolio.setdefault(uid, {})
        portfolio[uid][name] = portfolio[uid].get(name, 0) + shares

        await ctx.send(f"📈 Bought {shares} shares")

    @commands.command()
    async def sell(self, ctx, name: str, shares: int):
        uid = ctx.author.id

        if uid not in portfolio or portfolio[uid].get(name, 0) < shares:
            return await ctx.send("❌ Not enough shares")

        earnings = stocks[name]["price"] * shares
        balances[uid] = balances.get(uid, 0) + earnings

        portfolio[uid][name] -= shares

        await ctx.send(f"💸 Sold for ${round(earnings,2)}")

    @commands.command()
    async def portfolio(self, ctx):
        data = portfolio.get(ctx.author.id, {})

        if not data:
            return await ctx.send("📊 Empty")

        msg = "📊 Portfolio:\n"
        for n, s in data.items():
            msg += f"{n}: {s} shares\n"

        await ctx.send(msg)

    # =====================
    # GOVERNMENT
    # =====================
    @commands.command()
    async def becomegov(self, ctx):
        if government["leader"] is None:
            government["leader"] = ctx.author.id
            await ctx.send("👑 Gov set")
        else:
            await ctx.send("❌ Exists")

    @commands.command()
    async def settax(self, ctx, rate: int):
        if ctx.author.id != government["leader"]:
            return await ctx.send("❌ Not gov")

        government["tax_rate"] = rate
        await ctx.send(f"🧾 Tax {rate}%")

    # =====================
    # LAWS
    # =====================
    @commands.command()
    async def addlaw(self, ctx, *, law: str):
        if ctx.author.id != government["leader"]:
            return await ctx.send("❌ Not gov")

        laws[len(laws)+1] = law
        await ctx.send(f"⚖️ Law added")

    @commands.command()
    async def laws(self, ctx):
        if not laws:
            return await ctx.send("📜 None")

        msg = "📜 Laws:\n"
        for i, l in laws.items():
            msg += f"{i}. {l}\n"

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
            await ctx.send("🪧 Vote added")

    # =====================
    # ECONOMY INDEX
    # =====================
    @commands.command()
    async def economy(self, ctx):
        await ctx.send(f"📊 Economy Index: {round(economy_index,2)}")


async def setup(bot):
    await bot.add_cog(Economy(bot))
