import discord
from discord.ext import commands
from discord import app_commands
import traceback


class usercmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("usercmd cargado correctamente")
        await self.bot.tree.sync()

    @app_commands.command(name="tag", description="Sirve para colocarte en el nombre el tag y poder copiar el tag.")
    async def tag(self, interaction: discord.Interaction):
        try:
            prefix = "[•CTM•]"
            member = interaction.user
            embed = discord.Embed(title="Copia el tag", description=f"Steam: \n ```[•CTM•]``` \n Epic: \n ```Proximamente```", color=discord.Color.red())
            new_nickname = f"{prefix} {member.display_name}"
            await member.edit(nick=new_nickname)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
                traceback.print_exc()

async def setup(bot):
    await bot.add_cog(usercmd(bot))