# GameMaster

**GameMaster** is a Python project that learns keyboard input from your gameplay. It takes screenshots of your screen and logs the keys you press, then trains a neural network to predict which keys you’re likely to press given a current screen. This can be used for tasks like creating intelligent game assistants, bot prototypes, or input prediction models.

---

## Table of Contents

- [Features](#features)  
- [How It Works](#how-it-works)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
- [Usage](#usage)  
  - [1. Data Collection](#1-data-collection)  
  - [2. Training](#2-training)  
  - [3. Inference / Playing Mode](#3-inference--playing-mode)  
- [Project Structure](#project-structure)  
- [Limitations](#limitations)  
- [Future Improvements](#future-improvements)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- Captures screenshots and keyboard input in real time  
- Saves paired data (screen image + key pressed)  
- Uses the captured data to train a neural network model  
- After training, you can run a “playing” mode where the model predicts probable keys from the screen  

---

## How It Works

1. **Data collection**: Run a training script that observes your screen and logs keyboard presses, saving them in a dataset.  
2. **Model training**: Use the collected data to train a neural network that learns the mapping from screen pixels → keyboard input.  
3. **Prediction**: Once trained, run a “playing” script where, given a screenshot, the model predicts which keys you are likely to press.  

---

## Getting Started

### Prerequisites

Make sure you have:

- Python 3.8+  
- A working keyboard (required — mouse-only input is not supported)  
- Enough disk space for storing screenshots (depends on how much data you collect)  
- (Optional, but recommended) A GPU if your dataset is large and you want faster training  

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Isntnot/GameMaster.git
   cd GameMaster
   ```
2. Create a virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate   # On Windows: `venv\Scripts\activate`
   ```
3. Install dependencies:
  ```bash
  pip install -r requirement.txt
  ```
## Usage
Here’s how to use the project in its main phases.
1. Data Collection
  Run the script to collect screen + key data:
  ```bash
  python create_data.py
  ```
  This will start taking screenshots at some interval (you might need to configure the frequency).
  Simultaneously, it listens for keyboard presses and saves the keys associated with each screenshot.
  Make sure to collect a diverse set of data (different game states, menus, etc.) so that the model learns well.
*Press esc to leave the data creation*

2. Training
  Once you have enough data:
  ```bash
  python training.py
  ```
  This reads the saved data (screenshots + key labels) and trains a neural network model.
  You might want to configure hyperparameters such as learning rate, batch size, number of epochs, etc., in the script (or via a config file if you add one).
  After training, the model will be saved (to a file or directory depending on your implementation).

3. Inference / Playing Mode
  To use the trained model to predict keys:
  ```
  python playing.py
  ```
  
  This starts capturing screenshots again, but instead of just logging key presses, it feeds the screenshot to the model.
  The model’s predicted keys are printed or pressed(Press Tab to switch modes).

## Project Structure
```
GameMaster/
├── create_data.py        # Script to collect screenshots + keyboard data  
├── training.py           # Script to train the neural network  
├── playing.py            # Script to run inference (predict keys)  
├── requirement.txt       # Dependencies  
└── [model files / data]  # Created automaticly to stores the model traning data
```
## Limitations

Keyboard only: This only supports keyboard input, not mouse or other devices.
Data size: Requires a potentially large dataset of screenshots + key presses to train a reliable model.
Generalization: If you train on a very specific game, the model may not generalize well to other games or screen layouts.
Performance: Training may be slow or resource-intensive, depending on your hardware.

## Future Improvements

- Add support for mouse input (or other devices)
- Implement a more advanced neural network architecture (e.g., convolutional neural networks, vision transformers)
- Use data augmentation on screenshots to improve generalization
- Add a GUI for data collection and inference
- Implement continuous learning (online training as you play)
- Add CI / tests, e.g., unit tests or integration tests

## Contributing

Contributions are very welcome! If you want to help:
1.Fork the repository
2.Create a feature branch (git checkout -b feature/my-feature)
3.Make your changes and commit (git commit -am 'Add some feature')
4.Push to your branch (git push origin feature/my-feature)
5.Open a Pull Request
Feel free to open issues if something is unclear or if you have suggestions.

## License
MIT License
