import os
import psutil
import requests
import asyncio

from threading import Thread
from dotenv import load_dotenv

class Overlay(Thread):

    user_path = '\\'.join(os.getcwd().split('\\', 3)[:3])
    logFiles = {
        "Minecraft" : f"{user_path}\\AppData\\Roaming\\.minecraft\\logs\\latest.log",
        "Lunar Client" : f"{user_path}\\.lunarclient\\logs\\launcher\\renderer.log"
    }

    def __init__(self):
        super().__init__()
        self.currentPlayers = []


    @classmethod
    def get_PID(cls, name:str):
        """Get Process's PID"""
        return [p.pid for p in psutil.process_iter(attrs=['pid', 'name']) if name.lower() in p.name().lower()][0]


    @classmethod
    def get_file(cls) -> str:
        """Get the latest log file"""
        for file in cls.logFiles.values():
            if (os.path.isfile(file) and os.path.getmtime(file) >= psutil.Process(cls.get_PID("javaw.exe")).create_time()):
                return file


    def read_log_file(self) -> str:
        """Return The Last Line of "[CHAT]" Log"""
        with open(Overlay.logFiles["Lunar Client"]) as logFile:
            return [log.strip() for log in logFile.readlines()[-3:] if log != "\n"][-1]


    def get_all_players(self) -> list:
        log = self.read_log_file()
        if "[CHAT] ONLINE: " in log:
            self.reset_all()
            self.currentPlayers = log[log.index("[CHAT] ONLINE:") + 15:].rstrip("\n").split(", ")


    def check_new_lobby(self) -> bool:
        log = self.read_log_file()
        if "Sending you to mini" in log:
            self.reset_all()


    def player_joined(self) -> str:
        log = self.read_log_file()
        if "has joined (" in log:
            return log[log.index("[CHAT]") + 7:log.index("has joined") - 1]


    def player_quit(self) -> str:
        log = self.read_log_file()
        if "has quit!" in log:
            return log[log.index("[CHAT]") + 7:log.index("has quit") - 1]


    def reset_all(self) -> None:
        self.currentPlayers.clear()
    

    def run(self):
        pass


class Stats():

    def __init__(self):
        self.cachePlayers = []

        # APIs
        self.MojangAPI = "https://api.mojang.com/users/profiles/minecraft/{}?"
        self.HypixelAPI = "https://api.hypixel.net/player?key={}&uuid={}"
        self.AntiSniperAPI = "http://api.antisniper.net/{}?key={}&{}={}"

        # API Keys
        self.hypixel_ApiKey = os.getenv("Hypixel_API_KEY")
        self.antisniper_ApiKey = os.getenv("AntiSniper_API_KEY")


    def get_uuid(self, player:str) -> str:
        response = requests.get(self.MojangAPI.format(player))
        if response.status_code != 200:
            denick = self.denick(player)
            if not denick:
                return denick
            return denick
        return response.json()["id"]


    def get_player_data(self, player:str):
        uuid = self.get_uuid(player)
        if not uuid:
            return
        return requests.get(self.HypixelAPI.format(self.hypixel_ApiKey, uuid)).json()["player"]


    def get_rank(self, player:str) -> str:
        data = self.get_player_data(self.get_uuid(player))
        rank = data["newPackageRank"]
        if "newPackageRank" not in data:
            return ""
        if rank == 'MVP':
            return "[MVP]"
        elif rank == 'MVP_PLUS':
            if "monthlyPackageRank" in data:
                mvp_plus_plus = data["monthlyPackageRank"]
                return "[MVP+]" if mvp_plus_plus == "NONE" else "[MVP++]"
        elif rank == 'VIP':
            return "[VIP]"
        elif rank == 'VIP_PLUS':
            return "[VIP+]"
    

    def denick(self, nick:str) -> str:
        response = requests.get(self.AntiSniperAPI.format("denick", self.antisniper_ApiKey, "nick", nick))
        if response.status_code != 200:
            return None
        return response.json()["player"]["uuid"]


    def check_sniper(self, player:str):
        response = requests.get(self.AntiSniperAPI.format("antisniper", self.antisniper_ApiKey, "name", self.get_player_data(player)["displayname"]))
        return


    def get_overall_stats(self, player:str) -> tuple:
        return


if __name__ == "__main__":
    load_dotenv()
    overlay = Overlay()
    overlay.start()

