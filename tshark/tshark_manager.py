from enum import Enum
import threading
import subprocess
import time
import os
import select

from utils import INTERFACE_NAMES
from teams.team_manager import TeamManager
from teams.team import Team

class TSHARK_STATE(Enum):
    RUNNING = 0
    STOPPED = 1

class TSharkManager:
    _instance = None
    _lock = threading.Lock()

    state = TSHARK_STATE.STOPPED

    __r1_thread: threading.Thread = None
    __r2_thread: threading.Thread = None
    __b1_thread: threading.Thread = None
    __b2_thread: threading.Thread = None
    __stop_event = None

    def run_tshark_instance(self, team: Team, stop_event: threading.Event):
        channel = team.channel
        interface = team.interface_name
        if "interface" in interface or channel == "unknown":
            return
        
        # display_filter = "-Y \"(wlan.fc.type == 0 && (wlan.fc.subtype == 0xc || wlan.fc.subtype == 0xa) && wlan_radio.channel == " + channel + ")\"";
        display_filter = "-Y \"(wlan_radio.channel == " + channel + ")\""
        command = "sudo tshark -i " + interface + " " + " -e frame.number -e _ws.col.Time -e wlan.sa -e wlan.da -T fields -t a"
    #     sudo tshark -i wlp1s0 -e frame.number -e frame.time -e wlan.sa -e wlan.da -e _ws.col.Info -T fields
    #    -Y \"(wlan.fc.type == 0 && (wlan.fc.subtype == 0xc || wlan.fc.subtype == 0xa))\"
        
        team.tshark_output = command
        # print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while not stop_event.is_set():
            ready = select.select([process.stdout], [], [], 0.3)
            if ready[0]:
                output_out = process.stdout.readline()
                if output_out:
                    team.tshark_output += output_out.decode()
            time.sleep(0.1)
        process.kill()
        process.wait()


    def start(self):
        if self.state == TSHARK_STATE.RUNNING:
            print('Tshark already running')
            return
        
        self.state = TSHARK_STATE.RUNNING
        
        # Wait if there are any threads not stopped already
        if not self.__r1_thread is None and self.__r1_thread.is_alive():
            self.__r1_thread.join()
        
        if not self.__r2_thread is None and self.__r2_thread.is_alive():
            self.__r2_thread.join()

        if not self.__b1_thread is None and self.__b1_thread.is_alive():
            self.__b1_thread.join()

        if not self.__b2_thread is None and self.__b2_thread.is_alive():
            self.__b2_thread.join()

        # Start the threads
        self.__stop_event = threading.Event()
        self.__r1_thread = threading.Thread(target=self.run_tshark_instance, args=(TeamManager().RedTeam1, self.__stop_event))
        self.__r1_thread.start()

        self.__r2_thread = threading.Thread(target=self.run_tshark_instance, args=(TeamManager().RedTeam2, self.__stop_event))
        self.__r2_thread.start()

        self.__b1_thread = threading.Thread(target=self.run_tshark_instance, args=(TeamManager().BlueTeam1, self.__stop_event))
        self.__b1_thread.start()

        self.__b2_thread = threading.Thread(target=self.run_tshark_instance, args=(TeamManager().BlueTeam2, self.__stop_event))
        self.__b2_thread.start()

    def stop(self):
        if self.state == TSHARK_STATE.STOPPED:
            return
        self.__stop_event.set()

        if not self.__r1_thread is None and self.__r1_thread.is_alive():
            self.__r1_thread.join()
        
        if not self.__r2_thread is None and self.__r2_thread.is_alive():
            self.__r2_thread.join()

        if not self.__b1_thread is None and self.__b1_thread.is_alive():
            self.__b1_thread.join()

        if not self.__b2_thread is None and self.__b2_thread.is_alive():
            self.__b2_thread.join()

        # Scroll down the tshark outputs if they are not empty
        if TeamManager().RedTeam1.tshark_output != "":
            TeamManager().RedTeam1.tshark_output += "\n\n\n\n"
        
        if TeamManager().RedTeam2.tshark_output != "":
            TeamManager().RedTeam2.tshark_output += "\n\n\n\n"

        if TeamManager().BlueTeam1.tshark_output != "":
            TeamManager().BlueTeam1.tshark_output += "\n\n\n\n"

        if TeamManager().BlueTeam2.tshark_output != "":
            TeamManager().BlueTeam2.tshark_output += "\n\n\n\n"

        self.state = TSHARK_STATE.STOPPED


    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance