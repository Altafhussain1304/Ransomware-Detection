import os
import subprocess
import psutil
from datetime import datetime
import time
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print("==== RansomSaver - Main Menu ====")
        print("1. Start File Monitoring")
        print("2. Start Process Monitoring")
        print("3. Start System Monitoring")
        print("4. Start Network Monitoring")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            subprocess.run([sys.executable, "file_monitor.py"])
        elif choice == "2":
            subprocess.run([sys.executable, "process_monitor.py"])
        elif choice == "3":
            subprocess.run([sys.executable, "system_monitor.py"])
        elif choice == "4":
            subprocess.run([sys.executable, "network_monitor.py"])
        elif choice == "5":
            print("Exiting RansomSaver Goodbye!")
            time.sleep(1)
            break
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(2)

if __name__ == "__main__":
    main_menu()


