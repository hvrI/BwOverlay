import os
import psutil
import requests
import asyncio


class Overlay():

    user_path = '\\'.join(os.getcwd().split('\\', 3)[:3])
    logFiles = {
        "Minecraft" : f"{user_path}\\AppData\\Roaming\\.minecraft\\logs\\latest.log",
        "Lunar Client" : f"{user_path}\\.lunarclient\\logs\\launcher\\renderer.log"
    }
    Minecraft = Lunar_Client = None


    def __init__(self):
        self.currentPlayers = []

    @classmethod
    def get_PID(cls, name:str):
        return [p.pid for p in psutil.process_iter(attrs=['pid', 'name']) if name.lower() in p.name().lower()][0]

    @classmethod
    def get_file(cls) -> str:
        for file in cls.logFiles.values():
            if os.path.isfile(file) and os.path.getmtime(file) >= psutil.Process(cls.get_PID("javaw.exe")).create_time():
                return file

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
    
    def launcher(self):
        print(self.get_file())


class Stats():

    def __init__(self):
        self.cachePlayers = []

        # APIs
        self.MojangAPI = "https://api.mojang.com/users/profiles/minecraft/{}?"
        self.HypixelAPI = "https://api.hypixel.net/player?key={}&uuid={}"
        self.AntiSniperAPI = "http://api.antisniper.net/antisniper?key={}&{}={}"

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

if __name__ == "__main__":
    overlay = Overlay()
    overlay.launcher()

