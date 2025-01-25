import discord
import requests
import json
from check import env, auth
import traceback

class MyView(discord.ui.View):

    def __init__(self, chunks, placeholder="Elije al jugador", user_id=None, serveri="8012"):
        super().__init__()
        self.user_id = user_id
        self.serveri = serveri
        for options in chunks:
            select_menu = discord.ui.Select(
                placeholder=placeholder,
                min_values=1,
                max_values=1,
                options=options,
                row=2
            )
            select_menu.callback = self.create_select_callback()
            self.add_item(select_menu)

    def create_select_callback(self):
        async def select_callback(interaction: discord.Interaction):
            server = self.serveri
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(
                    "Este menú solo puede ser usado por el usuario que lo invocó.",
                    ephemeral=True
                )
                return


            try:
                file = discord.File("./res/logo.png", filename="logo.png")
                selected_value = interaction.data["values"][0]
                selected_player, selected_player_id = selected_value.split('|')
                datos = {'player_name': selected_player, 'reason': '', 'by': 'admin', 'player_id': selected_player_id}
                requests.post(f"http://{env('IP_VPS')}:{server}/api/kick", data=json.dumps(datos), headers=auth)
                #print(r.text)
                kick_embed =  discord.Embed(title=f"{selected_player}'s fue kickeado", description=f"{selected_player}'s fue kickeado con id {selected_player_id} correctamente por {interaction.user}'s", color=discord.Color.red())
                kick_embed.set_thumbnail(url="attachment://logo.png")
                await interaction.response.send_message(
                    file=file, embed=kick_embed,
                    delete_after = 10
                )
            except Exception as e:
                traceback.print_exc()
        return select_callback