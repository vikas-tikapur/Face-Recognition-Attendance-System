import os
from datetime import datetime  # To get current date and time

# ---------------- Attendance Function ----------------
def mark_attendance(name):
    """
    Marks attendance of a person in 'attendance.csv'.
    If the CSV file does not exist, it creates one with headers: Name, Date, Time.
    Ensures the same name is not recorded multiple times in the file.
    """
    filename = 'attendance.csv'
    
    # Create the CSV file with headers if it does not exist
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Name,Date,Time\n')

    # Open the file in read+write mode
    with open(filename, 'r+') as f:
        myDataList = f.readlines()  # Read all existing lines
        # Extract the first column (names) to prevent duplicates
        name_list = [line.split(',')[0] for line in myDataList]
        
        # If the name is not already in the CSV, add a new entry
        if name not in name_list:
            now = datetime.now()
            date_string = now.strftime('%Y-%m-%d')   # Format: yyyy-mm-dd
            time_string = now.strftime('%H:%M:%S')   # Format: hh:mm:ss
            # Write new record to the file
            f.write(f'{name},{date_string},{time_string}\n')
            print(f'[INFO] Attendance marked for {name} on {date_string} at {time_string}')
