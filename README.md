
# ESP32-CAM Face Detection

This project demonstrates real-time face detection using an **ESP32-CAM** module for image capture and a computer for image processing using **OpenCV**. The system captures images from the ESP32-CAM, sends them over a serial connection (via USB), and processes the images on the computer to detect faces in real time.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Hardware Setup](#hardware-setup)
3. [ESP32-CAM Firmware Setup](#esp32-cam-firmware-setup)
4. [Computer-Side Setup](#computer-side-setup)
5. [Running the Project](#running-the-project)
6. [Real-Time Operation](#real-time-operation)
7. [Troubleshooting](#troubleshooting)

---

## Project Structure

```
esp32-cam-face-detection/
│
├── esp32/
│   ├── camera_firmware/       # ESP32 camera firmware and code for capturing and sending images
│       ├── include/           # Header files (camera settings, ESP32 libraries)
│       ├── src/               # Source code for ESP32 image capture and USB communication
│       │   └── main.cpp       # ESP32-CAM firmware code to capture and send images via serial
│       └── platformio.ini     # PlatformIO configuration file for ESP32 development 
│
├── computer/
│   ├── face_detection/        # Python face detection code using OpenCV
│       ├── src/               # Source code for real-time image processing and display
│       │   ├── esp32_image_capture.py   # Script to capture and display images from ESP32
│       │   └── esp32_face_detection.py  # Main script for face detection using OpenCV
│       ├── tests/             # Unit tests for the face detection logic
│       └── requirements.txt   # Dependencies (if not using Nix)
│
├── nix/
│   ├── flake.nix              # NixOS Flake configuration for dependency management
│   ├── shell.nix              # Shell environment configuration for OpenCV and related libraries
│   └── default.nix            # Default Nix expression for running the project
│
└── README.md                  # Main project README file with setup and usage instructions

```

## Hardware Setup

### Components

- **ESP32-CAM**: A microcontroller with a built-in camera.
- **FTDI Adapter**: Used to upload firmware to the ESP32-CAM and enable communication via USB.
- **USB Cable**: Connects the FTDI adapter to the computer.

### Wiring

1. **FTDI Adapter to ESP32-CAM Connections**:
   - **VCC (3.3V)** → **ESP32-CAM 3.3V**
   - **GND** → **ESP32-CAM GND**
   - **TX** → **ESP32-CAM U0R**
   - **RX** → **ESP32-CAM U0T**
   - **GND (IO0)** → **ESP32-CAM GND** (for flashing mode)

2. Ensure the FTDI adapter is in **3.3V mode**.

---

## ESP32-CAM Firmware Setup

### 1. Install PlatformIO

1. Install [**PlatformIO IDE**](https://platformio.org/) in VSCode or use the CLI version.
2. Clone this repository and open the `esp32/camera_firmware/` folder in VSCode.

### 2. Configure PlatformIO

In the `esp32/camera_firmware/platformio.ini`, ensure the following configuration:

```ini
[env:esp32cam]
platform = espressif32
board = esp32cam
framework = arduino
upload_speed = 921600
monitor_speed = 115200
lib_deps =
    esp32-camera
upload_port = /dev/ttyUSB0  # Adjust this for your system (e.g., COMx for Windows)
```

### 3. Flash the Firmware

1. Press the **reset button** on the ESP32-CAM while holding **GND (IO0)** to put it into flashing mode.
2. In VSCode, select **PlatformIO: Upload** or use the following command:

   ```bash
   platformio run --target upload
   ```

3. After flashing, remove the GND connection from IO0 and open the serial monitor:

   ```bash
   platformio device monitor
   ```

You should see data being sent from the ESP32-CAM over serial.

---

## Computer-Side Setup

### 1. Install NixOS (with Flakes)

This project uses **NixOS** for dependency management, ensuring consistent environment setup. Install NixOS with flake support:

```bash
nix-env -iA nixos.nixFlakes
```

### 2. Set Up Environment Using Nix Flakes

To enter the Nix environment with all required dependencies (Python, OpenCV, pySerial), run:

```bash
nix develop
```

Alternatively, if you're not using Nix, you can install the dependencies with pip:

```bash
pip install -r computer/face_detection/requirements.txt
```

### 3. Python Code Overview

- **`esp32_image_capture.py`**: Captures images from the ESP32-CAM and displays them.
- **`esp32_face_detection.py`**: Captures images and performs real-time face detection using OpenCV.
- **`utils.py`**: Contains helper functions for serial communication and image decoding.

---

## Running the Project

### 1. Ensure ESP32-CAM is Running

Verify that the ESP32-CAM is sending data via the serial port by opening the serial monitor:

```bash
platformio device monitor
```

### 2. Run Face Detection on the Computer

Start the Python script for real-time face detection:

```bash
python computer/face_detection/src/esp32_face_detection.py
```

This script will display a video feed with rectangles around detected faces. Press **'q'** to exit the video feed.

---

## Real-Time Operation

### Optimizing Real-Time Performance

1. **Resolution**: Use lower image resolutions such as QVGA (320x240) for faster performance.
2. **Baud Rate**: Set a higher baud rate (921600) for faster serial communication.
3. **Frame Rate**: Limit the frame rate on the computer-side to avoid overloading the system.
4. **Face Detection**: Adjust the `scaleFactor` and `minNeighbors` parameters in OpenCV's `detectMultiScale()` function to optimize detection speed.

### Performance Tuning Example

In `esp32_face_detection.py`, adjust face detection parameters:

```python
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,     # Increase for faster but less accurate detection
    minNeighbors=5,      # Lower for more detections
    minSize=(30, 30)     # Set the minimum face size
)
```

---

## Troubleshooting

### Common Issues

1. **Serial Port Not Found**:
   - Ensure the correct serial port is selected in the `platformio.ini` file and Python script.
   - Use `dmesg | grep tty` to verify the correct serial port on Linux.

2. **Camera Initialization Failed**:
   - Double-check the wiring between the FTDI adapter and ESP32-CAM.
   - Ensure the camera module is not damaged.

3. **No Image Display**:
   - Verify that images are being received from the ESP32-CAM in the serial monitor.
   - Ensure the Python script is reading and decoding the image data properly.
