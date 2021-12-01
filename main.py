import os
import requests
import asyncio


class Overlay():

    user_path = '/'.join(os.getcwd().split('\\', 3)[:3])
    logFiles = {
        "Minecraft" : f"{user_path}\\AppData\\Roaming\\.minecraft\\logs\\latest.log",
        "Lunar Client" : f"{user_path}\\.lunarclient\\logs\\launcher\\renderer.log"
    }

    def __init__(self):
        self.currentPlayers = []
        self.antisniper_api = "http://api.antisniper.net/antisniper?key={api_key}&uuid={uuid}"

    @classmethod
    def get_file(cls) -> str:
        return

    def get_all_players(self, line:str) -> list:
        return

    def get_player(self, player:str) -> str:
        return

    def check_new_lobby(self) -> bool:
        return

    def player_joined(self) -> str:
        return

    def player_quit(self) -> str:
        return

    def reset_all(self) -> None:
        pass


class Stats():

    def __init__(self):
        self.cachePlayers = []

    def get_uuid(self, player:str) -> str:
        return

    def get_rank(self, player:str) -> str:
        return
    
    def denick(self, nick:str) -> str:
        return

    def check_sniper(self, player:str):
        return

    def get_overall_stats(self, player:str) -> tuple:
        return


