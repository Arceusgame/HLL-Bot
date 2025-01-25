import json
import requests
from dotenv import load_dotenv, dotenv_values

async def request_steamid(id: str):
        """Verifica si el Steam ID existe utilizando una API externa"""
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=76027F30FB6E9B10935C4AE24BAB3EBF&steamids={id}"
    
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'players' in data['response']:
                for player in data['response']['players']:
                     print(player["personaname"])

                     return player["personaname"]
        return None

def env(dato):
        get = dotenv_values(".env")
        return get[dato]

auth = {
    "Authorization": f"bearer {env("KEY")}",
    "Connection": "keep-alive",
    "Content-Type": "application/json"
}

async def check_game(id: str):
    url_stats = "http://rconctm.xyz:8010/api/get_detailed_players"

    # Obtener estadísticas del juego if player["player_id"] == id or player["player"] == name:
    try:
        respond_stats = requests.get(url_stats, headers=auth)
        respond_stats.raise_for_status()    
        game_data = respond_stats.json()
        if 'result' in game_data and 'players' in game_data['result']:
            if id in game_data['result']['players']:
                return True
    except requests.RequestException as e:
        print(f"Error al obtener datos del juego: {e}")
        return False

    return False
              


async def check_steamid(id: str):
        """Verifica si el Steam ID existe utilizando una API externa"""
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=76027F30FB6E9B10935C4AE24BAB3EBF&steamids={id}"
    
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'players' in data['response']:
                players = data['response']['players']
                if players:  # Si hay jugadores con ese Steam ID
                    return True
        return False

async def check_epicid(id: str):
     url = "http://rconctm.xyz:8010/api/get_detailed_players"


     response = requests.get(url, headers=auth)
     if response.status_code == 200:
          data = response.json()
          if 'result' in data and 'players' in data['result']:
               for player_id, player_data in data['result']['players'].items():
                    if player_id == id:
                         print(player_data["name"])

                         return player_data["name"]
     return None
     