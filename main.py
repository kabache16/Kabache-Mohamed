import cv2
from PIL import Image
import serial
from util import get_limits

# Define colors to detect
colors = {'yellow': [0, 255, 255],  # yellow in BGR colorspace
          'green': [0, 255, 0],  # green in BGR colorspace
          'red': [0, 0, 255],  # red in BGR colorspace
          'blue': [255, 0, 0]}  # blue in BGR colorspace

# Set up serial communication with Arduino
ser = serial.Serial('COM6', 9600)


ser.flushInput()

# Open camera
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()

    # Convert frame to HSV colorspace
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Loop through each color and detect its presence in the frame
    for color, bgr in colors.items():
        lowerLimit, upperLimit = get_limits(color=bgr)
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()

        # If the color is present, draw a rectangle around it and get its coordinates and dimensions
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 5)

            # Get the dimensions of the rectangle
            width = x2 - x1
            height = y2 - y1

            # Send the values to the Arduino board
            message = f"{x1},{y1},{width},{height}\n"  # add a newline character at the end
            ser.write(message.encode())

    # Show the frame
    cv2.imshow('frame', frame)

    # Check for exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
