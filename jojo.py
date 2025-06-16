# ==============================================================================
# FINAL MASTER SCRIPT - JOJO AI v3.0
# Creator: Ahmad Zaki, with AI Assistant
# ==============================================================================

# --- Import Semua Library yang Dibutuhkan ---
import cv2 # type: ignore
import mediapipe as mp # type: ignore
import pyautogui # type: ignore
import math
import numpy as np # type: ignore
import speech_recognition as sr # type: ignore
import datetime
import os
import webbrowser
import time
import requests # type: ignore
import wikipedia # type: ignore
from gtts import gTTS # type: ignore
from playsound import playsound # type: ignore
from dotenv import load_dotenv # type: ignore
import google.generativeai as genai # type: ignore
import threading
from colorama import Fore, Style, init # type: ignore
import pyfiglet # type: ignore

# Muat variabel dari file .env
load_dotenv()

# ==============================================================================
# --- FUNGSI BANNER, LOGGING, SUARA, DAN FUNGSI DASAR LAINNYA ---
# ==============================================================================

def display_welcome_banner():
    """Menampilkan banner startup yang keren."""
    init(autoreset=True) # Wajib ada untuk colorama di Windows
    font = pyfiglet.Figlet(font='slant')
    welcome_text = font.renderText('JOJO AI')
    
    print(Fore.CYAN + Style.BRIGHT + welcome_text)
    print(Style.BRIGHT + Fore.YELLOW + "=====================================================")
    print(Style.BRIGHT + Fore.YELLOW + "          Created by: Ahmad Zaki          ")
    print(Style.BRIGHT + Fore.YELLOW + "=====================================================\n")

def log_message(actor, message):
    """Mencetak pesan dengan format log yang konsisten."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{actor.upper()}] >> {message}")

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
        log_message("system", f"Gagal menghasilkan suara: {e}")

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
    except Exception:
        log_message("system", "Gagal mengenali suara.")
        return "none"
    
def wish_me():
    """Memberi salam pembuka."""
    hour = int(datetime.datetime.now().hour)
    greeting = "Selamat Pagi!" if 4 <= hour < 12 else "Selamat Siang!" if 12 <= hour < 18 else "Selamat Malam!"
    speak(f"{greeting} Saya Jojo, asisten pribadimu. Saya siap mendengarkan perintah Anda.")

wikipedia.set_lang("id")

# ==============================================================================
# --- OTAK AI (FUNGSI-FUNGSI GEMINI) ---
# ==============================================================================
def get_command_intent(command):
    """Menganalisis perintah dan menentukan intensi (TUGAS atau PERCAKAPAN)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "GANTI_DENGAN" in api_key: return "ERROR:NO_API_KEY"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Anda adalah AI manajer yang cerdas. Klasifikasikan perintah pengguna ke 'TUGAS' atau 'PERCAKAPAN'.
    Format: "KATEGORI:NAMA_TUGAS" atau "PERCAKAPAN".
    Daftar Tugas: JAM, YOUTUBE, WIKIPEDIA, SCREENSHOT, SHUTDOWN, CREATOR, MODE_GESTUR, EXIT.
    Contoh: "siapa pembuatmu?" -> "TUGAS:CREATOR". "apa kabar?" -> "PERCAKAPAN".
    PERINTAH PENGGUNA: "{command}"
    KLASIFIKASI ANDA:"""
    try:
        response = model.generate_content(prompt)
        intent = response.text.strip().upper()
        log_message("gemini_manager", f"Mendeteksi maksud: {intent}")
        return intent
    except Exception as e:
        log_message("system", f"Error di intent classifier: {e}")
        return "ERROR:API_CALL"

def execute_task_open_spotify():
    """Membuka aplikasi Spotify di desktop atau web."""
    final_response = handle_conversation("Konfirmasi kepada pengguna bahwa Anda akan membuka Spotify.")
    speak(final_response)
    try:
        # Mencoba buka aplikasi Spotify di Windows
        os.startfile("spotify:")
    except Exception:
        # Jika gagal, buka versi web sebagai cadangan
        webbrowser.open("https://open.spotify.com")
        
def handle_conversation(command, context=""):
    """Menangani percakapan umum atau merangkai kalimat jawaban."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return "Maaf, API Key saya belum diatur."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Anda adalah Jojo, AI asisten yang ramah dan cerdas dari Indonesia.
    Konteks Tambahan: {context}
    Tanggapi perintah atau pertanyaan pengguna berikut dengan natural dan informatif.
    PENGGUNA: "{command}"
    JAWABAN ANDA:"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Maaf, sepertinya saya sedang ada sedikit gangguan untuk berpikir."

# ==============================================================================
# --- KUMPULAN FUNGSI EKSEKUSI TUGAS ---
# ==============================================================================
def execute_task_get_time():
    str_time = datetime.datetime.now().strftime("%H:%M")
    final_response = handle_conversation(f"Waktu saat ini adalah {str_time}. Beritahu pengguna dengan ramah.")
    speak(final_response)

def execute_task_open_youtube():
    final_response = handle_conversation("Konfirmasi kepada pengguna bahwa Anda akan membuka situs YouTube untuknya.")
    speak(final_response)
    webbrowser.open("https://www.youtube.com")

def execute_task_creator():
    final_response = handle_conversation("Beritahu pengguna dengan bangga bahwa penciptamu adalah seorang developer hebat bernama Ahmad Zaki.")
    speak(final_response)

