# Hand Gesture Calculator

A real-time hand gesture-controlled calculator that uses computer vision to detect hand movements and translate them into calculator operations.

## Features

- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand detection and landmark tracking
- **Gesture Recognition**: Recognizes 13 different gestures for calculator control
- **Visual Feedback**: Live camera feed with hand landmarks, calculator display, and gesture indicators
- **Calculation History**: Keeps track of recent calculations

## Gesture Controls

| Gesture          | Operation | Description                                |
| ---------------- | --------- | ------------------------------------------ |
| 0 fingers (fist) | 0         | Closed fist                                |
| 1 finger         | 1 or /    | Point up for division, otherwise 1         |
| 2 fingers        | 2 or \*   | Peace sign for multiplication, otherwise 2 |
| 3 fingers        | 3         | Three fingers raised                       |
| 4 fingers        | 4         | Four fingers raised                        |
| 5 fingers        | 5 or =    | Flat palm for equals, otherwise 5          |
| Thumbs up        | +         | Addition                                   |
| Thumbs down      | -         | Subtraction                                |
| Peace sign       | \*        | Multiplication                             |
| Point up         | /         | Division                                   |
| Flat palm        | =         | Equals (calculate result)                  |
| Hold fist 1s     | C         | Clear calculator                           |

## Installation

1. Clone the repository:

```bash
git clone https://github.com/xggarcia/HandCalculator
cd HandCalculator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main application:

```bash
python main.py
```

**Controls:**

- Show gestures in front of your webcam to input numbers and operations
- Press `q` or `ESC` to quit the application

## Requirements

- Python 3.7 or higher
- Webcam
- OpenCV 4.8.1.78
- MediaPipe 0.10.8
- NumPy 1.24.3

## Project Structure

```
HandCalculator/
├── main.py                 # Main application entry point
├── hand_tracker.py         # Hand tracking using MediaPipe
├── gesture_recognizer.py   # Gesture recognition logic
├── calculator.py           # Calculator state and operations
├── ui_renderer.py          # UI rendering and display
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── LICENSE                # License information
```

## How It Works

1. **Hand Tracking**: The application uses MediaPipe Hands to detect and track 21 hand landmarks in real-time
2. **Gesture Recognition**: Analyzes finger positions and configurations to identify gestures
3. **Calculator Logic**: Processes recognized gestures and performs arithmetic operations
4. **UI Rendering**: Displays the camera feed with overlaid hand landmarks, calculator display, and visual feedback

## Tips for Best Results

- Ensure good lighting conditions
- Keep your hand within the camera frame
- Make clear, distinct gestures
- Wait for gesture confirmation (1-second debounce between gestures)
- Position yourself 1-2 feet from the camera

## Troubleshooting

- **Camera not opening**: Check if another application is using the webcam
- **Poor gesture detection**: Adjust lighting and ensure clear background
- **Lag or slow performance**: Close other resource-intensive applications

## License

See [LICENSE](LICENSE) file for details.

## Author

Created as a demonstration of computer vision and gesture recognition technology.
