import discord
from discord.ext import commands
from discord import app_commands
import requests
import traceback
import json
from check import request_steamid, check_game, check_steamid, check_epicid, env, auth
from select_config import MyView
import aiohttp
import asyncio
from embedlist import PlayerListPaginator
from discord.utils import get

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_live_game_stats(self, paginator, server: str):
        """Función para actualizar dinámicamente los datos del paginador."""
        url = f"http://rconctm.xyz:{server}/api/get_detailed_players"
        print(url)

        while True:
            try:
                response = requests.get(url, headers=auth)
                data = response.json()
                data = data.get('result', {}).get('players', {})
                player_list = [
                    {
                        'player_id': player_id,
                        'player': player_data.get("name")
                    }
                    for player_id, player_data in data.items()
                ]
                paginator.update_data(player_list)  # Actualizamos los datos en el paginador
                await asyncio.sleep(20)  # Esperamos 15 segundos antes de la próxima actualización
            except Exception as e:
                traceback.print_exc()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("utils cargado correctamente")
        await self.bot.tree.sync()

    @app_commands.command(name="kickuser", description="Sirve para kickiar a un usuario.")
    async def kick(self, interaction: discord.Interaction, id: str, reason: str = None, server: int = None):
        serveri = ""
        if server == None or server == 1:
            serveri = "8012"
        if server == 2:
            serveri = "8011"
        if server == 3:
            serveri = "8010"
        await interaction.response.defer()
        file = discord.File("./res/logo.png", filename="logo.png")
        rolename = get(interaction.guild.roles, id=int(env('ROLE_ID')))
        name = None
        try:
            if rolename in interaction.user.roles:
                if await check_steamid(id):
                    name = await request_steamid(id)
                elif await check_epicid(id):
                    name = await check_epicid(id)
                if await check_epicid(id) != None or await check_steamid(id):
                    if await check_game(id):
                        datos = {'player_name': name, 'reason': reason, 'by': 'admin', 'player_id': id}
                        requests.post(f"http://{env('IP_VPS')}:{serveri}/api/kick", data=json.dumps(datos), headers=auth)
                        kick_embed =  discord.Embed(title=f"{name}'s fue kickiado", description=f"{name}'s fue kickeado correctamente por {interaction.user}'s", color=discord.Color.red())
                        kick_embed.set_thumbnail(url="attachment://logo.png")
                        await interaction.followup.send(file=file, embed=kick_embed)
                    else:
                        errorsteamid_embed =  discord.Embed(title="No esta dentro del juego.", color=discord.Color.red())
                        errorsteamid_embed.set_thumbnail(url="attachment://logo.png")
                        await interaction.followup.send(file=file, embed=errorsteamid_embed)
                else:
                    errorgame_embed =  discord.Embed(title="Id inconrrecto debe ser de epic o de steam.", color=discord.Color.red())
                    errorgame_embed.set_thumbnail(url="attachment://logo.png")
                    await interaction.followup.send(file=file, embed=errorgame_embed)
            else:
                role_embed =  discord.Embed(title=f"Necesitas tener el rol de {rolename}", color=discord.Color.red())
                role_embed.set_thumbnail(url="attachment://logo.png")
                await interaction.followup.send(file=file, embed=role_embed)
        except Exception as e:
            traceback.print_exc()


    @app_commands.command(name = "select_kick", description = "Sirve para mostrarte en varias listas los usuarios para kickiarlos.")
    async def view_base(self, interaction: discord.Interaction, server: int = 0):
        await interaction.response.defer()
        serveri = ""
        if server == None or server == 1:
            serveri = "8012"
        if server == 2:
            serveri = "8011"
        if server == 3:
            serveri = "8010"
        file = discord.File("./res/logo.png", filename="logo.png")
        rolename = get(interaction.guild.roles, id=int(env('ROLE_ID')))
        url = f"http://rconctm.xyz:{serveri}/api/get_detailed_players"
        response = requests.get(url, headers=auth)
        if rolename in interaction.user.roles:
            try:
                if response.status_code == 200:
                    data = response.json()
                    players = data.get('result', {}).get('players', {})
                    player_list = [
                        {
                            'player_id': player_id,
                            'player': player_data.get("name")
                        }
                        for player_id, player_data in players.items()
                    ]
                    select_embed =  discord.Embed(title="Kick",description="Para poder kickiar a alguien tienes que seleccionarlo en la parte inferior en alguno de los boxes.", color=discord.Color.green())
                    select_embed.set_thumbnail(url="attachment://logo.png")

                    
                    #for index, chunk in enumerate(chunks):
                        
                    chunks = [
                        [
                        discord.SelectOption(
                            label=player["player"],
                            description=f"ID: {player['player_id']}",
                            value=f"{player['player']}|{player['player_id']}"
                        )
                        for player in player_list[i:i + 25]
                        ]
                        for i in range(0, len(player_list), 25)
                    ]


                    await interaction.followup.send(file=file, embed=select_embed)
                    for index, chunk in enumerate(chunks):
                        view = MyView([chunk], f"Página {index + 1}", interaction.user.id, serveri)
                        await interaction.followup.send(
                            view=view
                        )
            except Exception as e:
                traceback.print_exc()
        else:
                role_embed =  discord.Embed(title=f"Necesitas tener el rol de {rolename}", color=discord.Color.red())
                role_embed.set_thumbnail(url="attachment://logo.png")
                await interaction.followup.send(file=file, embed=role_embed)


    @app_commands.command(name = "message", description = "Envia un mensaje a un jugador.")
    async def message(self, interaction: discord.Interaction, id: str, message: str, server: int = 0):
        await interaction.response.defer()
        serveri = ""
        if server == 0 or server == 1:
            serveri = "8012"
        if server == 2:
            serveri = "8011"
        if server == 3:
            serveri = "8010"
        rolename = get(interaction.guild.roles, id=int(env('ROLE_ID')))
        file = discord.File("./res/logo.png", filename="logo.png")
        name = None
        if rolename in interaction.user.roles:
            try:
                if server <= 3:
                    if id == "all":
                        print("test")
                        url = f"http://rconctm.xyz:{serveri}/api/get_detailed_players"
                        all_embed =  discord.Embed(title="Se a enviado correctamente.",description=f"Se envio correctamente el siguente mensaje {message} a todo el server.", color=discord.Color.green())
                        all_embed.set_thumbnail(url="attachment://logo.png")
                        all_embed.set_footer(text="Tarda unos segundos en enviarse a todos.")


                        async with aiohttp.ClientSession(headers=auth) as session:
                            async with session.get(url) as response:
                                data = await response.json()
                                players = data.get('result', {}).get('players', {})


                                task = []
                                for player_id, player_data in players.items():
                                    data_request = {
                                        "player_name": player_data.get("name"),
                                        "player_id": player_id,
                                        "message": message
                                    }

                                    task.append(
                                        session.post(f"http://{env('IP_VPS')}:{serveri}/api/message_player", json=data_request)
                                    )
                                await asyncio.gather(*task)
                        await interaction.followup.send(file=file, embed=all_embed)
                    else:
                        if await check_steamid(id):
                            name = await request_steamid(id)
                        elif await check_epicid(id):
                            name = await check_epicid(id)
                        if await check_epicid(id) != None or await check_steamid(id):
                            if await check_game(id):
                                datos = {'player_name': name, 'player_id': id, 'message': message}
                                requests.post(f"http://{env('IP_VPS')}:{serveri}/api/message_player", data=json.dumps(datos), headers=auth)
                                message_embed =  discord.Embed(title=f"Se le envio un mensaje a {name}", description=f"Se le envio correctamente el siguente mensaje: {message}", color=discord.Color.green())
                                message_embed.set_thumbnail(url="attachment://logo.png")
                                await interaction.followup.send(file=file, embed=message_embed)
                                #print(r.text)
                            else:
                                errorsteamid_embed =  discord.Embed(title="No esta dentro del juego.", color=discord.Color.red())
                                errorsteamid_embed.set_thumbnail(url="attachment://logo.png")
                                await interaction.followup.send(file=file, embed=errorsteamid_embed)
                        else:
                            errorgame_embed =  discord.Embed(title="Id inconrrecto debe ser de epic o de steam.", color=discord.Color.red())
                            errorgame_embed.set_thumbnail(url="attachment://logo.png")
                            await interaction.followup.send(file=file, embed=errorgame_embed)
                else:
                    server_embed = discord.Embed(title="El server no existe.", color=discord.Color.red())
                    server_embed.set_thumbnail(url="attachment://logo.png")
                    await interaction.followup.send(file=file, embed=server_embed)
            except Exception as e:
                traceback.print_exc()
        else:
                role_embed =  discord.Embed(title=f"Necesitas tener el rol de {rolename}", color=discord.Color.red())
                role_embed.set_thumbnail(url="attachment://logo.png")
                await interaction.followup.send(file=file, embed=role_embed)
    @app_commands.command(name="info", description="Muestra los datos de los usuarios.")
    async def info(self, interaction: discord.Interaction, server: int = 0):
        serveri = ""
        if server == 0 or server == 1:
            serveri = "8012"
        if server == 2:
            serveri = "8011"
        if server == 3:
            serveri = "8010"
        await interaction.response.defer()
        rolename = get(interaction.guild.roles, id=int(env('ROLE_ID')))
        file = discord.File("./res/logo.png", filename="logo.png")
        if rolename in interaction.user.roles:
            try:
                if server <= 3:
                    paginator = PlayerListPaginator(server)
                    asyncio.create_task(self.fetch_live_game_stats(paginator, serveri))
                    embed = paginator.generate_embed()
                    await interaction.followup.send(embed=embed)
                    message = await interaction.original_response()

                    max_pages = paginator.max_pages
                    reactions = [f"{i}️⃣" for i in range(1, max_pages + 1)]

                    for reaction in reactions:
                        await message.add_reaction(reaction)

                    def check(reaction, user):
                        # Permitir que cualquier usuario reaccione
                        return (
                            str(reaction.emoji) in reactions  # Permitir reacciones numéricas
                            and reaction.message.id == message.id
                        )
                    
                    while True:
                        try:
                            reaction, user = await interaction.client.wait_for("reaction_add", check=check)

                            # Cambiar la página en función del emoji seleccionado
                            page_number = reactions.index(str(reaction.emoji))
                            paginator.set_page(page_number)
                            await message.edit(embed=paginator.generate_embed())

                            # Removemos la reacción del usuario para evitar desorden
                            await message.remove_reaction(reaction, user)
                        except discord.errors.NotFound:
                            # Si el mensaje es eliminado, salimos del bucle
                            break
                else:
                    server_embed = discord.Embed(title="El server no existe.", color=discord.Color.red())
                    server_embed.set_thumbnail(url="attachment://logo.png")
                    await interaction.followup.send(file=file, embed=server_embed)
            except Exception as e:
                traceback.print_exc()
        else:
                role_embed =  discord.Embed(title=f"Necesitas tener el rol de {rolename}", color=discord.Color.red())
                role_embed.set_thumbnail(url="attachment://logo.png")
                await interaction.followup.send(file=file, embed=role_embed)





            
        
         







async def setup(bot):
    await bot.add_cog(utils(bot))





