import cv2
import mediapipe as mp
import numpy as np
import serial
import time
import sys

# Setup serial communication with Arduino
ser = serial.Serial('COM16', 9600)  # Replace 'COM16' with your Arduino's port
time.sleep(2)  # Wait for Arduino to initialize

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define button properties (arranged horizontally)
buttons = [
    {"label": "L1(ON)", "color": (0, 255, 0), "position": (50, 50), "command": 'G'},
    {"label": "L2(ON)", "color": (0, 0, 255), "position": (300, 50), "command": 'B'},
    {"label": "L3(ON)", "color": (255, 0, 0), "position": (550, 50), "command": 'L'},
    {"label": "L4(ON)", "color": (0, 255, 255), "position": (800, 50), "command": 'Y'},
    {"label": "S(ON)", "color": (0, 0, 255), "position": (1050, 50), "command": 'R'},
    {"label": "L1(OFF)", "color": (128, 255, 255), "position": (50, 200), "command": 'S'},
    {"label": "L2(OFF)", "color": (0, 0, 0), "position": (300, 200), "command": 'K'},
    {"label": "L3(OFF)", "color": (0, 165, 255), "position": (550, 200), "command": 'O'},
    {"label": "L4(OFF)", "color": (128, 0, 128), "position": (800, 200), "command": 'P'},
    {"label": "S(OFF)", "color": (255, 255, 0), "position": (1050, 200), "command": 'C'}
]

# Function to draw buttons
def draw_buttons(frame):
    for button in buttons:
        cv2.rectangle(frame, button["position"], (button["position"][0] + 200, button["position"][1] + 100), button["color"], -1)
        cv2.putText(frame, button["label"], (button["position"][0] + 50, button["position"][1] + 65), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# Function to check if hand is over a button
def check_button_hover(x, y):
    for button in buttons:
        x1, y1 = button["position"]
        x2, y2 = x1 + 200, y1 + 100
        if x1 < x < x2 and y1 < y < y2:
            return button["command"]
    return None

# OpenCV loop to display buttons and detect hand gestures
cap = cv2.VideoCapture(0)

# Set the desired frame width and height
frame_width = 1280  # Set your desired width
frame_height = 720   # Set your desired height
cap.set(3, frame_width)  # Set width
cap.set(4, frame_height)  # Set height

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        draw_buttons(frame)

        # Convert the frame to RGB for mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the index finger tip
                x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
                y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])

                # Check if the index finger tip is over a button
                command = check_button_hover(x, y)
                if command:
                    ser.write(command.encode())
                    time.sleep(0.5)  # Add a small delay to prevent multiple triggers

                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Virtual Buttons", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Clean up resources
cap.release()
cv2.destroyAllWindows()
ser.close()

# Exit the script cleanly
sys.exit(0)