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
                title="📚 Economy Bot Help",
                description="Use `!help <module>` for details",
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="💰 Economy",
                value="balance, work, deposit, withdraw, bank",
                inline=False
            )

            embed.add_field(
                name="📈 Stocks",
                value="stocks, addstocks, invest (stock) (shares), sell (stock) (shares), portfolio",
                inline=False
            )

            embed.add_field(
                name="🏛️ Government",
                value="becomegov, settax (rate), addlaw (text), laws",
                inline=False
            )

            embed.add_field(
                name="👷 Jobs",
                value="job (name)",
                inline=False
            )

            embed.add_field(
                name="🧨 Chaos",
                value="revolt",
                inline=False
            )

            embed.add_field(
                name="📊 Info",
                value="economy",
                inline=False
            )

            embed.set_footer(text="Example: !invest Tesla 5")
            return await ctx.send(embed=embed)

        # =========================
        # ECONOMY
        # =========================
        if module.lower() == "economy":
            embed = discord.Embed(
                title="💰 Economy Commands",
                color=discord.Color.green()
            )

            embed.add_field(
                name="!balance",
                value="Check your money\nUsage: `!balance`",
                inline=False
            )

            embed.add_field(
                name="!work",
                value="Earn money from job\nUsage: `!work`",
                inline=False
            )

            embed.add_field(
                name="!deposit",
                value="Put money in bank\nUsage: `!deposit 100`",
                inline=False
            )

            embed.add_field(
                name="!withdraw",
                value="Take money from bank\nUsage: `!withdraw 100`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # STOCKS
        # =========================
        if module.lower() == "stocks":
            embed = discord.Embed(
                title="📈 Stock Market",
                color=discord.Color.gold()
            )

            embed.add_field(
                name="!stocks",
                value="View market prices\nUsage: `!stocks`",
                inline=False
            )

            embed.add_field(
                name="!addstocks",
                value="Create stock (admin)\nUsage: `!addstocks Tesla 100`",
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
                value="Your holdings\nUsage: `!portfolio`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # GOVERNMENT
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
        # JOBS
        # =========================
        if module.lower() == "jobs":
            embed = discord.Embed(
                title="👷 Jobs System",
                color=discord.Color.teal()
            )

            embed.add_field(
                name="!job",
                value="Choose job\nUsage: `!job miner`",
                inline=False
            )

            embed.add_field(
                name="Jobs List",
                value="miner, trader, developer, robber",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # CHAOS
        # =========================
        if module.lower() == "chaos":
            embed = discord.Embed(
                title="🧨 Chaos System",
                color=discord.Color.dark_purple()
            )

            embed.add_field(
                name="!revolt",
                value="Start revolution\nUsage: `!revolt`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # INFO
        # =========================
        if module.lower() == "info":
            embed = discord.Embed(
                title="📊 Info Commands",
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="!economy",
                value="View economy index\nUsage: `!economy`",
                inline=False
            )

            return await ctx.send(embed=embed)

        await ctx.send("❌ Module not found. Try: economy, stocks, government, jobs, chaos, info")


async def setup(bot):
    await bot.add_cog(Help(bot))
