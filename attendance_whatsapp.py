import csv
import requests

# ===================================================
# 🔐 WHATSAPP CLOUD API DETAILS
# ===================================================

PHONE_NUMBER_ID = "992732720594958"
ACCESS_TOKEN = "EAAQ9TXFJyugBQySP22RlXzkMQzr1aeQSnMNijkeNTJ9uAbg6ZCMbVZCmudIZAOmy3sZBVOVuKSoUctGhE9BYwuodw5ZCobFOMWPHTzbg65PEyrJm6rMAkvGnGLeYdaeUzsmTn3J9ZBl4poT1iuEhpS4R5wdrKspnZCfZB7TSLpnPxmr5q4Mm4zHr7unP5oVqs59jgXM1RtZA4fKyZAu6cbuYJelqXXm4a50LsVRm9OZBdmIsKREqDsOl1ZAaI7i1P6CP81KF0I37NuXHBhAYse90HWCZB3doM"

# ===================================================
# 📲 FUNCTION TO SEND WHATSAPP MESSAGE
# ===================================================

def send_whatsapp_message(to_number, message):

    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Response:", response.json())


# ===================================================
# 📂 LOAD STUDENTS DATA (students.csv)
# ===================================================

def load_students(file_path):

    students = {}

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))

        # Proctor details (Row 2)
        proctor_name = reader[1][0]
        proctor_whatsapp = reader[1][1]

        # Student data starts from Row 5
        for row in reader[4:]:

            if len(row) < 4:
                continue

            roll = row[0].strip()

            students[roll] = {
                "name": row[1].strip(),
                "section": row[2].strip(),
                "parent_phone": row[3].strip(),
                "proctor_name": proctor_name,
                "proctor_whatsapp": proctor_whatsapp
            }

    return students


# ===================================================
# 📂 PROCESS ATTENDANCE (attendance.csv)
# ===================================================

def process_attendance(attendance_file, students):

    with open(attendance_file, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))

        # Date, Period, Proctor (Row 2)
        proctor_name = reader[1][0].strip()
        date=reader[1][1].strip()
        period=reader[1][2].strip()

        # Attendance data starts from Row 4
        for row in reader[3:]:

            if len(row) < 2:
                continue

            roll = row[0].strip()
            status = row[1].strip().upper()

            if status == "A" and roll in students:

                student = students[roll]

                message = f"""
Dear Parent,

Your child {student['name']} (Roll No: {roll})
Section: {student['section']}

was ABSENT on:
Date: {date}
Period: {period}

Proctor: {proctor_name}

Please ensure regular attendance.
"""

                print(f"Sending message to {student['parent_phone']}...")

                send_whatsapp_message(student["parent_phone"], message)


# ===================================================
# 🚀 MAIN PROGRAM
# ===================================================

if __name__ == "__main__":

    students = load_students("students.csv")
    process_attendance("attendance.csv", students)