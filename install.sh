#!/usr/bin/env bash
# =============================================================================
#    ______ __  __ ______ _____ _____ __   __
#   |  ____|\ \/ /|  ____/ ____|  __ \\ \ / /
#   | |__    \  / | |__ | (___ | |__) |\ V / 
#   |  __|    /   |  __| \___ \|  ___/  | |  
#   | |____  / /\ \| |____ ____) | |      | |  
#   |______||_/  \_\______|_____/|_|      |_|  
#
#   EYESPY // KALI LINUX INSTALLER & ENVIRONMENT SETUP
# =============================================================================

set -e

RED="\033[1;31m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
WHITE="\033[1;37m"
DIM="\033[0;90m"
RESET="\033[0m"

echo -e "${GREEN}"
cat << "EOF"
    ______ __  __ ______ _____ _____ __   __
   |  ____|\ \/ /|  ____/ ____|  __ \\ \ / /
   | |__    \  / | |__ | (___ | |__) |\ V / 
   |  __|    /   |  __| \___ \|  ___/  | |  
   | |____  / /\ \| |____ ____) | |      | |  
   |______||_/  \_\______|_____/|_|      |_|  
EOF
echo -e "${CYAN}[+] EYESPY: COVERT OCULAR MORSE EXPLOITATION FRAMEWORK${RESET}"
echo -e "${YELLOW}[+] KALI LINUX ONE-CLICK INSTALLER${RESET}"
echo -e "${DIM}────────────────────────────────────────────────────────────${RESET}"

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Cek Python3 & pip
echo -e "${CYAN}[*] Memeriksa interpreter Python dan paket...${RESET}"
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[-] Python 3 tidak ditemukan! Silakan install python3 terlebih dahulu.${RESET}"
    exit 1
fi
echo -e "${GREEN}[+] Python 3 terdeteksi: $(python3 --version)${RESET}"

# 2. Install dependensi pip
echo -e "${CYAN}[*] Memasang dependensi (OpenCV, MediaPipe, Pygame, NumPy)...${RESET}"
if [ -f "$DIR/requirements.txt" ]; then
    pip3 install -r "$DIR/requirements.txt" --break-system-packages 2>/dev/null || \
    pip3 install -r "$DIR/requirements.txt" 2>/dev/null || \
    pip install -r "$DIR/requirements.txt" || true
fi

# 3. Buat wrapper script executable
chmod +x "$DIR/eyespy"
chmod +x "$DIR/eyespy.py"

# 4. Tentukan target instalasi global
TARGET_BIN="/usr/local/bin/eyespy"
USER_BIN="$HOME/.local/bin/eyespy"

INSTALLED=false

# Jika memiliki hak sudo / root, pasang ke /usr/local/bin
if [ "$EUID" -eq 0 ]; then
    echo -e "${CYAN}[*] Hak akses ROOT terdeteksi. Memasang ke /usr/local/bin/eyespy...${RESET}"
    ln -sf "$DIR/eyespy" "$TARGET_BIN"
    chmod +x "$TARGET_BIN"
    INSTALLED=true
    INSTALLED_PATH="$TARGET_BIN"
else
    # Jika user biasa, coba pasang ke ~/.local/bin
    mkdir -p "$HOME/.local/bin" 2>/dev/null || true
    if [ -d "$HOME/.local/bin" ]; then
        ln -sf "$DIR/eyespy" "$USER_BIN" 2>/dev/null || cp "$DIR/eyespy" "$USER_BIN" 2>/dev/null || true
        if [ -f "$USER_BIN" ]; then
            chmod +x "$USER_BIN"
            INSTALLED=true
            INSTALLED_PATH="$USER_BIN"
        fi
    fi
fi

echo -e "${DIM}────────────────────────────────────────────────────────────${RESET}"
if [ "$INSTALLED" = true ]; then
    echo -e "${GREEN}[✔] INSTALASI BERHASIL!${RESET}"
    echo -e "${WHITE}Sekarang Anda dapat menjalankan tool ini dari direktori MANA SAJA dengan mengetik:${RESET}"
    echo -e "    ${YELLOW}eyespy${RESET}"
else
    echo -e "${YELLOW}[!] Instalasi global memerlukan sudo. Namun Anda dapat langsung menjalankannya dengan:${RESET}"
    echo -e "    ${GREEN}sudo bash install.sh${RESET}  (untuk akses global dari mana saja)"
    echo -e "    ${CYAN}atau di direktori ini:${RESET}"
    echo -e "    ${WHITE}./eyespy${RESET}  atau  ${WHITE}python eyespy${RESET}"
fi

echo -e "${DIM}────────────────────────────────────────────────────────────${RESET}"
echo -e "${CYAN}[*] Menjalankan uji mandiri (Self-Test)...${RESET}"
python3 "$DIR/eyespy" --test
echo -e "\n${GREEN}[+] Siap beraksi! Ketik 'eyespy' atau './eyespy' untuk memulai.${RESET}\n"
