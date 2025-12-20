#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# Beautiful color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

LOG_FILE = "system.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] {msg}\n")


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print(CYAN + """
██████╗  █████╗ ██████╗ ██╗  ██╗██╗    ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██║    ██║██╔════╝██╔══██╗
██████╔╝███████║██████╔╝█████╔╝ ██║ █╗ ██║█████╗  ██████╔╝
██╔═══╝ ██╔══██║██╔══██╗██╔═██╗ ██║███╗██║██╔══╝  ██╔══██╗
██║     ██║  ██║██║  ██║██║  ██╗╚███╔███╔╝███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝
    
       DARK-WEB TRAFFIC ANALYSIS & DETECTION ENGINE
                 Machine Learning Powered
""" + RESET)


def menu():
    print(YELLOW + "Main Menu" + RESET)
    print(GREEN + """
[1] Extract Features (PCAP → CSV)
[2] Train Model
[3] Predict Traffic (CSV)
[4] View System Logs
[5] Exit
""" + RESET)
    return input(CYAN + "Enter choice: " + RESET)


def run_script(script_name, args=None):
    python_exec = sys.executable  # uses VENV python
    cmd = [python_exec, script_name]

    if args:
        cmd.extend(args)

    try:
        print(YELLOW + f"\nRunning {script_name}..." + RESET)
        log(f"Running script: {script_name}")
        subprocess.run(cmd, check=True)
        print(GREEN + f"\n✔ {script_name} executed successfully!\n" + RESET)
    except subprocess.CalledProcessError as e:
        print(RED + f"\n✘ Error running {script_name}: {str(e)}\n" + RESET)
        log(f"Error in {script_name}: {str(e)}")


def view_logs():
    print(CYAN + "\n=== System Log ===\n" + RESET)
    if not os.path.exists(LOG_FILE):
        print(RED + "No logs found.\n" + RESET)
        return
    with open(LOG_FILE, "r") as f:
        print(f.read())
    print(CYAN + "\n=== End of Log ===\n" + RESET)


if __name__ == "__main__":
    clear()
    banner()

    while True:
        choice = menu()

        if choice == "1":
            run_script("fx.py")

        elif choice == "2":
            run_script("trainer.py")

        elif choice == "3":
            run_script("predictor.py")

        elif choice == "4":
            view_logs()
            input(YELLOW + "Press Enter to return to menu..." + RESET)
            clear()
            banner()

        elif choice == "5":
            print(GREEN + "\nExiting Dark-Web Detection Engine. Stay safe! :)\n" + RESET)
            log("Program exited by user.")
            break

        else:
            print(RED + "Invalid choice! Try again.\n" + RESET)
