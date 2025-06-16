# File: modules/gesture_control.py
import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np
import time

from .voice import speak
from .ai_brain import handle_conversation
from .utils import log_message

# Inisialisasi hanya sekali
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
screen_width, screen_height = pyautogui.size()
smooth_factor = 7
prev_x, prev_y = 0, 0

def count_fingers(hand_landmarks):
    if not hand_landmarks: return 0
    landmarks = hand_landmarks.landmark; finger_count = 0; tip_ids = [4, 8, 12, 16, 20]
    # Logika untuk ibu jari (tangan kanan)
    if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 2].x:
        finger_count += 1
    # Logika untuk 4 jari lainnya
    for tip_id in tip_ids[1:]:
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            finger_count += 1
    return finger_count

def run_gesture_mode(cap):
    """Menjalankan loop untuk mode kontrol gestur."""
    global prev_x, prev_y
    
    success, frame = cap.read()
    if not success:
        return 'gestur' # Tetap di mode gestur jika frame gagal

    frame_rgb = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        num_fingers = count_fingers(hand_landmarks)

        if num_fingers == 5:
            log_message("system", "Gestur keluar (5 jari) terdeteksi.")
            speak(handle_conversation("Konfirmasi bahwa mode gestur telah dinonaktifkan."))
            return 'suara'

        # Logika Gerakan Mouse dan Klik
        index_finger_tip = hand_landmarks.landmark[8]
        thumb_tip = hand_landmarks.landmark[4]
        target_x = np.interp(index_finger_tip.x, (0.1, 0.9), (0, screen_width))
        target_y = np.interp(index_finger_tip.y, (0.1, 0.9), (0, screen_height))
        curr_x = prev_x + (target_x - prev_x) / smooth_factor
        curr_y = prev_y + (target_y - prev_y) / smooth_factor
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y
        
        click_distance = math.hypot(thumb_tip.x - index_finger_tip.x, thumb_tip.y - index_finger_tip.y)
        if click_distance < 0.04:
            pyautogui.click()
            time.sleep(0.2)
    
    time.sleep(0.01)
    return 'gestur'