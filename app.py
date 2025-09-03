import streamlit as st
from services import db, scheduler, comm, exporter

st.set_page_config(page_title="Medical Appointment AI Agent", layout="wide")

st.title("🏥 Medical Appointment Scheduling AI Agent")

# --- Load your own data ---
patients_df = db.load_patients("C:/Users/HP/medical_scheduling_agent/patients_sample_50.csv")
doctor_schedules = scheduler.load_doctor_schedules("data/doctor_schedules_sample.xlsx")

# --- Booking form ---
st.subheader("Book Appointment")

name = st.text_input("Patient Name")
dob = st.date_input("Date of Birth")
doctor = st.selectbox("Doctor", doctor_schedules['doctor_name'].unique())
location = st.text_input("Location")
insurance_carrier = st.text_input("Insurance Carrier")
member_id = st.text_input("Member ID")
group = st.text_input("Group")

if st.button("Book Appointment"):
    appointment = scheduler.book_appointment(
        patients_df, doctor_schedules,
        name, dob, doctor, location,
        insurance_carrier, member_id, group
    )

    st.success(f"✅ Appointment booked with {doctor} at {appointment['Scheduled Time']}")

    # Send confirmation & reminders
    comm.send_confirmation(name, appointment)
    comm.schedule_reminders(name, appointment)

    # Export to Excel
    exporter.export_appointments([appointment])
    st.info("Exported appointment to Excel.")

    # Email intake form (stub)
    comm.email_form(name, "forms/Patient Intake Form.pdf")
