import serial
import numpy as np
import cv2

# Setup serial connection (adjust the port as needed)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=10)

def read_image_from_serial(ser):
    # Read the image size first
    image_size = int.from_bytes(ser.read(4), byteorder='little')
    print(f"Image size: {image_size} bytes")

    # Read the image data
    image_data = ser.read(image_size)
    if len(image_data) != image_size:
        print("Error reading image data")
        return None

    # Convert the image data into a numpy array for OpenCV processing
    image_np = np.frombuffer(image_data, dtype=np.uint8)
    return image_np

while True:
    # Capture the image
    image = read_image_from_serial(ser)

    if image is not None:
        # Decode the image using OpenCV
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)

        if img is not None:
            # Display the image
            cv2.imshow("ESP32-CAM", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Failed to decode image")
    else:
        print("No image received")

ser.close()
cv2.destroyAllWindows()
