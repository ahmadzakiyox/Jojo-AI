# File: modules/utils.py
import datetime
from colorama import Fore, Style, init
import pyfiglet
import json

# Muat profil untuk banner
try:
    with open("jojo_profile.json", "r", encoding="utf-8") as f:
        jojo_profile = json.load(f)
except FileNotFoundError:
    jojo_profile = {}

def log_message(actor, message):
    """Mencetak pesan dengan format log yang konsisten."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{actor.upper()}] >> {message}")

def display_welcome_banner():
    """Menampilkan banner startup yang keren."""
    init(autoreset=True)
    font = pyfiglet.Figlet(font='slant')
    ai_name = jojo_profile.get('ai_name', 'JOJO AI')
    creator_name = jojo_profile.get('creator_name', 'Ahmad Zaki')
    
    welcome_text = font.renderText(ai_name)
    
    print(Fore.CYAN + Style.BRIGHT + welcome_text)
    print(Style.BRIGHT + Fore.YELLOW + f"================= Created by: {creator_name} =================")
    print("") # Spasi