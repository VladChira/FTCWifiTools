import threading

from teams.blue_team1 import BlueTeam1
from teams.blue_team2 import BlueTeam2
from teams.red_team1 import RedTeam1
from teams.red_team2 import RedTeam2


class TeamManager:
    _instance = None
    _lock = threading.Lock()

    teams = ["19103", "21050", "22226", "15991", "15989", "19117", "19055",
                              "24266", "21476", "16166", "19064"]
    
    BlueTeam1: BlueTeam1
    BlueTeam2: BlueTeam2 
    RedTeam1: RedTeam1
    RedTeam2: RedTeam2

    def update_teams(self, INT_NAMES):
        self.BlueTeam1.update(INT_NAMES, self.teams)
        self.BlueTeam2.update(INT_NAMES, self.teams)
        self.RedTeam1.update(INT_NAMES, self.teams)
        self.RedTeam2.update(INT_NAMES, self.teams)

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance.BlueTeam1 = BlueTeam1()
                    cls._instance.BlueTeam2 = BlueTeam2()
                    cls._instance.RedTeam1 = RedTeam1()
                    cls._instance.RedTeam2 = RedTeam2()
        return cls._instance