import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import requests
import traceback
from check import check_steamid


database = sqlite3.connect('database.db')
cursor = database.cursor()


class tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @commands.Cog.listener()
    async def on_ready(self):
        print("whitelist cargado correctamente")
        await self.bot.tree.sync()


    @app_commands.command(name="add_whitelist", description="Agrega a un usuario a la whitelist para cuando el server este lleno.")
    async def whitelist(self, interaction: discord.Interaction, user: str, member: discord.Member, id: str ):
        file = discord.File("./res/logo.png", filename="logo.png")
        try:
            if await check_steamid(id):
                query = "INSERT INTO whitelist VALUES (?, ?, ?)"
                cursor.execute(query, (user, str(member), id))
                database.commit()

                whitelist_embed = discord.Embed(title=f"{member}'s fue agregado a la whitelist", color=discord.Color.random(), description=f"Ahora {member} puede utilizar el comando para poder entrar mas rapido.")
                whitelist_embed.set_thumbnail(url="attachment://logo.png")
                whitelist_embed.set_footer(text=(f"Fue agregado por {interaction.user}'s"))

                await interaction.response.send_message(file=file, embed=whitelist_embed)
            else:
                errorsteamid_embed =  discord.Embed(title="Steamid incorrecto.", color=discord.Color.red())
                errorsteamid_embed.set_thumbnail(url="attachment://logo.png")
                await interaction.response.send_message(file=file, embed=errorsteamid_embed)
        except Exception as e:
            traceback.print_exc()

    #cursor.execute(query, (steam_user,))
    #str(member)

    #query = "DELETE FROM whitelist WHERE steam_user = ? OR member = ?"
        #cursor.execute(query, (steam_user, str(member)))


    @app_commands.command(name="delete_whitelist", description="Eliminar a un usuario a la whitelist para cuando el server este lleno.")
    async def delwhitelist(self, interaction: discord.Interaction, user: str = None, member: discord.Member = None, id: str = None):
        file = discord.File("./res/logo.png", filename="logo.png")
        if user or member or id != None:
           memberid = str(member)
           query = "DELETE FROM whitelist WHERE steam_user = ? OR discord_user = ? OR steamid = ?;"
           cursor.execute(query, (user, memberid, id))
           database.commit()

           if cursor.rowcount > 0:
               whitelist_embed = discord.Embed(title=f"{member}'s fue eliminado a la whitelist", color=discord.Color.random(), description=f"Ahora  ya no se encuentra en la lista para usar el comando.")
               whitelist_embed.set_thumbnail(url="attachment://logo.png")
               whitelist_embed.set_footer(text=(f"Fue eliminado por {interaction.user}'s"))
               await interaction.response.send_message(file=file, embed=whitelist_embed)
           else:
               errordontfound_embed =  discord.Embed(title="No se encontro en la base de datos.", color=discord.Color.red())
               errordontfound_embed.set_thumbnail(url="attachment://logo.png")
               await interaction.response.send_message(file=file, embed=errordontfound_embed)
        else:
            error_embed = discord.Embed(title="Se necesita por lo menos un dato.", color=discord.Color.red())
            error_embed.set_thumbnail(url="attachment://logo.png")
            await interaction.response.send_message(file=file, embed=error_embed)
        




async def setup(bot):
    await bot.add_cog(tests(bot))