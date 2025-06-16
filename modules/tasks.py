# File: modules/tasks.py
import os
import webbrowser
import datetime
import time
import pyautogui
import wikipedia
import json

from .voice import speak, listen_command
from .ai_brain import handle_conversation
from .utils import jojo_profile, log_message

# Setup awal
wikipedia.set_lang("id")

# --- Kumpulan Fungsi Eksekusi Tugas ---

def execute_task_get_time():
    str_time = datetime.datetime.now().strftime("%H:%M")
    speak(handle_conversation(f"Waktu saat ini adalah {str_time}. Beritahu pengguna dengan ramah."))

def execute_task_open_youtube():
    speak(handle_conversation("Konfirmasi kepada pengguna bahwa Anda akan membuka situs YouTube."))
    webbrowser.open("https://www.youtube.com")

def execute_task_creator():
    creator = jojo_profile.get('creator_name', 'seorang developer')
    speak(handle_conversation(f"Beritahu pengguna dengan bangga bahwa penciptamu adalah {creator}."))

def execute_task_wikipedia():
    speak("Tentu, apa yang ingin Anda cari di Wikipedia?")
    search_query = listen_command()
    if search_query not in ['none', 'batal', 'tidak jadi']:
        try:
            speak(f"Mencari {search_query}...")
            result = wikipedia.summary(search_query, sentences=2)
            speak(handle_conversation(f"Ringkas informasi ini untuk pengguna: {result}"))
        except Exception:
            speak(f"Maaf, saya tidak dapat menemukan hasil untuk {search_query}.")
    else:
        speak("Baik, dibatalkan.")

def execute_task_screenshot():
    try:
        speak("Baik, saya hitung mundur untuk mengambil screenshot.")
        time.sleep(1); speak("Tiga..."); time.sleep(1); speak("Dua..."); time.sleep(1); speak("Satu...")
        screenshot = pyautogui.screenshot()
        file_name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        screenshot.save(os.path.join(desktop_path, file_name))
        speak(f"Screenshot berhasil disimpan di Desktop Anda.")
    except Exception as e:
        speak(f"Maaf, gagal mengambil screenshot."); log_message("system", f"Error screenshot: {e}")

def execute_task_shutdown():
    speak("Apakah Anda benar-benar yakin ingin mematikan komputer?")
    confirmation = listen_command()
    if 'iya' in confirmation or 'yakin' in confirmation:
        speak("Baik, komputer akan dimatikan dalam 10 detik. Pastikan semua pekerjaan sudah tersimpan.")
        # os.system("shutdown /s /t 10") # Perintah Windows. Di-nonaktifkan agar tidak sengaja jalan.
        log_message("system", "Perintah shutdown akan dijalankan (saat ini dinonaktifkan).")
        return False
    else:
        speak("Perintah mematikan komputer dibatalkan.")
        return True

def execute_task_open_spotify():
    speak(handle_conversation("Konfirmasi kepada pengguna bahwa Anda akan membuka Spotify."))
    try:
        os.startfile("spotify:")
    except Exception:
        webbrowser.open("https://open.spotify.com")

def execute_task_open_instagram():
    speak(handle_conversation("Konfirmasi kepada pengguna bahwa Anda akan membuka Instagram."))
    webbrowser.open("https://www.instagram.com")

# --- Task Dispatcher ---
task_dispatcher = {
    "JAM": execute_task_get_time,
    "YOUTUBE": execute_task_open_youtube,
    "WIKIPEDIA": execute_task_wikipedia,
    "SCREENSHOT": execute_task_screenshot,
    "SHUTDOWN": execute_task_shutdown,
    "CREATOR": execute_task_creator,
    "SPOTIFY": execute_task_open_spotify,
    "INSTAGRAM": execute_task_open_instagram,
}