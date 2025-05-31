'''# Without GUI

import cv2
import face_recognition
import numpy as np
import pickle
from datetime import datetime
import os
from utils import mark_attendance

# Load encodings
with open('encode_faces.py', 'rb') as f:
    pass  # Encodings are generated in a separate step

with open('encodings.p', 'rb') as f:
    encodeListKnown, classNames = pickle.load(f)

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = [i * 4 for i in faceLoc]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1+6, y2+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            mark_attendance(name)

    cv2.imshow('Face Attendance', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()'''


# With GUI
import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import os
import pickle
import numpy as np
from utils import mark_attendance
from datetime import datetime

def start_attendance():
    with open('encodings.p', 'rb') as f:
        encodeListKnown, classNames = pickle.load(f)

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = [i * 4 for i in faceLoc]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1+6, y2+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                mark_attendance(name)

        cv2.imshow('Face Attendance', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def register_face():
    name = entry_name.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name")
        return

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Press 's' to save image")
    while True:
        ret, frame = cap.read()
        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(f"face_data/{name}.jpg", frame)
            messagebox.showinfo("Saved", f"{name}.jpg saved!")
            break

    cap.release()
    cv2.destroyAllWindows()

def re_encode_faces():
    os.system('python encode_faces.py')
    messagebox.showinfo("Info", "Encodings Updated!")

# GUI window
root = tk.Tk()
root.title("Face Recognition Attendance")
root.geometry("400x300")

tk.Label(root, text="Enter Name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

tk.Button(root, text="📸 Register New Face", command=register_face).pack(pady=10)
tk.Button(root, text="🔁 Re-Encode Faces", command=re_encode_faces).pack(pady=10)
tk.Button(root, text="✅ Start Attendance", command=start_attendance).pack(pady=10)
tk.Button(root, text="❌ Exit", command=root.destroy).pack(pady=10)

root.mainloop()