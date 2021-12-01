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
    def get_file(cls):
        return

    def get_all_players(self, line:str):
        return

    def get_player(self, player:str):
        pass

    def check_new_lobby(self) -> bool:
        return

    def player_joined(self):
        pass

    def player_quit(self):
        pass

    def reset_all(self):
        pass


class Stats():

    def __init__(self):
        self.cachePlayers = []

    def get_uuid(self, player:str) -> str:
        return

    def get_rank(self, player:str) -> str:
        return

    def get_overall_stats(self, player:str) -> tuple:
        return

