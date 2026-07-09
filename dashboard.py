import pandas as pd
import random
import time
from IPython.display import display, clear_output

patients = ["P001", "P002", "P003", "P004"]

while True:
    patient_data = []

    for patient in patients:
        heart_rate = random.randint(65, 140)
        movement_level = round(random.uniform(0.1, 4.0), 2)

        score = 0

        if heart_rate >= 120:
            score += 3
        elif heart_rate >= 100:
            score += 2

        if movement_level >= 3.0:
            score += 2
            movement_status = "Restless"
        elif movement_level <= 0.3:
            score += 1
            movement_status = "Very low movement"
        else:
            movement_status = "Normal"

        if score >= 5:
            status = "URGENT REASSESSMENT"
            action = "Prioritize immediately"
        elif score >= 3:
            status = "REVIEW SUGGESTED"
            action = "Nurse reassessment"
        else:
            status = "STABLE"
            action = "Continue monitoring"

        patient_data.append({
            "Patient ID": patient,
            "Heart Rate": f"{heart_rate} bpm",
            "Movement": movement_status,
            "Status": status,
            "Action": action
        })

    df = pd.DataFrame(patient_data)

    clear_output(wait=True)
    display(df)

    urgent = df[df["Status"] == "URGENT REASSESSMENT"]
    review = df[df["Status"] == "REVIEW SUGGESTED"]

    if not urgent.empty:
        print("URGENT: One or more patients need immediate reassessment.")
        display(urgent)
    elif not review.empty:
        print("WARNING: One or more patients should be reviewed.")
        display(review)
    else:
        print("All monitored patients are currently stable.")

    time.sleep(2)
