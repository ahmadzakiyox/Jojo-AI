# <p align="center">🤖 Jojo AI: Asisten Pribadi Cerdas Anda 🤖</p>

<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="GPLv3 License"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white" alt="Python 3.9+"></a>
  <a href="https://github.com/ahmadzakiyox/Jojo-AI/releases"><img src="https://img.shields.io/badge/Release-v1.0-brightgreen.svg" alt="Release v1.0"></a>
  <a href="https://github.com/ahmadzakiyox/Jojo-AI/issues"><img src="https://img.shields.io/badge/Contributions-Welcome-orange.svg" alt="Contributions Welcome"></a>
</p>

<p align="center">
  Sebuah asisten virtual multifungsi berbasis Python yang dapat berinteraksi melalui suara dan gestur tangan, ditenagai oleh kecerdasan buatan dari Google Gemini.
</p>

---
### 🎬 Video Demo

<p align="center">
  <a href="https://github.com/ahmadzakiyox/DB/blob/main/vd.mp4" target="_blank">
    <img src="https://raw.githubusercontent.com/ahmadzakiyox/DB/main/Screenshot%202025-06-16%20091312.png" alt="Demo Jojo AI" width="720">
  </a>
  <br>
  <em>(Klik gambar di atas untuk melihat video demo lengkap)</em>
</p>
---
---

## ✨ Fitur Utama

Jojo AI dirancang untuk menjadi lebih dari sekadar program, melainkan partner digital Anda.

* **🧠 Otak AI dengan Google Gemini:** Mampu memahami perintah dalam bahasa Indonesia natural dan melakukan percakapan terbuka, tidak terbatas pada perintah kaku.
* **🗣️ Interaksi Suara Alami:** Menggunakan suara "Mbah Google" (`gTTS`) untuk respons yang familiar dan sistem pengenalan suara yang canggih.
* **🖐️ Mode Kontrol Gestur:** Ambil alih kontrol mouse laptop Anda hanya dengan gerakan jari telunjuk dan ibu jari melalui webcam.
* **📂 Organisasi Modular:** Kode terstruktur rapi dalam modul-modul (`main.py`, `modules/`) yang mudah dipahami dan dikembangkan.
* **⚙️ Konfigurasi Mudah:** Sesuaikan nama, kepribadian, dan pengaturan lainnya melalui file `jojo_profile.json`.
* **✅ Fungsionalitas Lengkap:**
    * Menjawab waktu saat ini.
    * Membuka situs web (YouTube, Spotify, Instagram).
    * Mencari informasi ringkas dari Wikipedia.
    * Mengambil tangkapan layar (screenshot).
    * Mematikan komputer (dengan konfirmasi suara).
    * Mengenali penciptanya, **Ahmad Zaki**.
    * Dan kemampuan percakapan lainnya!

## 🛠️ Teknologi yang Digunakan

* **Bahasa:** Python 3.9+
* **AI & Machine Learning:** Google Gemini, MediaPipe
* **Interaksi Suara:** SpeechRecognition, gTTS, PyAudio, playsound
* **Kontrol & Otomatisasi:** PyAutoGUI, OpenCV
* **Tampilan & Lainnya:** PyFiglet, Colorama, python-dotenv

## ⚙️ Panduan Instalasi

Untuk menjalankan Jojo AI di komputer Anda, ikuti langkah-langkah berikut:

1.  **Clone Repositori:**
    ```bash
    git clone [https://github.com/](https://github.com/)[NamaPenggunaAnda]/[NamaRepoAnda].git
    cd [NamaRepoAnda]
    ```

2.  **Buat Virtual Environment (Direkomendasikan):**
    ```bash
    python -m venv venv
    # Di Windows:
    .\venv\Scripts\activate
    # Di macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    *(**Catatan:** Untuk `PyAudio` di Windows, mungkin perlu instalasi manual. Lihat dokumentasi atau diskusi sebelumnya jika terjadi error).*

4.  **Konfigurasi API Key:**
    * Buat file `.env` di folder utama.
    * Salin isi dari `.env.example` (jika Anda membuatnya) atau langsung tulis:
        ```env
        GEMINI_API_KEY="API_KEY_ANDA_DI_SINI"
        ```
    * Ganti dengan API Key Google Gemini Anda yang asli.

5.  **Jalankan Jojo AI:**
    ```bash
    python main.py
    ```

## 🚀 Cara Penggunaan

Setelah program berjalan dan banner muncul, Jojo akan menyapa Anda. Mulailah berbicara setelah Anda melihat log `[SYSTEM] >> Mendengarkan...`.

Beberapa contoh perintah:
* *"Halo Jojo"*
* *"Jam berapa sekarang?"*
* *"Siapa yang membuatmu?"*
* *"Ambil alih kendali"* (untuk masuk ke mode gestur)
* *"Keluar"* (untuk menghentikan program)

## 📄 Lisensi

Proyek ini dilisensikan di bawah **GNU General Public License v3.0**. Lisensi ini memastikan bahwa Jojo AI dan semua turunannya akan selalu tetap menjadi perangkat lunak bebas dan terbuka. Lihat file [LICENSE](LICENSE) untuk detail lengkapnya.
