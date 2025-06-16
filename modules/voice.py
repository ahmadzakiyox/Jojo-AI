# File: modules/voice.py
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import datetime
from .utils import log_message

def speak(audio):
    """Fungsi untuk berbicara menggunakan gTTS (suara Google)."""
    log_message("jojo", audio)
    try:
        tts = gTTS(text=audio, lang='id', slow=False)
        sound_file = "response.mp3"
        tts.save(sound_file)
        playsound(sound_file)
        os.remove(sound_file)
    except Exception as e:
        log_message("system", f"Gagal menghasilkan suara (gTTS/playsound): {e}")

def listen_command():
    """Mendengarkan perintah dan mengubahnya menjadi teks."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        log_message("system", "Kalibrasi kebisingan...")
        r.adjust_for_ambient_noise(source, duration=1)
        log_message("system", "Mendengarkan...")
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        log_message("system", "Mengenali...")
        query = r.recognize_google(audio, language='id-ID')
        log_message("user", query)
        return query.lower()
    except Exception as e:
        log_message("system", f"Gagal mengenali suara. Detail: {e}")
        return "none"
    
def wish_me():
    """Memberi salam pembuka."""
    hour = int(datetime.datetime.now().hour)
    greeting = "Selamat Pagi!" if 4 <= hour < 12 else "Selamat Siang!" if 12 <= hour < 18 else "Selamat Malam!"
    speak(f"{greeting} Saya Jojo, asisten pribadimu. Saya siap mendengarkan perintah Anda.")