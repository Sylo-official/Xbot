import discord
from discord.ext import commands


class HelpMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Economy", emoji="💰"),
            discord.SelectOption(label="Jobs", emoji="👷"),
            discord.SelectOption(label="Stocks", emoji="📈"),
            discord.SelectOption(label="Casino", emoji="🎰"),
        ]

        super().__init__(placeholder="Choose module...", options=options)

    async def callback(self, interaction):
        e = self.values[0]

        embeds = {
            "Economy": discord.Embed(
                title="💰 Economy",
                description="balance, bank, deposit, withdraw, economy",
                color=discord.Color.green()
            ),
            "Jobs": discord.Embed(
                title="👷 Jobs",
                description="job (name), work",
                color=discord.Color.orange()
            ),
            "Stocks": discord.Embed(
                title="📈 Stocks",
                description="stocks, addstocks, invest, sell",
                color=discord.Color.gold()
            ),
            "Casino": discord.Embed(
                title="🎰 Casino",
                description="spin (amount)",
                color=discord.Color.dark_gold()
            )
        }

        await interaction.response.edit_message(embed=embeds[e], view=self.view)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpMenu())


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="📚 Economy Bot Help",
            description="Pick a module",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=HelpView())


async def setup(bot):
    await bot.add_cog(Help(bot))
