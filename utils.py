import subprocess

INTERFACE_NAMES = ["<interface 1>", "<interface 2>", "<interface 3>", "<interface 4>"]

def load_interfaces():
    global INTERFACE_NAMES
    command = "sudo airmon-ng | awk '/^[[:space:]]*phy[0-9]+/{print $2}'"
    
    try:
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    except OSError as e:
        print(f"Error opening pipe: {e}")
        return
    
    result = ""
    while True:
        line = pipe.stdout.readline().decode().strip()
        if not line:
            break
        for i in range(4):
            if "<interface" in INTERFACE_NAMES[i]:
                INTERFACE_NAMES[i] = line
                break
    
    pipe.stdout.close()
    pipe.wait()