import torch
import torch.nn as nn
from torchvision import transforms
from PIL import ImageGrab
from pynput.keyboard import Controller, Key, Listener
import time

# --- CONFIG --- #
MODEL_PATH = "celeste.pth"  # trained model
BBOX = (100, 200, 800, 600)               # game window region
SLEEP_TIME = 0.1
THRESHOLD = 0.5                           # probability threshold for key press

# --- MODEL (must match training) --- #
class GameNet(nn.Module):
    def __init__(self, num_actions):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=8, stride=4), nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1), nn.ReLU(),
            nn.Flatten()
        )
        self.fc = nn.Sequential(
            nn.Linear(64*7*7, 512), nn.ReLU(),
            nn.Linear(512, num_actions)
        )
    def forward(self, x):
        return self.fc(self.cnn(x))

# --- LOAD MODEL --- #
device = "cuda" if torch.cuda.is_available() else "cpu"

# Must match your dataset 
#Detected 8 actions: {'Key.ctrl': 0, 'Key.down': 1, 'Key.left': 2, 'Key.right': 3, 'Key.up': 4, 'x': 5, 'z': 6, 'NOOP': 7}
label_to_key = {
    0: "Key.ctrl",
    1: "Key.down",
    2: "Key.left",
    3: "Key.right",
    4: "Key.up",        # jump
    5: "x",
    6: "z",
    7:"NOOP"
}
num_actions = len(label_to_key)

model = GameNet(num_actions).to(device)
state_dict = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(state_dict)
model.eval()

# --- TRANSFORM --- #
transform = transforms.Compose([
    transforms.Resize((84, 84)),
    transforms.Grayscale(),
    transforms.ToTensor()
])

# --- KEYBOARD CONTROL --- #
keyboard = Controller()
running = True
currently_being_pressed = []
from pynput.keyboard import Controller, Key

keyboard = Controller()
currently_being_pressed = set()

def press_key(key_name: str):
    """
    Press a key and keep it pressed until it's no longer predicted.
    key_name: str, e.g. "Key.right" or "z" or "NOOP"
    """
    global currently_being_pressed

    if key_name == "NOOP":
        # Release all keys if NOOP is predicted
        for k in list(currently_being_pressed):
            release_key(k)
        return

    if key_name not in currently_being_pressed:
        # Press new key
        key_attr = key_name.split(".")[1] if key_name.startswith("Key.") else key_name
        key = getattr(Key, key_attr) if key_name.startswith("Key.") else key_attr
        keyboard.press(key)
        currently_being_pressed.add(key_name)

def press_key(key_name: str):
    global currently_being_pressed
    if key_name == "NOOP":
        for k in list(currently_being_pressed):
            release_key(k)
        return

    if key_name not in currently_being_pressed:
        if key_name.startswith("Key."):
            key_attr = key_name.split(".")[1].lower()
            key = getattr(Key, key_attr)
        else:
            key = key_name  # regular character, e.g., 'z'

        keyboard.press(key)
        currently_being_pressed.add(key_name)

def release_key(key_name: str):
    global currently_being_pressed
    if key_name in currently_being_pressed:
        if key_name.startswith("Key."):
            key_attr = key_name.split(".")[1].lower()
            key = getattr(Key, key_attr)
        else:
            key = key_name  # regular character, e.g., 'z'

        keyboard.release(key)
        currently_being_pressed.remove(key_name)

# --- STOP WITH ESC --- #
def on_press(key):
    global running
    if key == Key.esc:
        running = False
        return False  # stop listener

listener = Listener(on_press=on_press)
listener.start()

# --- MAIN LOOP --- #
print("Starting live play in 3 seconds...")
time.sleep(3)

while running:
    # Grab screenshot
    img = ImageGrab.grab(bbox=BBOX).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)
    print(currently_being_pressed)
    with torch.no_grad():
        logits = model(img_tensor)
        probs = torch.sigmoid(logits).squeeze(0)  # shape [num_actions]

    # Decide which actions to take
    active_actions = [i for i, p in enumerate(probs) if p > THRESHOLD]
    # Suppose active_actions is the list of currently predicted keys:
    predicted_keys = [label_to_key[i] for i in active_actions]

    # Release keys that are no longer predicted
    for k in list(currently_being_pressed):
        if k not in predicted_keys:
            release_key(k)

# Press any new keys
    for k in predicted_keys:
        press_key(k)

    time.sleep(SLEEP_TIME)

listener.stop()
print("Live play stopped.")