def execute_task_wikipedia():
    speak("Tentu, apa yang ingin Anda cari di Wikipedia?")
    search_query = listen_command()
    if search_query not in ['none', 'batal', 'tidak jadi']:
        try:
            speak(f"Mencari {search_query}...")
            result = wikipedia.summary(search_query, sentences=2)
            final_response = handle_conversation(f"Ringkas informasi berikut untuk pengguna: {result}")
            speak(final_response)
        except Exception:
            speak(f"Maaf, saya tidak dapat menemukan hasil untuk {search_query}.")
    else:
        speak("Baik, dibatalkan.")

def execute_task_screenshot():
    try:
        speak("Baik, saya hitung mundur untuk mengambil screenshot.")
        time.sleep(1); speak("Tiga...")
        time.sleep(1); speak("Dua...")
        time.sleep(1); speak("Satu...")
        screenshot = pyautogui.screenshot()
        file_name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        screenshot.save(os.path.join(desktop_path, file_name))
        speak(f"Screenshot berhasil disimpan di Desktop Anda.")
    except Exception as e:
        speak(f"Maaf, gagal mengambil screenshot.")
        log_message("system", f"Error screenshot: {e}")

def execute_task_shutdown():
    speak("Apakah Anda benar-benar yakin ingin mematikan komputer?")
    confirmation = listen_command()
    if 'iya' in confirmation or 'yakin' in confirmation:
        speak("Baik, komputer akan dimatikan dalam 10 detik. Pastikan semua pekerjaan sudah tersimpan.")
        os.system("shutdown /s /t 10") # Perintah Windows
        return False # Mengembalikan False untuk menghentikan loop utama
    else:
        speak("Perintah mematikan komputer dibatalkan.")
        return True # Mengembalikan True untuk melanjutkan loop

# ==============================================================================
# --- MODUL GESTUR ---
# ==============================================================================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()
def count_fingers(hand_landmarks):
    if not hand_landmarks: return 0
    landmarks = hand_landmarks.landmark
    finger_count = 0
    tip_ids = [4, 8, 12, 16, 20]
    # Logika untuk ibu jari (tangan kanan)
    if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 2].x:
        finger_count += 1
    # Logika untuk 4 jari lainnya
    for tip_id in tip_ids[1:]:
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            finger_count += 1
    return finger_count

# ==============================================================================
# --- PROGRAM UTAMA ---
# ==============================================================================
if __name__ == "__main__":
    display_welcome_banner()

    mode = 'suara'
    program_is_running = True
    wish_me()
    cap = None
    smooth_factor = 7; prev_x, prev_y = 0, 0

    task_dispatcher = {
        "JAM": execute_task_get_time,
        "YOUTUBE": execute_task_open_youtube,
        "WIKIPEDIA": execute_task_wikipedia,
        "SCREENSHOT": execute_task_screenshot,
        "SHUTDOWN": execute_task_shutdown,
        "CREATOR": execute_task_creator,
    }

    try:
        while program_is_running:
            if mode == 'suara':
                if cap and cap.isOpened(): cap.release(); log_message("system", "Kamera dinonaktifkan.")
                
                command = listen_command()
                if command == 'none': continue

                intent = get_command_intent(command)

                if intent.startswith("TUGAS:"):
                    action = intent.split(":")[1]
                    
                    if action in task_dispatcher:
                        if action == "SHUTDOWN":
                            program_is_running = task_dispatcher[action]()
                        else:
                            task_dispatcher[action]()
                    
                    elif action == "MODE_GESTUR":
                        response_prompt = "Konfirmasi bahwa mode kontrol jari diaktifkan dan jelaskan cara keluar dengan menunjukkan 5 jari."
                        speak(handle_conversation(response_prompt))
                        mode = 'gestur'
                        cap = cv2.VideoCapture(0)
                        log_message("system", "Kamera diaktifkan.")
                    
                    elif action == "EXIT":
                        speak(handle_conversation("Ucapkan selamat tinggal yang ramah."))
                        program_is_running = False

                elif intent == "PERCAKAPAN":
                    time_context = f"Sebagai info, waktu saat ini adalah {datetime.datetime.now().strftime('%H:%M')}."
                    response_text = handle_conversation(command, context=time_context)
                    speak(response_text)

                elif intent == "ERROR:NO_API_KEY":
                    speak("API Key Gemini sepertinya belum diatur. Mohon periksa file .env Anda.")
                else:
                    speak("Maaf, saya tidak begitu mengerti maksud Anda.")

            elif mode == 'gestur':
                if not cap or not cap.isOpened(): cap = cv2.VideoCapture(0)
                success, frame = cap.read()
                if not success: continue
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    num_fingers = count_fingers(hand_landmarks)
                    if num_fingers == 5:
                        speak(handle_conversation("Konfirmasi bahwa mode gestur telah dinonaktifkan."))
                        mode = 'suara'
                        continue
                    
                    # Logika Gerakan Mouse
                    index_finger_tip = hand_landmarks.landmark[8]
                    thumb_tip = hand_landmarks.landmark[4]
                    frame_height, frame_width, _ = frame.shape
                    target_x = np.interp(index_finger_tip.x, (0.1, 0.9), (0, screen_width))
                    target_y = np.interp(index_finger_tip.y, (0.1, 0.9), (0, screen_height))
                    curr_x = prev_x + (target_x - prev_x) / smooth_factor
                    curr_y = prev_y + (target_y - prev_y) / smooth_factor
                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y

                    # Logika Klik Kiri
                    click_distance = math.hypot(thumb_tip.x - index_finger_tip.x, thumb_tip.y - index_finger_tip.y)
                    if click_distance < 0.04: pyautogui.click(); time.sleep(0.2)
                
                time.sleep(0.01)
    
    except KeyboardInterrupt:
        log_message("system", "Program dihentikan paksa.")
    finally:
        if cap and cap.isOpened(): cap.release()
        log_message("system", "Program Selesai.")