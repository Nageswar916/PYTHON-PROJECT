import cv2
import face_recognition
import numpy as np

# Load the known face image and encode it
known_image = face_recognition.load_image_file("known_person.jpg")  # Replace with your image file
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# To capture video from webcam. 
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    ret, img = cap.read()
    if not ret:
        print("Error reading frame")
        break

    # Resize the frame to 1/4 size for faster processing
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # Convert BGR to RGB

    # Only process every other frame to save time
    if process_this_frame:
        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Compare the face encoding with the known face encoding
            matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
            name = "Unknown"

            # If a match was found, set the name to the known person's name
            if True in matches:
                name = "Known Person"  # Replace with the actual name of the person

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Draw rectangles around recognized faces
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.putText(img, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        # Save the image if the recognized person is found
        if name == "Known Person":
            cv2.imwrite("captured_face.jpg", img[top:bottom, left:right])  # Save the face image

    # Display the resulting image
    cv2.imshow('Video', img)

    # Stop if escape key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()