# 👁️ EYESPY // Covert Morse Exploitation Framework (Kali Linux Edition)

```
    ______ __  __ ______ _____ _____ __   __
   |  ____|\ \/ /|  ____/ ____|  __ \\ \ / /
   | |__    \  / | |__ | (___ | |__) |\ V / 
   |  __|    /   |  __| \___ \|  ___/  | |  
   | |____  / /\ \| |____ ____) | |      | |  
   |______||_/  \_\______|_____/|_|      |_|  

    [+] COVERT MORSE EXPLOITATION & COMMUNICATION FRAMEWORK
    [+] HIGH-PRECISION SENSOR: ANTI-FALSE TRIGGER & HYSTERESIS
   ╔══════════════════════════════════════════════════════════════╗
   ║ CODENAME : EYESPY-AGENT007      PLATFORM : KALI LINUX ROLLING║
   ║ ENGINE   : DUAL-HYSTERESIS PINCH AUDIO   : SYNTHETIC CARRIER ║
   ║ ACCURACY : ULTRA-HIGH STABILITY STATUS   : CLASSIFIED        ║
   ╚══════════════════════════════════════════════════════════════╝
```

Tools komunikasi sandi morse rahasia *real-time* berbasis penglihatan komputer (*computer vision*) dengan sistem **Anti-False Trigger & Dual-Hysteresis**.

---

### 🛡️ Fitur Anti-False Trigger (Baru Ditambahkan!)

1. **Hand Entrance Guard (0.35s Open Hand Stabilization)**:
   - Saat tangan baru pertama kali muncul di depan kamera, sistem **TIDAK AKAN** langsung mendeteksi ketukan.
   - Sistem mewajibkan tangan terbuka stabil selama **0.35 detik** di depan kamera hingga status berubah menjadi `[ ARMED // READY ]`.
   - Ini 100% mencegah ketukan palsu saat Anda baru mengangkat tangan!

2. **Dual-Threshold Hysteresis (Anti-Jitter)**:
   - **Touch Threshold (`0.15`)**: Jari harus benar-benar menyatu dan menekan rapat untuk memulai sinyal ketukan.
   - **Release Threshold (`0.26`)**: Jari harus benar-benar membuka lebar kembali untuk mengakhiri sinyal ketukan.
   - Mencegah sinyal berkedut (*flicker/jitter*) pada batas ambang.

3. **Kombinasi Jarak 2D + 3D**:
   - Memanfaatkan koordinat Z (*depth*) dari MediaPipe agar ketukan tidak salah terdeteksi jika tangan berada pada sudut miring (*perspective overlap*).

---

## 🎮 3 Mode Input Taktis (Tekan `M` untuk Berganti)

### 1. 🤏 Mode 1: HAND AIR-PINCH (Default / Rekomendasi Utama)
Sentuhkan ujung **Ibu Jari (Thumb)** dan **Jari Telunjuk (Index)**:
- **Ketukan Cepat (`0.08s - 0.35s`)** ➔ **Titik (Dot / `•`)** + Beep Pendek
- **Ketukan Ditahan (`0.35s - 1.20s`)** ➔ **Garis (Dash / `-`)** + Beep Panjang
- **Lepas Jari (`> 1.20s`)** ➔ Otomatis mengubah buffer menjadi Huruf
- **Lepas Jari (`> 3.00s`)** ➔ Otomatis menyisipkan Spasi kata

### 2. ✌️ Mode 2: HAND GESTURE (Pose Jari Tahan 0.22s)
- ☝️ **1 Jari (Telunjuk)** ditahan sekejap ➔ **Titik (`•`)**
- ✌️ **2 Jari (Peace sign)** ditahan sekejap ➔ **Garis (`-`)**
- ✊ **Kepalan Tangan** ➔ Posisi Netral untuk gesture berikutnya

### 3. 👁️ Mode 3: EYE BLINK
Mode kedipan mata dengan perlindungan dual-hysteresis.

---

## ⚡ Cara Menjalankan

```bash
# Langsung jalankan (Default Mode: Hand Air-Pinch)
eyespy

# Atau opsi pilihan mode:
eyespy --mode hand       # Mode Air-Pinch Presisi (Default)
eyespy --mode gesture    # Mode Simbol Jari
eyespy --mode eye        # Mode Kedipan Mata
```

---

## ⌨️ Tombol Kendali Cepat (Hotkeys)

Saat jendela kamera HUD terbuka:

| Tombol | Fungsi |
|---|---|
| **`M`** | **Ganti Mode Taktis (HAND PINCH ↔ HAND GESTURE ↔ EYE BLINK)** |
| **`Q`** / **`ESC`** / **`Ctrl+C`** | Menghentikan program dan keluar secara bersih tanpa crash |
| **`C`** | Membersihkan (*Clear*) buffer dan pesan |
| **`BACKSPACE`** | Menghapus 1 simbol / karakter terakhir |
| **`SPACE`** | Menyisipkan spasi kata manual |
| **`+` / `-`** | Menyesuaikan sensitivitas ambang batas |
