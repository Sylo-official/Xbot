import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, module: str = None):

        # =========================
        # MAIN MENU
        # =========================
        if module is None:
            embed = discord.Embed(
                title="📚 Economy World Help",
                description="Use `!help <module>`",
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="💰 Economy",
                value="balance, bank, deposit (amount), withdraw (amount), economy",
                inline=False
            )

            embed.add_field(
                name="👷 Jobs",
                value="job (name), work",
                inline=False
            )

            embed.add_field(
                name="📈 Stocks",
                value="stocks, addstocks (name price), invest (stock shares), sell (stock shares), portfolio",
                inline=False
            )

            embed.add_field(
                name="🎰 Casino",
                value="spin (amount)",
                inline=False
            )

            embed.add_field(
                name="🏛️ Government",
                value="becomegov, settax (rate), addlaw (text), laws",
                inline=False
            )

            embed.add_field(
                name="🧨 Chaos",
                value="revolt",
                inline=False
            )

            embed.set_footer(text="Example: !invest Tesla 5")
            return await ctx.send(embed=embed)

        # =========================
        # ECONOMY MODULE
        # =========================
        if module.lower() == "economy":
            embed = discord.Embed(
                title="💰 Economy System",
                color=discord.Color.green()
            )

            embed.add_field(
                name="!balance",
                value="Check money\nUsage: `!balance`",
                inline=False
            )

            embed.add_field(
                name="!bank",
                value="Check bank balance\nUsage: `!bank`",
                inline=False
            )

            embed.add_field(
                name="!deposit",
                value="Deposit cash\nUsage: `!deposit 100`",
                inline=False
            )

            embed.add_field(
                name="!withdraw",
                value="Withdraw cash\nUsage: `!withdraw 100`",
                inline=False
            )

            embed.add_field(
                name="!economy",
                value="View world economy index\nUsage: `!economy`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # JOBS MODULE
        # =========================
        if module.lower() == "jobs":
            embed = discord.Embed(
                title="👷 Job System",
                color=discord.Color.teal()
            )

            embed.add_field(
                name="!job",
                value="Choose a job\nUsage: `!job miner`",
                inline=False
            )

            embed.add_field(
                name="!work",
                value="Work your job for money\nUsage: `!work`",
                inline=False
            )

            embed.add_field(
                name="Available Jobs",
                value="miner, trader, developer, robber",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # STOCKS MODULE
        # =========================
        if module.lower() == "stocks":
            embed = discord.Embed(
                title="📈 Stock Market",
                color=discord.Color.gold()
            )

            embed.add_field(
                name="!stocks",
                value="View market\nUsage: `!stocks`",
                inline=False
            )

            embed.add_field(
                name="!addstocks",
                value="Create stock\nUsage: `!addstocks Tesla 100`",
                inline=False
            )

            embed.add_field(
                name="!invest",
                value="Buy shares\nUsage: `!invest Tesla 5`",
                inline=False
            )

            embed.add_field(
                name="!sell",
                value="Sell shares\nUsage: `!sell Tesla 2`",
                inline=False
            )

            embed.add_field(
                name="!portfolio",
                value="Your investments\nUsage: `!portfolio`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # CASINO MODULE
        # =========================
        if module.lower() == "casino":
            embed = discord.Embed(
                title="🎰 Casino System",
                color=discord.Color.dark_gold()
            )

            embed.add_field(
                name="!spin",
                value="Gamble money\nUsage: `!spin 100`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # GOVERNMENT MODULE
        # =========================
        if module.lower() == "government":
            embed = discord.Embed(
                title="🏛️ Government System",
                color=discord.Color.red()
            )

            embed.add_field(
                name="!becomegov",
                value="Become leader\nUsage: `!becomegov`",
                inline=False
            )

            embed.add_field(
                name="!settax",
                value="Set tax rate\nUsage: `!settax 10`",
                inline=False
            )

            embed.add_field(
                name="!addlaw",
                value="Create law\nUsage: `!addlaw no gambling`",
                inline=False
            )

            embed.add_field(
                name="!laws",
                value="View laws\nUsage: `!laws`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # CHAOS MODULE
        # =========================
        if module.lower() == "chaos":
            embed = discord.Embed(
                title="🧨 Chaos System",
                color=discord.Color.purple()
            )

            embed.add_field(
                name="!revolt",
                value="Start revolution vote\nUsage: `!revolt`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # INVALID MODULE
        # =========================
        await ctx.send("❌ Module not found. Try: economy, jobs, stocks, casino, government, chaos")


async def setup(bot):
    await bot.add_cog(Help(bot))
