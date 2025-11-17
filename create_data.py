import os
import cv2
import numpy as np
from pynput import keyboard
import mss
import time

# --- Configuration ---
SAVE_DIR = "dataset"
os.makedirs(SAVE_DIR, exist_ok=True)
FRAME_RATE = 30  # frames per second
MONITOR = {"top": 100, "left": 200, "width": 800, "height": 600}  # adjust to your game window
MAX_OF_FRAME = 100000
STOP_AFTER_MAX = True
# --- Storage ---
frame_count = 0
actions = []

current_keys = set()

# --- Functions ---
def on_press(key):
    try:
        current_keys.add(key.char)  # letters, numbers
    except AttributeError:
        current_keys.add(str(key))  # special keys
    return True

def on_release(key):
    try:
        current_keys.discard(key.char)
    except AttributeError:
        current_keys.discard(str(key))
    # Optional: stop recording on ESC
    if key == keyboard.Key.esc:
        return False

# --- Screen capture ---
sct = mss.mss()
last_time = time.time()

# --- Keyboard listener ---
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
print("começando daqui a 3 segundos")
time.sleep(3)
print("começou")
try:
    while True:
        # Control frame rate
        if time.time() - last_time < 1 / FRAME_RATE or len(current_keys) == 0:
            continue
        last_time = time.time()

        # Capture screen
        img = np.array(sct.grab(MONITOR))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Save image
        cv2.imwrite(os.path.join(SAVE_DIR, f"{frame_count}.png"), img)

        # Save current action as a list of keys pressed
        actions.append(list(current_keys))

        frame_count += 1

        if frame_count >= MAX_OF_FRAME and STOP_AFTER_MAX:  # stop after 100000 frames (optional)
            break

finally:
    listener.stop()
    # Save all actions
    np.save(os.path.join(SAVE_DIR, "actions.npy"), np.array(actions, dtype=object))
    print(f"Saved {frame_count} frames and actions.")
