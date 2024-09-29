import serial
import numpy as np
import cv2

# Setup serial connection (adjust the port as needed)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=10)

# Load OpenCV's pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
            # Convert the image to grayscale for face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Display the image with face detection
            cv2.imshow("ESP32-CAM Face Detection", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Failed to decode image")
    else:
        print("No image received")

ser.close()
cv2.destroyAllWindows()
