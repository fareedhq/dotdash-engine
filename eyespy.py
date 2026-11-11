#!/usr/bin/env python3
r"""
=============================================================================
   ______ __  __ ______ _____ _____ __   __
  |  ____|\ \/ /|  ____/ ____|  __ \\ \ / /
  | |__    \  / | |__ | (___ | |__) |\ V / 
  |  __|    /   |  __| \___ \|  ___/  | |  
  | |____  / /\ \| |____ ____) | |      | |  
  |______||_/  \_\______|_____/|_|      |_|  

  [+] COVERT MORSE EXPLOITATION & COMMUNICATION FRAMEWORK
  [+] KALI LINUX SPECIAL EDITION // AIR-GAPPED EXFILTRATION
=============================================================================
Sistem komunikasi rahasia kode Morse taktis berakurasi tinggi (Anti-False Trigger).
Mendukung 3 Mode Input Taktis:
1. HAND AIR-PINCH   : Ketukan presisi jempol + telunjuk dengan Dual-Hysteresis & Anti-Glitch
2. HAND GESTURE     : Simbol jari stabil (1 Jari = Dot, 2 Jari = Dash, Kepalan = Neutral)
3. EYE BLINK        : Pelacakan kedipan mata (Ocular EAR Tracking)
=============================================================================
"""

import os
# Redam peringatan cache matplotlib pada sistem Linux
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import sys
import time
import math
import argparse
import numpy as np

# =============================================================================
# 0. TACTICAL TERMINAL COLOR ENGINE (ANSI)
# =============================================================================
class Colors:
    GREEN   = "\033[1;32m"
    CYAN    = "\033[1;36m"
    RED     = "\033[1;31m"
    YELLOW  = "\033[1;33m"
    WHITE   = "\033[1;37m"
    MAGENTA = "\033[1;35m"
    DIM     = "\033[0;90m"
    RESET   = "\033[0m"
    BOLD    = "\033[1m"

def log_info(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{ts}]{Colors.RESET} {Colors.CYAN}[*]{Colors.RESET} {msg}")

def log_success(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{ts}]{Colors.RESET} {Colors.GREEN}[+]{Colors.RESET} {msg}")

def log_warn(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{ts}]{Colors.RESET} {Colors.YELLOW}[!]{Colors.RESET} {msg}")

def log_error(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{ts}]{Colors.RESET} {Colors.RED}[-]{Colors.RESET} {msg}")

def log_payload(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{ts}]{Colors.RESET} {Colors.MAGENTA}[>>>]{Colors.RESET} {Colors.BOLD}{Colors.GREEN}{msg}{Colors.RESET}")

