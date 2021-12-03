import os
import sys
import psutil
import requests

from multiprocessing.pool import ThreadPool
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
        self.cachePlayers = {}
        self.currentPlayers = []
        self.check = True


    @classmethod
    def get_PID(cls, name:str):
        """Get Process's PID"""
        result = [p.pid for p in psutil.process_iter(attrs=['pid', 'name']) if name.lower() in p.name().lower()]
        if result == []:
            print("You do not have Minecraft running.")
            sys.exit(1)
        return result[0]


    @classmethod
    def get_file(cls) -> str:
        """Get the latest log file"""
        for file in cls.logFiles.values():
            if (os.path.isfile(file) and os.path.getmtime(file) >= psutil.Process(cls.get_PID("javaw.exe")).create_time()):
                return file


    def read_log_file(self) -> str:
        """Return The Last Line of "[CHAT]" Log"""
        with open(self.get_file()) as logFile:
            return [log.strip() for log in logFile.readlines()[-3:] if log != "\n"][-1]


    def reset_all(self) -> None:
        self.currentPlayers.clear()
        self.cachePlayers.clear()


    def get_all_stats(self):
        threads = []
        def stats(player):
            stats = Stats()
            return self.cachePlayers.update(stats.get_overall_stats(player))

        for player in self.currentPlayers:
            t = Thread(target=stats, args=[player])
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()


    def get_stats(self, player:str):
        stats = Stats()
        pool = ThreadPool(processes=1)
        t = pool.apply_async(stats.get_overall_stats, (player,))
        return t.get()


    def update_display(self):
        os.system("cls")
        for player, stats in self.cachePlayers.items():
            player+=(" "*(23-(len(player)+len(str(stats[0])))))
            stars = str(stats[1])
            ws = str(stats[4])
            fkdr = str(stats[3])
            wlr = str(stats[2])

            stars+=(" "*(5-len(stars)))
            ws+=(" "*(5-len(ws)))
            fkdr+=(" "*(7-len(fkdr)))
            wlr+=(" "*(7-len(wlr)))

            if len(stats) == 1:
                print(f"{player} | tag: {stats[0]}")
            elif len(stats) == 6:
                print(f"{stats[0]} {player} | stars: {stars} | WS: {ws} FKDR: {fkdr} WLR: {wlr} Sniper: {stats[5]}")
            else:
                print(f"{stats[0]} {player} | stars: {stars} | WS: {ws} FKDR: {fkdr} WLR: {wlr} Sniper: {stats[6]}  Nick: {stats[5]}")
 

    def run(self):
        while 1:
            log = self.read_log_file()
            if "Sending you to mini" in log:
                self.reset_all()
                self.check = True

            if self.check and "[CHAT] ONLINE: " in log:
                self.reset_all()
                self.currentPlayers = log[log.index("[CHAT] ONLINE:") + 15:].rstrip("\n").split(", ")
                self.get_all_stats()
                self.check = False
                self.update_display()

            if "has joined (" in log:
                self.check = True
                new_player = log[log.index("[CHAT]") + 7:log.index("has joined") - 1]
                if new_player not in self.currentPlayers:
                    self.currentPlayers.append(new_player)
                    self.cachePlayers.update(self.get_stats(new_player))
                    self.update_display()
            
            if "has quit!" in log:
                self.check = True
                left_player = log[log.index("[CHAT]") + 7:log.index("has quit") - 1]
                if left_player in self.currentPlayers:
                    self.currentPlayers.remove(left_player)


class Stats():

    def __init__(self):

        # APIs
        self.MojangAPI = "https://api.mojang.com/users/profiles/minecraft/{}?"
        self.HypixelAPI = "https://api.hypixel.net/player?key={}&uuid={}"
        self.AntiSniperAPI = "http://api.antisniper.net/{}?key={}&{}={}"

        # API Keys
        self.hypixel_ApiKey = os.getenv("Hypixel_API_KEY")
        self.antisniper_ApiKey = os.getenv("AntiSniper_API_KEY")


    def get_uuid(self, player:str):
        """Get player's UUID"""
        with requests.Session() as r:
            response = r.get(self.MojangAPI.format(player))
        if response.status_code != 200:
            denick = self.denick(player)
            if not denick:
                return denick
            return (denick, False) # Return uuid if can be denicked
        return response.json()["id"]


    def get_player_data(self, player:str):
        """Get player's Hypixel Player Data"""
        uuid = self.get_uuid(player)
        if not uuid:
            return "NICKED" # Denick Unsuccessful
        with requests.Session() as r:
            if not uuid[1]:
                return (r.get(self.HypixelAPI.format(self.hypixel_ApiKey, uuid[0])), "DENICKED")
            else:
                return (r.get(self.HypixelAPI.format(self.hypixel_ApiKey, uuid)), "Not Nick")


    def get_rank(self, data) -> str:
        """Get Player's Hypixel Rank"""
        if "newPackageRank" not in data:
            return ""
        rank = data["newPackageRank"]
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
        """Denick a nicked player"""
        with requests.Session() as r:
            response = r.get(self.AntiSniperAPI.format("denick", self.antisniper_ApiKey, "nick", nick))
        if response.status_code != 200:
            return None
        return response.json()["player"]["uuid"]


    def check_sniper(self, display_name:str):
        """If player requeues a weight above 25.0"""
        with requests.Session() as r:
            response = r.get(self.AntiSniperAPI.format("antisniper", self.antisniper_ApiKey, "name", display_name))
        if response.status_code != 200:
            return None
        return bool(response.json()["data"][display_name.lower()]["queues"]["consecutive_queue_checks"]["weighted"]["1_min_requeue"] >= 30.0)


    def get_estimate_winstreak(self, player:str):
        """Get player's estimated winstreak"""
        with requests.Session() as r:
            response = r.get(self.AntiSniperAPI.format("winstreak", self.antisniper_ApiKey, "name", player))
        if response.status_code != 200:
            return 0
        return response.json()["player"]["data"]["overall_winstreak"]
        

    def get_overall_stats(self, player:str) -> dict:
        data = self.get_player_data(player)
        if data == "NICKED":
            return {player : ("NICKED",)}
        nick = player if data[1] == "DENICKED" else None
        data = data[0].json()["player"]
        rank = self.get_rank(data)
        display_name = data["displayname"]
        is_sniper = self.check_sniper(display_name)
        bedwarsData = data["stats"]["Bedwars"]
        stars = data["achievements"].get("bedwars_level", 0)
        try:
            wlr = round(bedwarsData.get("wins_bedwars", 0) / bedwarsData.get("losses_bedwars", 0), 2)
        except ZeroDivisionError:
            wlr = bedwarsData.get("wins_bedwars", 0)
        try:
            fkdr = round(bedwarsData.get("final_kills_bedwars", 0) / bedwarsData.get("final_deaths_bedwars", 0), 2)
        except ZeroDivisionError:
            fkdr = bedwarsData.get("final_kills_bedwars", 0)
        try:
            winstreak = bedwarsData["winstreak"]
        except KeyError: # If winstreak API is off
            winstreak = self.get_estimate_winstreak(display_name)
        finally:
            if is_sniper is None:
                is_sniper = False
            if not nick:
                return {display_name : (rank, stars, wlr, fkdr, winstreak, is_sniper)} # If no nick
            return {display_name : (rank, stars, wlr, fkdr, winstreak, nick, is_sniper)} # If nicked + denicked



if __name__ == "__main__":
    load_dotenv()
    overlay = Overlay()
    overlay.start()

