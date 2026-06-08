import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, module: str = None):

        # =========================
        # MAIN HELP MENU
        # =========================
        if module is None:
            embed = discord.Embed(
                title="📚 Economy Bot Help Menu",
                description="Use `!help <module>` to view commands",
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="💰 Economy",
                value="work, balance, deposit, withdraw, bank",
                inline=False
            )

            embed.add_field(
                name="📈 Stocks",
                value="stocks, addstocks, invest, sell, portfolio",
                inline=False
            )

            embed.add_field(
                name="🏛️ Government",
                value="becomegov, settax, addlaw, laws",
                inline=False
            )

            embed.add_field(
                name="👷 Jobs",
                value="job",
                inline=False
            )

            embed.add_field(
                name="🧨 Chaos",
                value="revolt",
                inline=False
            )

            embed.set_footer(text="Use !help <module> for detailed usage")
            return await ctx.send(embed=embed)

        # =========================
        # ECONOMY MODULE
        # =========================
        if module.lower() == "economy":
            embed = discord.Embed(
                title="💰 Economy Commands",
                color=discord.Color.green()
            )

            embed.add_field(
                name="!work",
                value="Earn money from your job\nUsage: `!work`",
                inline=False
            )

            embed.add_field(
                name="!balance",
                value="Check your cash\nUsage: `!balance`",
                inline=False
            )

            embed.add_field(
                name="!deposit / !withdraw",
                value="Move money to/from bank\nUsage: `!deposit 100`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # STOCKS MODULE
        # =========================
        if module.lower() == "stocks":
            embed = discord.Embed(
                title="📈 Stock Market Commands",
                color=discord.Color.gold()
            )

            embed.add_field(
                name="!stocks",
                value="View all stock prices\nUsage: `!stocks`",
                inline=False
            )

            embed.add_field(
                name="!addstocks",
                value="Create a stock (admin)\nUsage: `!addstocks Tesla 100.5`",
                inline=False
            )

            embed.add_field(
                name="!invest",
                value="Buy stock shares\nUsage: `!invest Tesla 5`",
                inline=False
            )

            embed.add_field(
                name="!sell",
                value="Sell stock shares\nUsage: `!sell Tesla 2`",
                inline=False
            )

            embed.add_field(
                name="!portfolio",
                value="View your investments\nUsage: `!portfolio`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # GOVERNMENT MODULE
        # =========================
        if module.lower() == "government":
            embed = discord.Embed(
                title="🏛️ Government Commands",
                color=discord.Color.red()
            )

            embed.add_field(
                name="!becomegov",
                value="Become government leader\nUsage: `!becomegov`",
                inline=False
            )

            embed.add_field(
                name="!settax",
                value="Set global tax rate\nUsage: `!settax 10`",
                inline=False
            )

            embed.add_field(
                name="!addlaw",
                value="Create a law\nUsage: `!addlaw no gambling`",
                inline=False
            )

            embed.add_field(
                name="!laws",
                value="View all laws\nUsage: `!laws`",
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
                name="Available Jobs",
                value="miner, trader, developer, robber",
                inline=False
            )

            return await ctx.send(embed=embed)

        # =========================
        # CHAOS MODULE
        # =========================
        if module.lower() == "chaos":
            embed = discord.Embed(
                title="🧨 Chaos Commands",
                color=discord.Color.dark_purple()
            )

            embed.add_field(
                name="!revolt",
                value="Start a revolution against government\nUsage: `!revolt`",
                inline=False
            )

            return await ctx.send(embed=embed)

        # fallback
        await ctx.send("❌ Module not found. Try: economy, stocks, government, jobs, chaos")


async def setup(bot):
    await bot.add_cog(Help(bot))
