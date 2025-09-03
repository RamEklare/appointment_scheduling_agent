import pandas as pd
from datetime import datetime

def load_doctor_schedules(path="data/doctor_schedules.xlsx"):
    """Load doctor schedule from your Excel file."""
    return pd.read_excel(path)

def book_appointment(patients_df, doctor_schedules,
                     name, dob, doctor, location,
                     insurance_carrier, member_id, group):
    """Simple booking logic."""
    patient_type = "Returning" if name in patients_df['Name'].values else "New"
    slot_length = 60 if patient_type == "New" else 30
    # pick first available slot for the selected doctor
    slot = doctor_schedules[doctor_schedules['Doctor'] == doctor].iloc[0]['Next Available Slot']
    appointment = {
        "Name": name,
        "DOB": dob,
        "Doctor": doctor,
        "Location": location,
        "Patient Type": patient_type,
        "Slot Length (min)": slot_length,
        "Scheduled Time": slot,
        "Insurance Carrier": insurance_carrier,
        "Member ID": member_id,
        "Group": group,
        "Booked At": datetime.now().isoformat()
    }
    return appointment
