import face_recognition
import cv2
import pickle
import os
from datetime import datetime

# STEP 1: Attendance function
def mark_attendance(name):
    filename = 'attendance.csv'
    
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Name,Time\n')

    # Check if name already marked
    with open(filename, 'r+') as f:
        myDataList = f.readlines()
        name_list = [line.split(',')[0] for line in myDataList]
        
        if name not in name_list:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'{name},{dtString}\n')
            print(f'[INFO] Attendance marked for {name} at {dtString}')

# STEP 2: Load encodings
with open("encodings.p", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

# STEP 3: Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.45)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = face_distances.argmin()

        if matches[best_match_index]:
            name = known_names[best_match_index]

        # Draw box and name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        # Mark attendance
        if name != "Unknown":
            mark_attendance(name)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
