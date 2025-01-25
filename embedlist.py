import discord
import requests
from check import auth
import asyncio

#run = True
#while True:
    #url = "http://rconctm.xyz:8010/api/get_live_game_stats"

    #response = requests.get(url, headers=auth)
    #data = response.json()['result']['stats']
    #time.sleep(15)



class PlayerListPaginator:
    def __init__(self, serveri, max_chars=1024):
        self.players = [] # Lista de jugadores
        self.max_chars = max_chars
        self.current_page = 0
        self.max_pages = 0
        self.serveri = serveri

    def update_data(self, players):
        self.players = players
        self.max_pages = self.calculate_max_pages()

    def calculate_max_pages(self):
        """Calcula cuántas páginas se necesitan según el límite de caracteres."""
        pages = []
        current_page_players = []
        current_chars = 0

        for player in self.players:
            player_str = f"`{player['player']}                  <{player['player_id']}>`\n"
            player_len = len(player_str)

            # Si agregar al jugador excede el límite de caracteres, agregamos una nueva página
            if current_chars + player_len > self.max_chars:
                if current_page_players:
                    pages.append(current_page_players)  # Guardamos la página actual
                current_page_players = [player]  # Comenzamos una nueva página
                current_chars = player_len
            else:
                current_page_players.append(player)  # Agregamos el jugador a la página actual
                current_chars += player_len

        # Agregar la última página de jugadores
        if current_page_players:
            pages.append(current_page_players)

        return len(pages)

    def generate_embed(self):
        """Genera un embed con la página actual de jugadores."""
        start = self.current_page * 30  # Multiplicamos por 30 jugadores por página
        end = start + 30
        players_slice = self.players[start:end]  # Tomamos un segmento de 30 jugadores
        server = self.serveri

        # Verificamos si players_slice es una lista de diccionarios
        player_list_string = ""
        for player in players_slice:
            player_list_string += f"`{player['player']}                  <{player['player_id']}>`\n"

        # Dividimos el contenido en campos si excede el límite de 1024 caracteres
        fields = []
        current_field = ""
        for player in players_slice:
            player_str = f"`{player['player']}                  <{player['player_id']}>`\n"
            if len(current_field) + len(player_str) > self.max_chars:
                fields.append(current_field)
                current_field = player_str  # Comenzamos un nuevo campo
            else:
                current_field += player_str

        if current_field:
            fields.append(current_field)  # Agregamos el último campo
        
        if server == 0:
            server = 1

        # Crear el embed
        embed = discord.Embed(
            title=f"Lista de Jugadores (Página {self.current_page + 1}/{self.max_pages}) (Server {str(server)})",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Debes actualizar la pagina cambiando de pagina.")

        # Agregar los campos al embed
        for i, field in enumerate(fields):
            embed.add_field(
                name=f"Jugadores (Campo {i + 1})",
                value=field,
                inline=False
            )

        return embed

    def set_page(self, page_number):
        """Establece la página actual para la paginación."""
        if 0 <= page_number < self.max_pages:
            self.current_page = page_number
