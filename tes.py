# File: tes_koneksi_gemini.py (Versi Diagnostik)

import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

print("[LANGKAH 1] Skrip diagnostik dimulai.")
time.sleep(1)

try:
    print("\n[LANGKAH 2] Mencoba memuat file .env...")
    # Memastikan file .env terbaca
    if load_dotenv():
        print("   [OK] File .env ditemukan dan dimuat.")
    else:
        print("   [PERINGATAN] File .env tidak ditemukan. Pastikan file ada di folder yang sama.")

    time.sleep(1)

    print("\n[LANGKAH 3] Mencoba membaca API Key dari environment...")
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or "GANTI_DENGAN" in api_key:
        print("   [GAGAL] Variabel GEMINI_API_KEY tidak ditemukan atau belum diisi di dalam .env.")
        print("   --- Tes Berhenti ---")
    else:
        print(f"   [OK] API Key ditemukan (beberapa karakter awal: {api_key[:4]}...).")
        time.sleep(1)

        print("\n[LANGKAH 4] Mencoba mengonfigurasi library Gemini dengan API Key...")
        genai.configure(api_key=api_key)
        print("   [OK] Konfigurasi genai.configure() berhasil.")
        time.sleep(1)

        print("\n[LANGKAH 5] Mencoba membuat model 'gemini-1.5-flash'...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("   [OK] Model berhasil dibuat.")
        time.sleep(1)

        print("\n[LANGKAH 6] INI BAGIAN PENTING: Mengirim permintaan ke server Google...")
        print("   Program mungkin akan diam (menggantung) di sini jika ada masalah jaringan atau firewall.")
        print("   Mohon tunggu beberapa saat...")
        
        # Ini adalah baris yang melakukan koneksi ke internet
        response = model.generate_content("Halo, ini tes. Jawab 'OK'.")
        
        print("   [OK] Berhasil menerima respons dari server Google!")
        time.sleep(1)

        print("\n--- HASIL AKHIR: SUKSES ---")
        print(f"Jawaban Gemini: {response.text.strip()}")

except Exception as e:
    print("\n!!! TERJADI ERROR YANG TERTANGKAP !!!")
    print(f"Detail Error Teknis: {e}")

finally:
    print("\n[LANGKAH 7] Skrip selesai.")
    input("Tekan Enter untuk keluar...") # Agar jendela tidak langsung tertutup