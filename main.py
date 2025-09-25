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


# # With GUI
# import tkinter as tk
# from tkinter import messagebox
# import cv2
# import face_recognition
# import os
# import pickle
# import numpy as np
# from utils import mark_attendance
# from datetime import datetime

# def start_attendance():
#     with open('encodings.p', 'rb') as f:
#         encodeListKnown, classNames = pickle.load(f)

#     cap = cv2.VideoCapture(0)
#     while True:
#         success, img = cap.read()
#         imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#         imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#         facesCurFrame = face_recognition.face_locations(imgS)
#         encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#         for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#             matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#             matchIndex = np.argmin(faceDis)

#             if matches[matchIndex]:
#                 name = classNames[matchIndex].upper()
#                 y1, x2, y2, x1 = [i * 4 for i in faceLoc]
#                 cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(img, name, (x1+6, y2+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#                 mark_attendance(name)

#         cv2.imshow('Face Attendance', img)
#         if cv2.waitKey(1) == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# def register_face():
#     name = entry_name.get()
#     if not name:
#         messagebox.showerror("Error", "Please enter a name")
#         return

#     cap = cv2.VideoCapture(0)
#     messagebox.showinfo("Info", "Press 's' to save image")
#     while True:
#         ret, frame = cap.read()
#         cv2.imshow("Register Face", frame)
#         if cv2.waitKey(1) & 0xFF == ord('s'):
#             cv2.imwrite(f"face_data/{name}.jpg", frame)
#             messagebox.showinfo("Saved", f"{name}.jpg saved!")
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# def re_encode_faces():
#     os.system('python encode_faces.py')
#     messagebox.showinfo("Info", "Encodings Updated!")

# # GUI window
# root = tk.Tk()
# root.title("Face Recognition Attendance")
# root.geometry("400x300")

# tk.Label(root, text="Enter Name:").pack(pady=5)
# entry_name = tk.Entry(root)
# entry_name.pack(pady=5)

# tk.Button(root, text="Register New Face", command=register_face).pack(pady=10)
# tk.Button(root, text="Re-Encode Faces", command=re_encode_faces).pack(pady=10)
# tk.Button(root, text="Start Attendance", command=start_attendance).pack(pady=10)
# tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

# root.mainloop()



# -------------------- GUI toolkit --------------------
import tkinter as tk   # Standard Python GUI package
from tkinter import messagebox, ttk  # Pop-up dialogs & themed widgets
import cv2  # OpenCV for image processing
import face_recognition # Library for face detection & recognition
import os # For file and folder operations
import pickle # For saving/loading Python objects in binary format
import numpy as np  # Numerical operations
import sqlite3  # SQLite database for attendance records
from datetime import datetime  # For timestamping attendance

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("attendance.db")  # Connect to SQLite database (or create it)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()

# ---------------- Face Recognition ----------------
def start_attendance():
    """
    Start webcam and recognize faces using encodings.p.
    If a known face is detected, mark attendance in the database.
    Press 'q' to close the camera window.
    """
    try:
        # Load encodings (list of faces + names)
        with open('encodings.p', 'rb') as f:
            encodeListKnown, classNames = pickle.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Encodings not found! Please encode faces first.")
        return

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)  # Resize for faster processing
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Detect faces & encode them
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            # Compare with known encodings
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)  # Best match

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = [i * 4 for i in faceLoc]   # Scale back coordinates
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)   # Draw rectangle
                cv2.putText(img, name, (x1+6, y2+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                mark_attendance(name)   # Save attendance in DB

        cv2.imshow('Face Attendance', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):   # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------- Register New Face ----------------
def register_face():
    """
    Capture a new user's face using webcam and save it to 'face_data' folder.
    File will be named as <name>.jpg.
    After saving, re-encode faces to update encodings.p automatically.
    """
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
            filepath = f"face_data/{name}.jpg"
            cv2.imwrite(filepath, frame)   # Save face image
            messagebox.showinfo("Saved", f"{filepath} saved!")
            break

    cap.release()
    cv2.destroyAllWindows()

    # Update encodings automatically after registering new face
    re_encode_faces()

# ---------------- Re-Encode Faces ----------------
def re_encode_faces():
    """
    Run encode_faces.py script to regenerate 'encodings.p'
    after adding new face images.
    """
    os.system('python encode_faces.py')
    messagebox.showinfo("Info", "Encodings Updated!")

# ---------------- Attendance Report ----------------
def view_report():
    report_win = tk.Toplevel(root)
    report_win.title("Attendance Report")
    report_win.geometry("500x400")


    # Create a table view
    tree = ttk.Treeview(report_win, columns=("ID", "Name", "Date", "Time"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.pack(fill=tk.BOTH, expand=True)


    # Fetch data from DB and insert into table
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance ORDER BY id DESC")
    rows = cur.fetchall( )
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close( )

# ---------------- GUI Window ----------------
root = tk.Tk( )
root.title("Face Recognition Attendance")
root.geometry("400x350")

# Input field for user name
tk.Label(root, text="Enter Name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)


# Buttons for different actions
tk.Button(root, text="Register New Face", command=register_face).pack(pady=10)
tk.Button(root, text="Re-Encode Faces", command=re_encode_faces).pack(pady=10)
tk.Button(root, text="Start Attendance", command=start_attendance).pack(pady=10)
tk.Button(root, text="View Attendance Report", command=view_report).pack(pady=10)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

# Initialize DB
init_db( )

root.mainloop( )