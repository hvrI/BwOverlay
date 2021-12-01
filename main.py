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

    def __init__(self):
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


    def get_all_players(self, log:str=read_log_file()) -> list:
        if "[CHAT] ONLINE: " in log:
            self.reset_all()
            self.currentPlayers = log[log.index("[CHAT] ONLINE:") + 15:].rstrip("\n").split(", ")


    def get_player(self, player:str) -> str:
        return


    def check_new_lobby(self, log:str=read_log_file()) -> bool:
        if "Sending you to mini" in log:
            self.reset_all()


    def player_joined(self, log:str=read_log_file()) -> str:
        if "has joined (" in log:
            return log[log.index("[CHAT]") + 7:log.index("has joined") - 1]


    def player_quit(self, log:str=read_log_file()) -> str:
        if "has quit!" in log:
            return log[log.index("[CHAT]") + 7:log.index("has quit") - 1]


    def reset_all(self) -> None:
        pass
    

    def launcher(self):
        print(self.read_log_file())


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

