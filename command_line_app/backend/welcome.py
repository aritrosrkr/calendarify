# welcome.py
import sys
import os
import platform
import time
import pyfiglet
from colorama import init, Fore


# Initialize colorama
init(autoreset=True)

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        print("\033c", end="")

def heading_h1(text):
    return Fore.RED + pyfiglet.figlet_format(text, font="slant")

def heading_h2(text):
    return f"\n--- {text} ---\n"

def footer_signature():
    text = f"made with ♥ by AKB"
    return Fore.RED + heading_h2(text)

def show_welcome():
    clear_terminal()

    print(heading_h1("Calendarify"))

    print("✨ Convert your BRACU class routine to a beautiful .ics calendar file.\n")
    print("📅 No more manual entry—just generate and import into Apple or Google Calendar!\n")

    print(heading_h2("This is a terminal-based app (Requires Internet)"))

    print(footer_signature())
    print("\nNote: Include lab courses in the course count if they carry separate credit \nor aren’t integrated with the main course (unlike in the CSE Department).\n")
    startStop = input("👉 Would you like to proceed? [Y/N]: ")
    clear_terminal()
    if startStop == 'Y':
        print("Starting Calendarify... 🚀🚀")
        time.sleep(1)
    else:
        print("Looking forward to seeing you again with Calendarify. Goodbye for now! 👋👋")
        clear_terminal()
        sys.exit(0)