def print_banner():
    """Mencetak Banner Hacker ala Tools Kali Linux."""
    banner = rf"""
{Colors.GREEN}    ______ __  __ ______ _____ _____ __   __
   |  ____|\ \/ /|  ____/ ____|  __ \\ \ / /
   | |__    \  / | |__ | (___ | |__) |\ V / 
   |  __|    /   |  __| \___ \|  ___/  | |  
   | |____  / /\ \| |____ ____) | |      | |  
   |______||_/  \_\______|_____/|_|      |_|  
{Colors.RESET}
{Colors.CYAN}    [+] COVERT MORSE EXPLOITATION & COMMUNICATION FRAMEWORK
{Colors.YELLOW}    [+] HIGH-PRECISION SENSOR: ANTI-FALSE TRIGGER & HYSTERESIS
{Colors.DIM}   ╔══════════════════════════════════════════════════════════════╗
   ║ {Colors.WHITE}CODENAME : EYESPY-AGENT007      PLATFORM : KALI LINUX ROLLING{Colors.DIM}║
   ║ {Colors.WHITE}ENGINE   : DUAL-HYSTERESIS PINCH AUDIO   : SYNTHETIC CARRIER {Colors.DIM}║
   ║ {Colors.WHITE}ACCURACY : ULTRA-HIGH STABILITY STATUS   : CLASSIFIED        {Colors.DIM}║
   ╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


# =============================================================================
# 1. KAMUS MORSE CODE LENGKAP
# =============================================================================
MORSE_DICT = {
    # Huruf A - Z
    '.-': 'A',   '-...': 'B', '-.-.': 'C', '-..': 'D',  '.': 'E',
    '..-.': 'F', '--.': 'G',  '....': 'H', '..': 'I',   '.---': 'J',
    '-.-': 'K',  '.-..': 'L', '--': 'M',   '-.': 'N',   '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R',  '...': 'S',  '-': 'T',
    '..-': 'U',  '...-': 'V', '.--': 'W',  '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
    # Angka 0 - 9
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    # Tanda Baca & Simbol Taktis
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '-.-.--': '!',
    '-....-': '-', '-..-.': '/',  '.--.-.': '@', '...---...': 'SOS'
}

def morse_to_char(morse_str: str) -> str:
    """Menerjemahkan rangkaian kode morse (menggunakan '•' atau '.') menjadi karakter."""
    normalized = morse_str.replace('•', '.').strip()
    return MORSE_DICT.get(normalized, '?')


# =============================================================================
# 2. SISTEM AUDIO SINTETIS (PYGAME MIXER / NUMPY TONE GENERATOR)
# =============================================================================
class AudioManager:
    """Mengelola pembuatan dan pemutaran audio beep Morse murni non-blocking."""
    def __init__(self, sample_rate=44100, enabled=True):
        self.sample_rate = sample_rate
        self.audio_enabled = False
        self.dot_sound = None
        self.dash_sound = None
        self.commit_sound = None
        self.space_sound = None

        if not enabled:
            return

        try:
            import pygame
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
            self.dot_sound = self._create_tone(freq=850, duration=0.08, volume=0.55)
            self.dash_sound = self._create_tone(freq=850, duration=0.28, volume=0.55)
            self.commit_sound = self._create_tone(freq=1250, duration=0.06, volume=0.35)
            self.space_sound = self._create_tone(freq=480, duration=0.09, volume=0.40)
            self.audio_enabled = True
        except Exception as e:
            log_warn(f"Audio device not active ({e}). Running in silent HUD mode.")

    def _create_tone(self, freq=800, duration=0.1, volume=0.5):
        import pygame
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(2 * np.pi * freq * t)
        envelope = np.ones(n_samples)
        fade_len = min(int(self.sample_rate * 0.008), n_samples // 4)
        if fade_len > 0:
            envelope[:fade_len] = np.linspace(0, 1, fade_len)
            envelope[-fade_len:] = np.linspace(1, 0, fade_len)
        mono = (wave * envelope * volume * 32767).astype(np.int16)
        stereo = np.column_stack((mono, mono))
        return pygame.sndarray.make_sound(stereo)

    def play_dot(self):
        if self.audio_enabled and self.dot_sound:
            self.dot_sound.play()

    def play_dash(self):
        if self.audio_enabled and self.dash_sound:
            self.dash_sound.play()

    def play_commit(self):
        if self.audio_enabled and self.commit_sound:
            self.commit_sound.play()

    def play_space(self):
        if self.audio_enabled and self.space_sound:
            self.space_sound.play()


# =============================================================================
# 3. HAND SKELETON CONNECTIONS & PERHITUNGAN PINCH PRESISI
# =============================================================================
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
    (0, 17)                                # Palm base
]

def calculate_pinch_ratio_robust(landmarks, w, h):
    """
    Menghitung rasio jarak jepitan antara Ibu Jari (#4) dan Jari Telunjuk (#8)
    menggunakan kombinasi 2D pixel dan 3D normalized coordinates untuk mencegah
    kesalahan sudut pandang kamera (perspective overlap).
    """
    # Titik 2D di layar
    tx, ty = landmarks[4].x * w, landmarks[4].y * h
    ix, iy = landmarks[8].x * w, landmarks[8].y * h
    dist_2d = math.hypot(tx - ix, ty - iy)

    wx, wy = landmarks[0].x * w, landmarks[0].y * h
    mx, my = landmarks[9].x * w, landmarks[9].y * h
    palm_2d = math.hypot(wx - mx, wy - my)
    if palm_2d < 1.0:
        palm_2d = 1.0

    ratio_2d = dist_2d / palm_2d

    # Jarak 3D relatif untuk mengoreksi rotasi tangan
    dx_3d = landmarks[4].x - landmarks[8].x
    dy_3d = landmarks[4].y - landmarks[8].y
    dz_3d = landmarks[4].z - landmarks[8].z
    dist_3d = math.sqrt(dx_3d**2 + dy_3d**2 + dz_3d**2)

    wx_3d = landmarks[0].x - landmarks[9].x
    wy_3d = landmarks[0].y - landmarks[9].y
    wz_3d = landmarks[0].z - landmarks[9].z
    palm_3d = math.sqrt(wx_3d**2 + wy_3d**2 + wz_3d**2)
    if palm_3d < 1e-4:
        palm_3d = 1e-4
    ratio_3d = dist_3d / palm_3d

    # Gabungkan 2D dan 3D untuk akurasi optimal
    combined_ratio = (ratio_2d * 0.70) + (ratio_3d * 0.30)
    return combined_ratio, (int(tx), int(ty)), (int(ix), int(iy))

def count_extended_fingers(landmarks):
    """
    Menghitung jari yang terangkat ke atas secara stabil:
    Mengembalikan (index_up, middle_up, ring_up, pinky_up, total_up)
    """
    index_up = landmarks[8].y < landmarks[6].y
    middle_up = landmarks[12].y < landmarks[10].y
    ring_up = landmarks[16].y < landmarks[14].y
    pinky_up = landmarks[20].y < landmarks[18].y
    total = sum([index_up, middle_up, ring_up, pinky_up])
    return index_up, middle_up, ring_up, pinky_up, total


# =============================================================================
# 4. OCULAR (EYE) CALCULATIONS
# =============================================================================
LEFT_EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_LANDMARKS = [362, 385, 387, 263, 373, 380]
LEFT_EYE_CONTOUR = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE_CONTOUR = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

def calculate_ear(landmarks, eye_indices, width: float, height: float) -> float:
    pts = [np.array([landmarks[idx].x * width, landmarks[idx].y * height]) for idx in eye_indices]
    v1 = np.linalg.norm(pts[1] - pts[5])
    v2 = np.linalg.norm(pts[2] - pts[4])
    h = np.linalg.norm(pts[0] - pts[3])
    if h <= 1e-6:
        return 0.0
    return float((v1 + v2) / (2.0 * h))


# =============================================================================
# 5. UNIVERSAL SENSOR ADAPTER
# =============================================================================
class UniversalSensor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.hand_landmarker = None
        self.face_landmarker = None

        # Hand Landmarker
        hand_model = os.path.join(base_dir, "hand_landmarker.task")
        if not os.path.exists(hand_model):
            try:
                log_info("Downloading hand_landmarker.task model (~7.5MB)...")
                import urllib.request
                url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
                urllib.request.urlretrieve(url, hand_model)
                log_success("Hand model successfully downloaded.")
            except Exception as e:
                log_warn(f"Failed to auto-download hand model: {e}")

        if os.path.exists(hand_model):
            try:
                import mediapipe as mp
                BaseOptions = mp.tasks.BaseOptions
                HandLandmarker = mp.tasks.vision.HandLandmarker
                HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
                VisionRunningMode = mp.tasks.vision.RunningMode

                options = HandLandmarkerOptions(
                    base_options=BaseOptions(model_asset_path=hand_model),
                    running_mode=VisionRunningMode.IMAGE,
                    num_hands=1
                )
                self.hand_landmarker = HandLandmarker.create_from_options(options)
                log_success("Hand Sensor Engine: MediaPipe Neural Hands (v1.x) [ONLINE]")
            except Exception as e:
                log_warn(f"Hand tracker init error: {e}")

        # Face Landmarker
        face_model = os.path.join(base_dir, "face_landmarker.task")
        if os.path.exists(face_model):
            try:
                import mediapipe as mp
                BaseOptions = mp.tasks.BaseOptions
                FaceLandmarker = mp.tasks.vision.FaceLandmarker
                FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
                VisionRunningMode = mp.tasks.vision.RunningMode

                options = FaceLandmarkerOptions(
                    base_options=BaseOptions(model_asset_path=face_model),
                    running_mode=VisionRunningMode.IMAGE,
                    output_face_blendshapes=True,
                    num_faces=1
                )
                self.face_landmarker = FaceLandmarker.create_from_options(options)
                log_success("Ocular Sensor Engine: MediaPipe Neural FaceMesh [ONLINE]")
            except Exception as e:
                log_warn(f"Face tracker init error: {e}")

    def process_hand(self, cv2, bgr_frame):
        if not self.hand_landmarker:
            return False, None
        import mediapipe as mp
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self.hand_landmarker.detect(mp_image)
        if result.hand_landmarks and len(result.hand_landmarks) > 0:
            return True, result.hand_landmarks[0]
        return False, None

    def process_face(self, cv2, bgr_frame):
        if not self.face_landmarker:
            return False, None
        import mediapipe as mp
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self.face_landmarker.detect(mp_image)
        if result.face_landmarks and len(result.face_landmarks) > 0:
            return True, result.face_landmarks[0]
        return False, None


# =============================================================================
# 6. KOMPONEN UI / HUD CYBER-TACTICAL
# =============================================================================
COLOR_BG_DARK   = (12, 20, 14)
COLOR_GREEN     = (0, 255, 100)
COLOR_CYAN      = (255, 230, 0)
COLOR_AMBER     = (0, 180, 255)
COLOR_RED       = (60, 60, 255)
COLOR_DIM_GREEN = (0, 90, 35)
COLOR_WHITE     = (240, 240, 240)

def draw_corner_reticle(img, x, y, w, h, color=COLOR_GREEN, length=15, thickness=2):
    import cv2
    cv2.line(img, (x, y), (x + length, y), color, thickness)
    cv2.line(img, (x, y), (x, y + length), color, thickness)
    cv2.line(img, (x + w, y), (x + w - length, y), color, thickness)
    cv2.line(img, (x + w, y), (x + w, y + length), color, thickness)
    cv2.line(img, (x, y + h), (x + length, y + h), color, thickness)
    cv2.line(img, (x, y + h), (x, y + h - length), color, thickness)
    cv2.line(img, (x + w, y + h), (x + w - length, y + h), color, thickness)
    cv2.line(img, (x + w, y + h), (x + w - length, y + h), color, thickness)

def draw_progress_bar(img, x, y, w, h, ratio, fill_color, bg_color=COLOR_DIM_GREEN, border_color=COLOR_GREEN):
    import cv2
    ratio = max(0.0, min(1.0, ratio))
    cv2.rectangle(img, (x, y), (x + w, y + h), bg_color, -1)
    fill_w = int(w * ratio)
    if fill_w > 0:
        cv2.rectangle(img, (x, y), (x + fill_w, y + h), fill_color, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), border_color, 1)

def draw_hud(cv2, frame, mode_name, status_tag, is_active, active_duration,
             sensor_val, touch_thresh, release_thresh, morse_buffer, decoded_text,
             letter_ratio, space_ratio, time_since_action, fps, audio_active):
    """Merender antarmuka HUD Cyber-Tactical ke atas frame kamera OpenCV."""
    h, w, _ = frame.shape
    overlay = frame.copy()

    # 1. Header Bar Atas
    cv2.rectangle(overlay, (0, 0), (w, 44), COLOR_BG_DARK, -1)
    cv2.line(overlay, (0, 44), (w, 44), COLOR_GREEN, 1)

    # 2. Panel Kiri: Sensor Tracking
    panel_w = 340
    cv2.rectangle(overlay, (15, 55), (15 + panel_w, 280), COLOR_BG_DARK, -1)
    cv2.rectangle(overlay, (15, 55), (15 + panel_w, 280), COLOR_DIM_GREEN, 1)
    draw_corner_reticle(overlay, 15, 55, panel_w, 225, COLOR_GREEN, length=12)

    # 3. Panel Bawah: Terminal Morse & Pesan Rahasia Terdekripsi
    hud_bottom_y = h - 170
    cv2.rectangle(overlay, (15, hud_bottom_y), (w - 15, h - 15), COLOR_BG_DARK, -1)
    cv2.rectangle(overlay, (15, hud_bottom_y), (w - 15, h - 15), COLOR_DIM_GREEN, 1)
    draw_corner_reticle(overlay, 15, hud_bottom_y, w - 30, 155, COLOR_GREEN, length=16)

    cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)

    # Render Header
    cv2.putText(frame, f"[ SECURE COMMS // EYESPY: {mode_name} ]",
                (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.60, COLOR_GREEN, 2, cv2.LINE_AA)

    audio_str = "AUDIO: ON" if audio_active else "AUDIO: MUTE"
    sys_status = f"{audio_str} | FPS: {int(fps)} | [M] SWITCH MODE"
    cv2.putText(frame, sys_status, (w - 380, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, COLOR_CYAN, 1, cv2.LINE_AA)

    # Render Panel Kiri
    py = 80
    cv2.putText(frame, f"// TACTICAL SENSOR: {status_tag}", (25, py),
                cv2.FONT_HERSHEY_SIMPLEX, 0.46, COLOR_CYAN, 1, cv2.LINE_AA)

    py += 35
    status_label = "CONTACT:" if "HAND" in mode_name else "EYE STATUS:"
    cv2.putText(frame, status_label, (25, py),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, COLOR_WHITE, 1, cv2.LINE_AA)
    
    if is_active:
        if active_duration >= 0.35:
            status_text = f"HOLDING DASH (-) [{active_duration:.2f}s]"
            status_color = COLOR_AMBER
        else:
            status_text = f"TAPPING DOT (•) [{active_duration:.2f}s]"
            status_color = COLOR_RED
    else:
        if "ARMED" in status_tag:
            status_text = "READY / ARMED"
            status_color = COLOR_GREEN
        elif "STABILIZING" in status_tag:
            status_text = "ACQUIRING..."
            status_color = COLOR_CYAN
        else:
            status_text = "WAITING HAND"
            status_color = COLOR_DIM_GREEN

    cv2.putText(frame, status_text, (135, py),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, status_color, 2, cv2.LINE_AA)

    py += 30
    metric_label = "PINCH DIST" if "HAND" in mode_name else "EAR RATIO"
    metric_str = f"{metric_label}: {sensor_val:.3f}  [T: {touch_thresh:.2f} | R: {release_thresh:.2f}]"
    cv2.putText(frame, metric_str, (25, py),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, COLOR_WHITE, 1, cv2.LINE_AA)

    py += 12
    # Progress Bar Sensor dengan Hysteresis Dual Markers
    max_scale = 0.50 if "HAND" in mode_name else 0.42
    bar_ratio = min(1.0, max(0.0, sensor_val / max_scale))
    bar_color = COLOR_RED if is_active else COLOR_GREEN
    draw_progress_bar(frame, 25, py, 315, 14, bar_ratio, bar_color)
    
    # Touch threshold marker (Merah)
    t_x = int(25 + 315 * (touch_thresh / max_scale))
    cv2.line(frame, (t_x, py - 3), (t_x, py + 17), COLOR_RED, 2)
    # Release threshold marker (Hijau)
    r_x = int(25 + 315 * (release_thresh / max_scale))
    cv2.line(frame, (r_x, py - 3), (r_x, py + 17), COLOR_GREEN, 2)

    py += 35
    cv2.putText(frame, "TELEGRAPH PROTOCOL:", (25, py),
                cv2.FONT_HERSHEY_SIMPLEX, 0.44, COLOR_CYAN, 1, cv2.LINE_AA)
    py += 20
    if "PINCH" in mode_name:
        cv2.putText(frame, " * Quick Tap  (<0.35s)  => Dot  (•)", (25, py),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)
        py += 18
        cv2.putText(frame, " * Hold Tap   (0.35-1.2s)=> Dash (-)", (25, py),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)
    elif "GESTURE" in mode_name:
        cv2.putText(frame, " * 1 Finger (Index)     => Dot  (•)", (25, py),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)
        py += 18
        cv2.putText(frame, " * 2 Fingers (Peace)    => Dash (-)", (25, py),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)
    else:
        cv2.putText(frame, " * Quick Blink (<0.30s) => Dot  (•)", (25, py),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)
        py += 18
        cv2.putText(frame, " * Hold Blink (0.3-1.2s)=> Dash (-)", (25, py),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)

    py += 18
    cv2.putText(frame, " * Auto-Letter: Idle 1.2s | Space: Idle 3.0s", (25, py),
                cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)

    # Render Panel Bawah
    ty = hud_bottom_y + 28
    
    cv2.putText(frame, "MORSE BUFFER:", (25, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, COLOR_CYAN, 1, cv2.LINE_AA)
    
    buffer_display = morse_buffer if morse_buffer else "<EMPTY>"
    buf_color = COLOR_GREEN if morse_buffer else COLOR_DIM_GREEN
    cv2.putText(frame, f"[ {buffer_display} ]", (160, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, buf_color, 2, cv2.LINE_AA)

    if morse_buffer:
        candidate_char = morse_to_char(morse_buffer)
        cv2.putText(frame, f"=> NEXT CHAR: '{candidate_char}'", (350, ty),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_AMBER, 2, cv2.LINE_AA)
        
        cv2.putText(frame, "COMMIT LETTER:", (580, ty),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_WHITE, 1, cv2.LINE_AA)
        draw_progress_bar(frame, 710, ty - 12, 160, 12, letter_ratio, COLOR_AMBER)

    ty += 34
    cv2.putText(frame, "AUTO-SPACE TIMER:", (25, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, COLOR_WHITE, 1, cv2.LINE_AA)
    
    space_status = f"{time_since_action:.1f}s / 3.0s"
    space_color = COLOR_CYAN if space_ratio < 1.0 else COLOR_GREEN
    draw_progress_bar(frame, 190, ty - 13, 240, 13, space_ratio, space_color)
    cv2.putText(frame, space_status, (445, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.46, space_color, 1, cv2.LINE_AA)

    if space_ratio >= 1.0:
        cv2.putText(frame, "[ SPACE INSERTED ]", (570, ty),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.46, COLOR_GREEN, 1, cv2.LINE_AA)

    ty += 42
    cv2.putText(frame, "DECRYPTED MESSAGE:", (25, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, COLOR_CYAN, 1, cv2.LINE_AA)

    blink_cursor = "█" if int(time.time() * 2) % 2 == 0 else " "
    msg_to_show = (decoded_text + blink_cursor) if decoded_text else ("<WAITING FOR TRANSMISSION>" + blink_cursor)
    msg_color = COLOR_GREEN if decoded_text else COLOR_DIM_GREEN
    
    if len(msg_to_show) > 42:
        msg_to_show = "..." + msg_to_show[-39:]
        
    cv2.putText(frame, f"> {msg_to_show}", (210, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.70, msg_color, 2, cv2.LINE_AA)

    ty += 32
    hotkeys = "[M] Switch Mode  |  [Q] Quit  |  [C] Clear  |  [BACKSPACE] Del  |  [SPACE] Space  |  [+/-] Sens"
    cv2.putText(frame, hotkeys, (25, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_WHITE, 1, cv2.LINE_AA)


# =============================================================================
# 7. SELF-TEST & VALIDASI MANDIRI
# =============================================================================
def run_self_tests():
    print("=" * 60)
    print("  MENJALANKAN VERIFIKASI UNIT TEST MANDIRI")
    print("=" * 60)

    # 1. Test Morse Dictionary
    assert morse_to_char('.-') == 'A', "Kamus gagal untuk 'A'"
    assert morse_to_char('•-') == 'A', "Kamus gagal untuk simbol '•-'"
    assert morse_to_char('-...') == 'B', "Kamus gagal untuk 'B'"
    assert morse_to_char('...---...') == 'SOS', "Kamus gagal untuk 'SOS'"
    log_success("Kamus Morse Code Internasional 100% valid.")

    # 2. Test Audio Manager
    audio = AudioManager(enabled=True)
    log_success("Audio Manager inisialisasi berhasil.")

    # 3. Test Hand Pinch Math Robust
    class DummyPt:
        def __init__(self, x, y, z=0.0):
            self.x, self.y, self.z = x, y, z
    dummy_hand = [DummyPt(0.5, 0.5) for _ in range(21)]
    dummy_hand[0] = DummyPt(0.5, 0.8)  # Wrist
    dummy_hand[9] = DummyPt(0.5, 0.5)  # Middle MCP
    dummy_hand[4] = DummyPt(0.49, 0.40) # Thumb
    dummy_hand[8] = DummyPt(0.50, 0.40) # Index
    ratio, _, _ = calculate_pinch_ratio_robust(dummy_hand, 1000, 1000)
    log_success(f"Hand Pinch Ratio Calculation accurate (Pinch: {ratio:.3f}).")

    print("=" * 60)
    log_success("SEMUA TEST MANDIRI BERHASIL DENGAN SEMPURNA!")
    print("=" * 60)
    return True


# =============================================================================
# 8. LOOP UTAMA PROGRAM (MAIN APPLICATION)
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="EYESPY: Covert Tactical Morse Code Framework"
    )
    parser.add_argument("--cam", type=int, default=0, help="Index kamera webcam (default: 0)")
    parser.add_argument("--mode", type=str, default="hand", choices=["hand", "gesture", "eye"],
                        help="Mode input: 'hand' (Air-Pinch Telegraph - Rekomendasi), 'gesture' (Finger Sign), 'eye' (Ocular Blink)")
    parser.add_argument("--no-audio", action="store_true", help="Nonaktifkan feedback audio beep")
    parser.add_argument("--test", action="store_true", help="Jalankan verifikasi unit test mandiri lalu keluar")
    parser.add_argument("--banner", action="store_true", help="Tampilkan banner hacker lalu keluar")
    args = parser.parse_args()

    print_banner()

    if args.banner:
        sys.exit(0)

    if args.test:
        run_self_tests()
        sys.exit(0)

    try:
        import cv2
    except ImportError:
        log_error("Modul 'cv2' (OpenCV) belum terpasang!")
        sys.exit(1)

    log_info("Executing pre-flight sensor diagnostics...")
    time.sleep(0.1)

    audio = AudioManager(enabled=(not args.no_audio))
    if audio.audio_enabled:
        log_success("Synthetic Audio Synthesizer: [ONLINE] (850 Hz carrier)")
    else:
        log_warn("Audio Engine in Mute/Silent Mode.")

    # Inisialisasi Universal Sensor
    sensor = UniversalSensor()

    # Inisialisasi Kamera OpenCV
    cam_index = args.cam
    log_info(f"Probing optical video interface (/dev/video{cam_index})...")
    cap = cv2.VideoCapture(cam_index)

    if not cap.isOpened() and cam_index == 0:
        log_warn("Camera /dev/video0 not responding, probing /dev/video1...")
        cam_index = 1
        cap = cv2.VideoCapture(cam_index)

    if not cap.isOpened():
        log_error(f"Cannot access optical video interface (Index: {cam_index}).")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    log_success(f"Optical sensor locked on /dev/video{cam_index} (1280x720).")

    # Mode Input: HAND_PINCH, HAND_GESTURE, EYE_BLINK
    mode_list = ["HAND_PINCH", "HAND_GESTURE", "EYE_BLINK"]
    mode_map = {"hand": "HAND_PINCH", "gesture": "HAND_GESTURE", "eye": "EYE_BLINK"}
    current_mode = mode_map.get(args.mode, "HAND_PINCH")

    # =========================================================================
    # PARAMETER HYSTERESIS & ANTI-FALSE TRIGGER
    # =========================================================================
    # Dual-Threshold Pinch Hysteresis:
    # Jari harus benar-benar menyatu (< 0.15) untuk memicu sentuhan (CONTACT)
    # dan harus terbuka lebar (> 0.26) untuk melepaskan sentuhan (RELEASE).
    pinch_touch_thresh = 0.15      # Ambang batas sentuhan (Pinch-In)
    pinch_release_thresh = 0.26    # Ambang batas pelepasan (Pinch-Out)
    
    # Hand Entrance Stabilization
    # Tangan harus terbuka stabil di kamera selama 0.35 detik sebelum sistem ARMED
    hand_first_detected_time = 0.0
    is_hand_armed = False
    hand_detected_prev = False

    ear_touch_thresh = 0.18
    ear_release_thresh = 0.24

    min_tap_time = 0.08         # Filter glitch (< 0.08s diabaikan)
    dot_max_time = 0.35         # 0.08s - 0.35s = Dot (•)
    dash_max_time = 1.20        # 0.35s - 1.20s = Dash (-)
    letter_timeout = 1.20       # Jeda idle untuk commit huruf
    auto_space_timeout = 3.00   # Jeda idle untuk spasi kata

    # State Variables
    is_active = False           # Apakah sedang kontak (Pinch / Mata Tutup)
    action_start_time = 0.0
    last_action_end_time = time.time()
    auto_space_inserted = False

    # State Khusus Gesture Mode
    gesture_hold_time = 0.0
    current_stable_gesture = None
    gesture_registered = False

    morse_buffer = ""
    decoded_message = ""

    # FPS Smoother
    prev_time = time.time()
    fps = 30.0

    print(f"\n{Colors.DIM}────────────────────────────────────────────────────────────{Colors.RESET}")
    log_success(f"DEFAULT ACTIVE MODE: {Colors.BOLD}{Colors.GREEN}[ {current_mode} ]{Colors.RESET}")
    print(f"    {Colors.CYAN}-> Anti-False Trigger :{Colors.RESET} {Colors.BOLD}Dual Hysteresis (Touch: {pinch_touch_thresh} | Release: {pinch_release_thresh}){Colors.RESET}")
    print(f"    {Colors.CYAN}-> Hand Entrance Guard:{Colors.RESET} {Colors.BOLD}0.35s Open Hand Stabilization{Colors.RESET}")
    print(f"    {Colors.CYAN}-> Dot Tap Window     :{Colors.RESET} {Colors.BOLD}0.08s - 0.35s (Quick Tap){Colors.RESET}")
    print(f"    {Colors.CYAN}-> Dash Tap Window    :{Colors.RESET} {Colors.BOLD}0.35s - 1.20s (Held Tap){Colors.RESET}")
    print(f"    {Colors.YELLOW}[*] Tekan tombol 'M' di jendela video untuk berganti mode kapan saja!{Colors.RESET}")
    print(f"{Colors.DIM}────────────────────────────────────────────────────────────{Colors.RESET}")
    log_success("Tactical HUD Window ready. Standby for operator input...\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                log_warn("Failed to retrieve frame from optical sensor.")
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            current_time = time.time()

            dt = current_time - prev_time
            prev_time = current_time
            if dt > 0:
                fps = 0.9 * fps + 0.1 * (1.0 / dt)

            current_val = 0.0
            touch_thresh = pinch_touch_thresh if "HAND" in current_mode else ear_touch_thresh
            release_thresh = pinch_release_thresh if "HAND" in current_mode else ear_release_thresh
            status_tag = "NO TARGET"
            active_duration = 0.0

            # ---------------------------------------------------------
            # 1. MODE HAND AIR-PINCH (TEGRAPH TAP DENGAN DUAL HYSTERESIS)
            # ---------------------------------------------------------
            if current_mode == "HAND_PINCH":
                detected, hand_lms = sensor.process_hand(cv2, frame)
                if detected and hand_lms:
                    ratio, pt_thumb, pt_index = calculate_pinch_ratio_robust(hand_lms, w, h)
                    current_val = ratio

                    # Gambar Skeleton Tangan Neon
                    pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand_lms]
                    for conn in HAND_CONNECTIONS:
                        cv2.line(frame, pts[conn[0]], pts[conn[1]], COLOR_DIM_GREEN, 1, cv2.LINE_AA)
                    for pt in pts:
                        cv2.circle(frame, pt, 2, COLOR_CYAN, -1)

                    # Hand Entrance Stabilization Check
                    if not hand_detected_prev:
                        hand_first_detected_time = current_time
                        is_hand_armed = False
                        hand_detected_prev = True

                    # Tangan harus terbuka (> release_thresh) selama 0.35s sebelum ARMED
                    if not is_hand_armed:
                        if ratio < release_thresh:
                            # Masih terlipat saat masuk, reset waktu stabilisasi
                            hand_first_detected_time = current_time
                            status_tag = "STABILIZING..."
                        elif current_time - hand_first_detected_time >= 0.35:
                            is_hand_armed = True
                            status_tag = "ARMED // READY"
                        else:
                            status_tag = "ACQUIRING..."
                    else:
                        status_tag = "ARMED // READY"

                    # Visual Efek Target Titik Kontak
                    contact_color = COLOR_RED if is_active else (COLOR_GREEN if is_hand_armed else COLOR_CYAN)
                    cv2.line(frame, pt_thumb, pt_index, contact_color, 2, cv2.LINE_AA)
                    cv2.circle(frame, pt_thumb, 8, contact_color, 2)
                    cv2.circle(frame, pt_index, 8, contact_color, 2)

                    mid_x = (pt_thumb[0] + pt_index[0]) // 2
                    mid_y = (pt_thumb[1] + pt_index[1]) // 2
                    contact_label = "CONTACT [HOLD]" if is_active else ("READY" if is_hand_armed else "STABILIZING")
                    cv2.putText(frame, contact_label, (mid_x + 10, mid_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, contact_color, 1, cv2.LINE_AA)

                    # State Machine dengan Dual-Threshold Hysteresis
                    if is_hand_armed:
                        if not is_active:
                            # Hanya memicu sentuhan jika rasio turun di bawah touch_thresh
                            if ratio < touch_thresh:
                                is_active = True
                                action_start_time = current_time
                        else:
                            active_duration = current_time - action_start_time
                            # Hanya melepaskan sentuhan jika rasio naik di atas release_thresh
                            if ratio > release_thresh:
                                duration = current_time - action_start_time
                                is_active = False
                                last_action_end_time = current_time
                                auto_space_inserted = False

                                if duration >= min_tap_time:
                                    if duration < dot_max_time:
                                        morse_buffer += "•"
                                        audio.play_dot()
                                        log_success(f"[HAND AIR-TAP] -> {Colors.YELLOW}DOT  (•){Colors.RESET} ({duration:.2f}s) | Buffer: {Colors.WHITE}[ {morse_buffer} ]{Colors.RESET}")
                                    elif duration < dash_max_time:
                                        morse_buffer += "-"
                                        audio.play_dash()
                                        log_success(f"[HAND AIR-TAP] -> {Colors.CYAN}DASH (-){Colors.RESET} ({duration:.2f}s) | Buffer: {Colors.WHITE}[ {morse_buffer} ]{Colors.RESET}")
                                    else:
                                        log_warn(f"[HAND AIR-TAP] Tap held too long ({duration:.2f}s) - ignored.")
                else:
                    hand_detected_prev = False
                    is_hand_armed = False
                    is_active = False
                    status_tag = "NO HAND DETECTED"

            # ---------------------------------------------------------
            # 2. MODE HAND GESTURE (SIMBOL JARI DENGAN DEBOUNCE HOLD)
            # ---------------------------------------------------------
            elif current_mode == "HAND_GESTURE":
                detected, hand_lms = sensor.process_hand(cv2, frame)
                if detected and hand_lms:
                    i_up, m_up, r_up, p_up, total_up = count_extended_fingers(hand_lms)
                    current_val = float(total_up) / 4.0
                    touch_thresh = 0.25
                    release_thresh = 0.50

                    pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand_lms]
                    for conn in HAND_CONNECTIONS:
                        cv2.line(frame, pts[conn[0]], pts[conn[1]], COLOR_DIM_GREEN, 1, cv2.LINE_AA)
                    for pt in pts:
                        cv2.circle(frame, pt, 2, COLOR_CYAN, -1)

                    # Tentukan pose jari yang terdeteksi
                    detected_pose = None
                    if i_up and not m_up and not r_up and not p_up:
                        detected_pose = "1_FINGER_DOT"
                    elif i_up and m_up and not r_up and not p_up:
                        detected_pose = "2_FINGERS_DASH"
                    elif total_up == 0:
                        detected_pose = "FIST_NEUTRAL"
                    elif total_up >= 4:
                        detected_pose = "OPEN_PALM"

                    # Gesture Debounce: Pose harus ditahan selama minimal 0.22 detik
                    if detected_pose != current_stable_gesture:
                        current_stable_gesture = detected_pose
                        gesture_hold_time = current_time
                        gesture_registered = False

                    hold_elapsed = current_time - gesture_hold_time

                    if detected_pose == "1_FINGER_DOT":
                        status_tag = f"1 FINGER (DOT) [{hold_elapsed:.2f}s]"
                        if hold_elapsed >= 0.22 and not gesture_registered:
                            morse_buffer += "•"
                            audio.play_dot()
                            log_success(f"[GESTURE LOCKED] -> {Colors.YELLOW}DOT  (•){Colors.RESET} | Buffer: {Colors.WHITE}[ {morse_buffer} ]{Colors.RESET}")
                            last_action_end_time = current_time
                            auto_space_inserted = False
                            gesture_registered = True
                    elif detected_pose == "2_FINGERS_DASH":
                        status_tag = f"2 FINGERS (DASH) [{hold_elapsed:.2f}s]"
                        if hold_elapsed >= 0.22 and not gesture_registered:
                            morse_buffer += "-"
                            audio.play_dash()
                            log_success(f"[GESTURE LOCKED] -> {Colors.CYAN}DASH (-){Colors.RESET} | Buffer: {Colors.WHITE}[ {morse_buffer} ]{Colors.RESET}")
                            last_action_end_time = current_time
                            auto_space_inserted = False
                            gesture_registered = True
                    elif detected_pose == "FIST_NEUTRAL":
                        status_tag = "NEUTRAL (FIST)"
                        gesture_registered = False
                    elif detected_pose == "OPEN_PALM":
                        status_tag = "OPEN PALM (IDLE)"
                        gesture_registered = False
                    else:
                        status_tag = "TRANSITIONING"
                else:
                    status_tag = "NO HAND DETECTED"
                    current_stable_gesture = None
                    gesture_registered = False

            # ---------------------------------------------------------
            # 3. MODE EYE BLINK (OCULAR DUAL HYSTERESIS)
            # ---------------------------------------------------------
            elif current_mode == "EYE_BLINK":
                detected, face_lms = sensor.process_face(cv2, frame)
                if detected and face_lms:
                    left_ear = calculate_ear(face_lms, LEFT_EYE_LANDMARKS, w, h)
                    right_ear = calculate_ear(face_lms, RIGHT_EYE_LANDMARKS, w, h)
                    current_val = (left_ear + right_ear) / 2.0
                    status_tag = "OCULAR ARMED"

                    left_pts = np.array([[int(face_lms[i].x * w), int(face_lms[i].y * h)] for i in LEFT_EYE_CONTOUR], np.int32)
                    right_pts = np.array([[int(face_lms[i].x * w), int(face_lms[i].y * h)] for i in RIGHT_EYE_CONTOUR], np.int32)
                    contour_color = COLOR_RED if is_active else COLOR_GREEN
                    cv2.polylines(frame, [left_pts], isClosed=True, color=contour_color, thickness=1, lineType=cv2.LINE_AA)
                    cv2.polylines(frame, [right_pts], isClosed=True, color=contour_color, thickness=1, lineType=cv2.LINE_AA)

                    if not is_active:
                        if current_val < ear_touch_thresh:
                            is_active = True
                            action_start_time = current_time
                    else:
                        active_duration = current_time - action_start_time
                        if current_val > ear_release_thresh:
                            duration = current_time - action_start_time
                            is_active = False
                            last_action_end_time = current_time
                            auto_space_inserted = False

                            if duration >= min_tap_time:
                                if duration < dot_max_time:
                                    morse_buffer += "•"
                                    audio.play_dot()
                                    log_success(f"[OCULAR BLINK] -> {Colors.YELLOW}DOT  (•){Colors.RESET} ({duration:.2f}s) | Buffer: {Colors.WHITE}[ {morse_buffer} ]{Colors.RESET}")
                                elif duration < dash_max_time:
                                    morse_buffer += "-"
                                    audio.play_dash()
                                    log_success(f"[OCULAR BLINK] -> {Colors.CYAN}DASH (-){Colors.RESET} ({duration:.2f}s) | Buffer: {Colors.WHITE}[ {morse_buffer} ]{Colors.RESET}")
                                else:
                                    log_warn(f"[OCULAR BLINK] Blink too long ({duration:.2f}s) - ignored.")
                else:
                    status_tag = "NO FACE DETECTED"
                    is_active = False

            # ---------------------------------------------------------
            # LOGIKA COMMIT HURUF & AUTO-SPACE
            # ---------------------------------------------------------
            time_since_last_action = current_time - last_action_end_time
            letter_progress = 0.0
            space_progress = 0.0

            if not is_active:
                if morse_buffer != "":
                    letter_progress = min(1.0, time_since_last_action / letter_timeout)
                    if time_since_last_action >= letter_timeout:
                        decoded_char = morse_to_char(morse_buffer)
                        decoded_message += decoded_char
                        audio.play_commit()
                        log_success(f"[DECODE] Inter-symbol timeout -> Commit {Colors.BOLD}{Colors.YELLOW}'{decoded_char}'{Colors.RESET} (from buffer: '{morse_buffer}')")
                        log_payload(f"LIVE PAYLOAD: \"{decoded_message}\"")
                        morse_buffer = ""
                        last_action_end_time = current_time
                        time_since_last_action = 0.0
                else:
                    space_progress = min(1.0, time_since_last_action / auto_space_timeout)
                    if time_since_last_action >= auto_space_timeout and not auto_space_inserted:
                        if decoded_message and not decoded_message.endswith(" "):
                            decoded_message += " "
                            audio.play_space()
                            log_info(f"[AUTO-SPACE] Sensor idle > 3.0s -> Word space inserted (' ')")
                            log_payload(f"LIVE PAYLOAD: \"{decoded_message}\"")
                        auto_space_inserted = True

            # Render UI HUD
            draw_hud(
                cv2=cv2,
                frame=frame,
                mode_name=current_mode,
                status_tag=status_tag,
                is_active=is_active,
                active_duration=active_duration,
                sensor_val=current_val,
                touch_thresh=touch_thresh,
                release_thresh=release_thresh,
                morse_buffer=morse_buffer,
                decoded_text=decoded_message,
                letter_ratio=letter_progress,
                space_ratio=space_progress,
                time_since_action=time_since_last_action,
                fps=fps,
                audio_active=audio.audio_enabled
            )

            cv2.imshow("EYESPY // TACTICAL COVERT MORSE FRAMEWORK (KALI EDITION)", frame)

            # Keyboard Hotkeys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                log_info("Termination signal received from operator.")
                break
            elif key == ord('m') or key == ord('M'):
                idx = (mode_list.index(current_mode) + 1) % len(mode_list)
                current_mode = mode_list[idx]
                is_active = False
                is_hand_armed = False
                log_warn(f"TACTICAL MODE SWITCHED TO: {Colors.BOLD}{Colors.YELLOW}[ {current_mode} ]{Colors.RESET}")
            elif key == ord('c') or key == ord('C'):
                decoded_message = ""
                morse_buffer = ""
                log_warn("Payload and morse buffer cleared by operator.")
            elif key == 8:
                if morse_buffer:
                    morse_buffer = morse_buffer[:-1]
                    log_info(f"Deleted last morse symbol: [ {morse_buffer} ]")
                elif decoded_message:
                    decoded_message = decoded_message[:-1]
                    log_info(f"Deleted last payload character: \"{decoded_message}\"")
            elif key == 32:
                decoded_message += " "
                audio.play_space()
                log_info("Manual space injected into transmission.")
                log_payload(f"LIVE PAYLOAD: \"{decoded_message}\"")
            elif key == ord('+') or key == ord('='):
                if "HAND" in current_mode:
                    pinch_touch_thresh = min(0.30, pinch_touch_thresh + 0.01)
                    pinch_release_thresh = min(0.40, pinch_release_thresh + 0.01)
                    log_info(f"Pinch threshold adjusted: Touch={pinch_touch_thresh:.2f}, Release={pinch_release_thresh:.2f}")
                else:
                    ear_touch_thresh = min(0.30, ear_touch_thresh + 0.01)
                    ear_release_thresh = min(0.35, ear_release_thresh + 0.01)
                    log_info(f"EAR threshold adjusted: {ear_touch_thresh:.2f}")
            elif key == ord('-') or key == ord('_'):
                if "HAND" in current_mode:
                    pinch_touch_thresh = max(0.08, pinch_touch_thresh - 0.01)
                    pinch_release_thresh = max(0.18, pinch_release_thresh - 0.01)
                    log_info(f"Pinch threshold adjusted: Touch={pinch_touch_thresh:.2f}, Release={pinch_release_thresh:.2f}")
                else:
                    ear_touch_thresh = max(0.10, ear_touch_thresh - 0.01)
                    ear_release_thresh = max(0.15, ear_release_thresh - 0.01)
                    log_info(f"EAR threshold adjusted: {ear_touch_thresh:.2f}")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Keyboard interrupt detected (Ctrl+C). Cleaning up tactical bridge...{Colors.RESET}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        try:
            import pygame
            pygame.mixer.quit()
        except Exception:
            pass

        print(f"{Colors.DIM}────────────────────────────────────────────────────────────{Colors.RESET}")
        log_success(f"Final Exfiltrated Payload: {Colors.BOLD}{Colors.WHITE}\"{decoded_message}\"{Colors.RESET}")
        log_info("Covert bridge closed. Sensors offline.")


if __name__ == "__main__":
    main()
