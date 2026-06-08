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

government = {
    "leader": None,
    "tax_rate": 5,
}

laws = {}

revolution_votes = set()

# =========================
# CONFIG
# =========================
WORK_COOLDOWN = 60


# =========================
# STOCK ENGINE (AUTO WORLD SIM)
# =========================
async def world_engine():
    while True:
        await asyncio.sleep(1)

        # 📈 stock movement
        for stock in stocks.values():
            stock["price"] = max(
                0.01,
                round(stock["price"] + random.uniform(-0.10, 0.32), 2)
            )

            # 💀 crash event
            if random.randint(1, 250) == 1:
                stock["price"] *= random.uniform(0.3, 0.7)

        # 🧠 insider/global events
        if random.randint(1, 300) == 1:
            mult = random.uniform(0.5, 1.8)

            for stock in stocks.values():
                stock["price"] = round(stock["price"] * mult, 2)

        # 🧾 AUTO TAX SYSTEM (government controlled)
        tax_rate = government["tax_rate"] / 100

        for uid in list(balances.keys()):
            tax = int(balances.get(uid, 0) * tax_rate)
            balances[uid] = max(0, balances.get(uid, 0) - tax)


# =========================
# ECONOMY COG
# =========================
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(world_engine())

    # =====================
    # WORK SYSTEM
    # =====================
    @commands.command()
    async def work(self, ctx):
        uid = ctx.author.id
        now = time.time()

        if uid in cooldowns and now - cooldowns[uid] < WORK_COOLDOWN:
            return await ctx.send("⏳ Cooldown active")

        cooldowns[uid] = now

        job = user_jobs.get(uid, "unemployed")
        if job == "unemployed":
            return await ctx.send("💀 You need a job")

        earnings = random.randint(25, 150)
        balances[uid] = balances.get(uid, 0) + earnings

        await ctx.send(f"💼 Worked as {job} and earned ${earnings}")

    # =====================
    # JOB SYSTEM
    # =====================
    @commands.command()
    async def job(self, ctx, name: str):
        user_jobs[ctx.author.id] = name
        await ctx.send(f"👷 Job set: {name}")

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
            return await ctx.send("❌ Not enough cash")

        balances[uid] -= amount
        bank[uid] = bank.get(uid, 0) + amount

        await ctx.send("🏦 Deposited")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        uid = ctx.author.id

        if bank.get(uid, 0) < amount:
            return await ctx.send("❌ Not enough bank")

        bank[uid] -= amount
        balances[uid] = balances.get(uid, 0) + amount

        await ctx.send("💸 Withdrawn")

    # =====================
    # STOCK SYSTEM
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
    async def invest(self, ctx, name: str, amount: int = 1):
        uid = ctx.author.id

        if name not in stocks:
            return await ctx.send("❌ Stock not found")

        cost = stocks[name]["price"] * amount

        if balances.get(uid, 0) < cost:
            return await ctx.send("❌ Not enough money")

        balances[uid] -= cost

        portfolio.setdefault(uid, {})
        portfolio[uid][name] = portfolio[uid].get(name, 0) + amount

        await ctx.send(f"📈 Invested ${cost}")

    @commands.command()
    async def sell(self, ctx, name: str, amount: int = 1):
        uid = ctx.author.id

        if uid not in portfolio or portfolio[uid].get(name, 0) < amount:
            return await ctx.send("❌ Not enough shares")

        earnings = stocks[name]["price"] * amount
        balances[uid] = balances.get(uid, 0) + earnings

        portfolio[uid][name] -= amount

        await ctx.send(f"💸 Sold for ${round(earnings,2)}")

    @commands.command()
    async def portfolio(self, ctx):
        data = portfolio.get(ctx.author.id, {})

        if not data:
            return await ctx.send("📊 Empty portfolio")

        msg = "📊 Portfolio:\n"

        for n, a in data.items():
            msg += f"{n}: {a} shares\n"

        await ctx.send(msg)

    # =====================
    # GOVERNMENT SYSTEM
    # =====================
    @commands.command()
    async def becomegov(self, ctx):
        if government["leader"] is None:
            government["leader"] = ctx.author.id
            await ctx.send("👑 You are now government")
        else:
            await ctx.send("❌ Already exists")

    @commands.command()
    async def settax(self, ctx, rate: int):
        if ctx.author.id != government["leader"]:
            return await ctx.send("❌ Not government")

        government["tax_rate"] = rate
        await ctx.send(f"🧾 Tax set to {rate}%")

    # =====================
    # LAWS SYSTEM (AUTO RULES)
    # =====================
    @commands.command()
    async def addlaw(self, ctx, *, law: str):
        if ctx.author.id != government["leader"]:
            return await ctx.send("❌ Not government")

        law_id = len(laws) + 1
        laws[law_id] = law

        await ctx.send(f"⚖️ Law added: {law}")

    @commands.command()
    async def laws(self, ctx):
        if not laws:
            return await ctx.send("📜 No laws")

        msg = "📜 Laws:\n"
        for i, l in laws.items():
            msg += f"{i}. {l}\n"

        await ctx.send(msg)

    # =====================
    # REVOLUTION SYSTEM
    # =====================
    @commands.command()
    async def revolt(self, ctx):
        revolution_votes.add(ctx.author.id)

        if len(revolution_votes) > 3:  # simple threshold
            government["leader"] = None
            revolution_votes.clear()
            await ctx.send("🔥 REVOLUTION SUCCESSFUL")
        else:
            await ctx.send("🪧 Vote added")


async def setup(bot):
    await bot.add_cog(Economy(bot))
