# File: main.py
# Ini adalah file utama untuk menjalankan Jojo AI.

import time
import cv2
import os
import datetime

# Impor fungsi-fungsi spesifik dari modul-modul kita
from modules.utils import log_message, display_welcome_banner
from modules.voice import speak, listen_command, wish_me
from modules.ai_brain import get_command_intent, handle_conversation
from modules.tasks import task_dispatcher
from modules.gesture_control import run_gesture_mode

def main():
    """Fungsi utama yang menjalankan seluruh alur program."""
    mode = 'suara'
    program_is_running = True
    cap = None
    
    wish_me()

    try:
        while program_is_running:
            if mode == 'suara':
                # Pastikan kamera mati jika kita kembali ke mode suara
                if cap and cap.isOpened():
                    cap.release()
                    cv2.destroyAllWindows()
                    log_message("system", "Kamera dinonaktifkan.")
                
                command = listen_command()
                if command == 'none':
                    continue

                intent = get_command_intent(command)

                if intent.startswith("TUGAS:"):
                    action = intent.split(":")[1]
                    
                    if action in task_dispatcher:
                        # Untuk shutdown, kita cek return value-nya
                        if action == "SHUTDOWN":
                            program_is_running = task_dispatcher[action]()
                        else:
                            task_dispatcher[action]()
                    
                    elif action == "MODE_GESTUR":
                        response_prompt = "Konfirmasi bahwa mode kontrol jari diaktifkan dan jelaskan cara keluar dengan menunjukkan 5 jari."
                        speak(handle_conversation(response_prompt))
                        mode = 'gestur'
                        cap = cv2.VideoCapture(0)
                        log_message("system", "Kamera diaktifkan untuk mode gestur.")
                    
                    elif action == "EXIT":
                        speak(handle_conversation("Ucapkan selamat tinggal yang ramah."))
                        program_is_running = False

                elif intent == "PERCAKAPAN":
                    # Menambahkan konteks waktu pada percakapan umum
                    time_context = f"Sebagai info, waktu saat ini adalah {datetime.datetime.now().strftime('%H:%M')}."
                    response_text = handle_conversation(command, context=time_context)
                    speak(response_text)
                
                elif intent == "ERROR:NO_API_KEY":
                    speak("API Key Gemini sepertinya belum diatur. Mohon periksa file .env Anda.")
                else: # Fallback untuk TIDAK_MENGERTI atau ERROR:API_CALL
                    speak("Maaf, saya tidak begitu mengerti maksud Anda.")

            elif mode == 'gestur':
                # Panggil fungsi mode gestur dan tunggu hasilnya (apakah mode harus diubah)
                mode = run_gesture_mode(cap)
    
    except KeyboardInterrupt:
        log_message("system", "Program dihentikan paksa.")
    finally:
        if cap and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        log_message("system", "Program Selesai.")

if __name__ == "__main__":
    # Tampilkan banner dan jalankan program utama
    display_welcome_banner()
    main()