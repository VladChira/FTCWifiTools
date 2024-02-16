class Team:
    def __init__(self):
        self.interface_name = "wlps10"
        self.dropDownSelectedInterface = 0
        self.team_name = "TITANS"
        self.team_number = ""
        self.MAC_address = ""
        self.channel = "unknown"
        self.dropdownTeamNumber = 0
        self.capture_message = "Not ready to capture"
        self.status_message = ""
        self.tshark_output = ""
        self.overriden = False
        self.override_text = "1"

    def update_capture_message(self):
        if "interface" in self.interface_name:
            self.capture_message = "Not ready to capture. Please select a valid interface."
            return
        if self.team_number == "" or self.channel == "unknown":
            self.capture_message = f"Not ready to capture on {self.interface_name}"
            return

        self.capture_message = f"Ready to capture on {self.interface_name} - Team {self.team_number} {self.team_name} - Channel {self.channel}"

    def update(self, INT_NAMES, TEAM_NAMES):
        if self.overriden:
            self.status_message = ""
            if self.override_text.isdigit():
                self.channel = self.override_text

        # Update the team number and name
        self.team_number = TEAM_NAMES[self.dropdownTeamNumber]
        self.team_name = ""  # todo using hashmap

        # Update the team capture message displayed above their terminals
        self.update_capture_message()

        # Update the interface for each team based on the dropdown
        self.interface_name = INT_NAMES[self.dropDownSelectedInterface]
