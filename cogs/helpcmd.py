import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from check import env
import traceback

class helpcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("help cargado correctamente")
        await self.bot.tree.sync()

    @app_commands.command(name="help", description="Te ayuda con el bot y sus comandos.")
    async def help(self, interaction: discord.Interaction):
        try:
            rolename = get(interaction.guild.roles, id=int(env('ROLE_ID')))
            help_embed = discord.Embed(title="CTM Commands", description="Comandos del bot.", color=discord.Color.red())
            help_embed.set_footer(text="Creado por Arceusgame (toagus)")
            help_embed.add_field(name="Comandos Generales", value=f"**/tag:** Sirve para poder colocarse el tag en discord y poder copiarlo para tu nombre. \n **Proximamente...**")
            if rolename in interaction.user.roles:
                help_embed.add_field(name="Comandos Staff", value=f"**/info:** Se obtienen los nombre y id de los usuarios. \n **/kickuser: <id del usuario> <razon del kickeo este parametro es opcional>** \n **/message: <id del usuario> <mensaje hacia el usuario>** \n **/select_kick:** Sirve para seleccionar al usuario en diferentes lista dependiendo de la cantidad de usuarios.")
            try:
                await interaction.user.send(embed=help_embed)
                await interaction.response.send_message("Revisa tu DM", ephemeral=True)
            except discord.Forbidden:
                # Si el bot no puede enviar un mensaje privado al usuario
                await interaction.response.send_message("No puedo enviarte un mensaje privado. ¿Tienes los DMs habilitados?", ephemeral=True)
        except Exception as e:
                traceback.print_exc()

async def setup(bot):
    await bot.add_cog(helpcmd(bot))