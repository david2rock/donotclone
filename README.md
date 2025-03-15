# Gesture-Controlled PowerPoint Presentation

This project enables users to control PowerPoint presentations using hand gestures detected via a webcam. It leverages computer vision techniques to track hand movements and interpret gestures for actions like swiping slides, selecting tools (laser pointer, highlighter, eraser), and more.

## Features

- **Gesture Recognition**: Detects various hand gestures to perform actions.
  - Swipe left/right to navigate slides.
  - Use specific gestures to activate tools like laser pointer, highlighter, and eraser.
- **Smooth Mouse Movement**: Maps hand movements to screen coordinates for precise control.
- **Real-Time Feedback**: Displays the current gesture and tool mode on the screen.
- **PowerPoint Integration**: Automatically opens and controls PowerPoint presentations.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.7 or higher
- Required Python libraries:
  - `opencv-python`
  - `numpy`
  - `pyautogui`
  - `cvzone`
  - `psutil`
  - `rich`

You can install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository or download the project files.
2. Ensure your webcam is functional and connected to your system.
3. Open the project directory in your preferred Python IDE or terminal.

## Usage

1. Run the `main.py` script to start the application:

   ```bash
   python main.py
   ```

2. The application will open a webcam feed and display the detected hand gestures.
3. Use the following gestures to control the presentation:
   - **Thumb Up**: Move to the next slide.
   - **Pinky Up**: Move to the previous slide.
   - **Index Finger Up**: Activate laser pointer mode.
   - **Index and Middle Fingers Up**: Activate highlighter mode.
   - **Index, Middle, and Ring Fingers Up**: Activate eraser mode.
4. Press `q` to quit the application.

### Opening a PowerPoint Presentation

- If PowerPoint is not already open, the application will prompt you to enter the file path of the presentation.
- Ensure the file path is valid and points to a `.ppt` or `.pptx` file.

## Project Structure

```txt
GestureControledPPT/
├── main.py          # Main script for gesture detection and control
├── utils.py         # Utility functions for PowerPoint control and gesture actions
├── README.md        # Project documentation
```

## Acknowledgments

- **[cvzone](https://github.com/cvzone/cvzone)**: For simplifying computer vision tasks.
- **[OpenCV](https://opencv.org/)**: For image processing and webcam integration.
- **[pyautogui](https://pyautogui.readthedocs.io/)**: For automating mouse and keyboard actions.
- **[psutil](https://psutil.readthedocs.io/)**: For process management.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the license terms.
