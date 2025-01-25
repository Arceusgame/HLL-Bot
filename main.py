import discord
from discord.ext import commands
from discord import app_commands
import requests
import os
import cogs
import asyncio
import sqlite3
import json
from check import auth
from check import env
from embedlist import PlayerListPaginator

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

database = sqlite3.connect('database.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS whitelist(steam_user STRING, discord_user STRING, steamid STRING)")


datos = {'username': f'{env('user')}', 'password': f'{env('psw')}'}
requests.post(f"http://{env('IP_VPS')}/api/login", data=json.dumps(datos), headers=auth)



@bot.command()
async def arceus(ctx):
    await ctx.send("EASTER EGG")


     

extensions = []

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

##if __name__ == '__main__':
   ##app.run(debug=True)

@bot.event
async def on_ready():
    

    print(f"{bot.user} ha iniciado sesión.")
    try:
        # Sincroniza comandos slash
        count = await bot.tree.sync()
        print(f"{len(count)} Comandos slash sincronizados.")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

async def main():
    async with bot:
        await load()
        await bot.start(env("TOKEN"))

asyncio.run(main())