from enum import Enum
import threading
import subprocess
import time
import os

from utils import INTERFACE_NAMES
from teams.team_manager import TeamManager

class AIRODUMP_STATE(Enum):
    RUNNING = 0
    STOPPED = 1

class AirodumpManager:
    _instance = None
    _lock = threading.Lock()

    state = AIRODUMP_STATE.STOPPED

    __airodump_process = None

    __stop_event: threading.Event = None
    __scanning_thread: threading.Thread = None

    output = ""

    def start(self, interface_name):
        if self.state == AIRODUMP_STATE.RUNNING or not self.__airodump_process is None:
            print('Airodump already running')
            return
        
        try:
            os.remove("temp-01.csv")
        except OSError:
            pass

        command = [
            "sudo",
            "airodump-ng",
            interface_name,
            "--band",
            "abg",
            "-w",
            "temp",
            "--output-format",
            "csv",
            "--write-interval",
            "2",
            "-K",
            "0"
        ]
        # Launch airodump process in the background
        self.__airodump_process = subprocess.Popen(command, stdout=subprocess.DEVNULL)

        # Launch the thread that reads the file
        file_path = "temp-01.csv"
        self.__stop_event = threading.Event()
        self.__scanning_thread = threading.Thread(target=self.__file_scanner, args=(file_path, self.__stop_event))
        self.__scanning_thread.start()
        self.state = AIRODUMP_STATE.RUNNING

    def stop(self):
        if self.state is AIRODUMP_STATE.STOPPED:
            return
        
        self.output = ""

        # Stop airodump
        if not self.__airodump_process is None:
            self.__airodump_process.kill()
            self.__airodump_process.wait()
            self.__airodump_process = None

        # Stop the scanning thread
        if not self.__scanning_thread is None or self.__scanning_thread.is_alive():
            self.__stop_event.set()
            self.__scanning_thread.join()
            self.__scanning_thread = None
        
        self.state = AIRODUMP_STATE.STOPPED
   
        try:
            os.remove("temp-01.csv")
        except OSError:
            pass

    def __file_scanner(self, file_path, stop_event):
        while not stop_event.is_set():
            try:
                with open(file_path, 'r') as file:
                    data = file.read()
                    if not "BSSID" in data:
                        continue
                    lines = data.split("\n")[2:]

                    stop_index = next(i for i, line in enumerate(lines) if "Station MAC" in line)
                    parsed_data = []
                    for line in lines[:stop_index]:
                        fields = line.split(',')
                        if len(fields) > 14:
                            parsed_data.append([fields[0], fields[3],fields[13]])
                    AirodumpManager().output = '\n'.join([','.join(fields) for fields in parsed_data])


                    # Now auto-detect the channels for each team
                    r1 = "DIGI-5wqN"
                    r2 = "DIGI-Vkdg"
                    b1 = "DIGI-7Uju"
                    b2 = "DIGI-BkzM"

                    foundR1 = False
                    foundR2 = False
                    foundB1 = False
                    foundB2 = False
                    for entry in parsed_data:
                        if entry[2].strip() == r1 and not TeamManager().RedTeam1.overriden:
                            foundR1 = True
                            TeamManager().RedTeam1.channel = entry[1].strip()
                        if entry[2].strip() == r2 and not TeamManager().RedTeam2.overriden:
                            foundR2 = True
                            TeamManager().RedTeam2.channel = entry[1].strip()
                        if entry[2].strip() == b1 and not TeamManager().BlueTeam1.overriden:
                            foundB1 = True
                            TeamManager().BlueTeam1.channel = entry[1].strip()
                        if entry[2].strip() == b2 and not TeamManager().BlueTeam2.overriden:
                            foundB2 = True
                            TeamManager().BlueTeam2.channel = entry[1].strip()

                    if foundR1:
                        TeamManager().RedTeam1.status_message = "Auto-detected channel " + TeamManager().RedTeam1.channel
                    else:
                        TeamManager().RedTeam1.status_message = "Could not find the RC for this team"

                    if foundR2:
                        TeamManager().RedTeam2.status_message = "Auto-detected channel " + TeamManager().RedTeam2.channel
                    else:
                        TeamManager().RedTeam2.status_message = "Could not find the RC for this team"

                    if foundB1:
                        TeamManager().BlueTeam1.status_message = "Auto-detected channel " + TeamManager().BlueTeam1.channel
                    else:
                        TeamManager().BlueTeam1.status_message = "Could not find the RC for this team"

                    if foundB2:
                        TeamManager().BlueTeam2.status_message = "Auto-detected channel " + TeamManager().BlueTeam2.channel
                    else:
                        TeamManager().BlueTeam2.status_message = "Could not find the RC for this team"

            except FileNotFoundError:
                pass
            
            if stop_event.is_set():
                return
        
            for i in range(2):
                if stop_event.is_set():
                    return
                time.sleep(0.5)

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance