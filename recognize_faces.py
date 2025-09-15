import face_recognition  # Library for face detection & encoding
import cv2               # OpenCV for image processing & webcam
import pickle            # For loading saved encodings
import os                # For file operations
from datetime import datetime  # To save date and time of attendance

# ---------------- Attendance Function ----------------
def mark_attendance(name):
    """
    Save the attendance of a recognized person into a CSV file.
    If the CSV file does not exist, create it with headers: Name,Date,Time
    """
    filename = 'attendance.csv'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Name,Date,Time\n')  # CSV header

    with open(filename, 'r+') as f:
        myDataList = f.readlines()
        # Get list of already marked names to avoid duplicates
        name_list = [line.split(',')[0] for line in myDataList]
        if name not in name_list:
            now = datetime.now()
            date_string = now.strftime('%d-%m-%Y')  # Format: day-month-year
            time_string = now.strftime('%H:%M:%S')  # Format: hour:minute:second
            f.write(f'{name},{date_string},{time_string}\n')  # Append new record
            print(f'[INFO] Attendance marked for {name} on {date_string} at {time_string}')

# ---------------- Load Face Encodings ----------------
with open("encodings.p", "rb") as f:
    data = pickle.load(f)  # Load known face encodings and names

known_encodings = data["encodings"]
known_names = data["names"]

# ---------------- Open Webcam ----------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Capture frame from webcam
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for face_recognition

    # Detect faces in the current frame
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare current face with known encodings
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.45)
        name = "Unknown"

        # Find best match based on distance
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = face_distances.argmin()

        if matches[best_match_index]:
            name = known_names[best_match_index]

        # Draw rectangle around face and display name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        # Mark attendance for recognized faces only
        if name != "Unknown":
            mark_attendance(name)

    # Show webcam feed with annotations
    cv2.imshow("Face Recognition", frame)

    # Press 'q' to quit webcam
    if cv2.waitKey(1) == ord('q'):
        break

# Release webcam and close all windows
cap.release()
cv2.destroyAllWindows()