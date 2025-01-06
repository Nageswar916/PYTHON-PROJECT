import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import numpy as np

# Initialize video capture and hand detector
cap = cv2.VideoCapture(0)

# Set the desired frame width and height
frame_width = 1920  # Set your desired width
frame_height = 1080  # Set your desired height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
detector = HandDetector(detectionCon=0.8)
keyboard = Controller()

# Define keyboard layout
keyboard_keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                 ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                 ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                 ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
                 ["SP", "EN", "B"]]  # Adjusted button text

# Button class to represent each key
class Button:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.size = (80, 80)  # Size of each button

# Create button objects
button_list = []
for i, row in enumerate(keyboard_keys):
    for j, key in enumerate(row):
        x = j * 100 + 50  # X position
        y = i * 100 + 50  # Y position
        button_list.append(Button(key, (x, y)))

# Function to draw buttons
def draw_buttons(img, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (37, 238, 250), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    return img

# Variable to store the current text input
current_text = ""

# Main loop
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    
    # Draw buttons on the image
    img = draw_buttons(img, button_list)

    if hands:
        lmList = hands[0]['lmList']
        # Logic to detect which button is pressed based on finger positions
        index_finger_tip = lmList[8]  # Index finger tip landmark
        for button in button_list:
            x, y = button.pos
            w, h = button.size
            if x < index_finger_tip[0] < x + w and y < index_finger_tip[1] < y + h:
                cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (0, 255, 0), cv2.FILLED)  # Highlight button
                if cv2.waitKey(1) & 0xFF == 1:  # Check for a click (you can adjust this logic)
                    if button.text == "SP":  # Space button
                        current_text += " "
                        keyboard.press(" ")
                    elif button.text == "EN":  # Enter button
                        current_text += "\n"
                        keyboard.press("\n")
                    elif button.text == "B":  # Backspace button
                        current_text = current_text[:-1]  # Remove last character
                        keyboard.press("\b")
                    else:
                        current_text += button.text
                        keyboard.press(button.text)

    # Define the position and size of the text box
    text_box_y = 540  # Y position for the text box
    text_box_height = 100  # Height of the text box
    text_box_width = 800  # Width of the text box

    # Draw the rectangle for the text box
    cv2.rectangle(img, (50, text_box_y), (50 + text_box_width, text_box_y + text_box_height), (255, 255, 255), cv2.FILLED)  # Background for text box

    # Draw the current text input inside the text box
    cv2.putText(img, current_text, (60, text_box_y + 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)  # Display current text

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == 27:  # Exit on ESC key
        break

cap.release()
cv2.destroyAllWindows()