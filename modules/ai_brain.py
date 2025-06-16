# File: modules/ai_brain.py
import os
import google.generativeai as genai
from .utils import log_message, jojo_profile

# Konfigurasi awal saat modul diimpor
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_command_intent(command):
    """Menganalisis perintah dan menentukan intensi."""
    if not api_key or "GANTI_DENGAN" in api_key: return "ERROR:NO_API_KEY"
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Anda adalah AI manajer yang cerdas. Klasifikasikan perintah pengguna ke 'TUGAS' (jika ada dalam daftar) atau 'PERCAKAPAN'.
    Format: "KATEGORI:NAMA_TUGAS" atau "PERCAKAPAN".
    Daftar Tugas: JAM, YOUTUBE, WIKIPEDIA, SCREENSHOT, SHUTDOWN, CREATOR, SPOTIFY, INSTAGRAM, MODE_GESTUR, EXIT.
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

def handle_conversation(command, context=""):
    """Menangani percakapan umum atau merangkai kalimat jawaban."""
    if not api_key: return "Maaf, API Key saya belum diatur."

    model = genai.GenerativeModel('gemini-1.5-flash')
    personality = ", ".join(jojo_profile.get("personality_traits", ["ramah"]))
    ai_name = jojo_profile.get('ai_name', 'Jojo')

    prompt = f"""
    Anda adalah {ai_name}, sebuah AI asisten yang {personality} dari Indonesia.
    Konteks Tambahan: {context}
    Tanggapi perintah atau pertanyaan pengguna berikut dengan natural dan informatif.
    PENGGUNA: "{command}"
    JAWABAN ANDA:"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        log_message("system", f"Error di handle_conversation: {e}")
        return "Maaf, sepertinya saya sedang ada sedikit gangguan untuk berpikir."