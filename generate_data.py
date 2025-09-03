# generate_data.py
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta


fake = Faker()


# 1) generate 50 patients
patients = []
for i in range(50):
dob = fake.date_of_birth(minimum_age=1, maximum_age=90)
name = fake.name()
phone = fake.phone_number()
email = fake.free_email()
mrn = f"MRN{i+1000:06d}"
patients.append({
'mrn': mrn,
'name': name,
'dob': dob.isoformat(),
'phone': phone,
'email': email,
'primary_insurance': fake.company(),
'member_id': fake.bothify(text='??######'),
'is_returning': np.random.choice([0,1], p=[0.3,0.7])
})


patients_df = pd.DataFrame(patients)


# save
import os
os.makedirs('data', exist_ok=True)
patients_df.to_csv('data/patients.csv', index=False)


# 2) generate doctor schedules (Excel)
doctors = [
{'doctor_id': 'D001', 'name': 'Dr. A. Sharma', 'specialty':'Cardiology'},
{'doctor_id': 'D002', 'name': 'Dr. P. Mehta', 'specialty':'General Medicine'},
{'doctor_id': 'D003', 'name': 'Dr. S. Rao', 'specialty':'Dermatology'},
]


# make availability per doctor for next 14 days
sheets = {}
start = datetime.now().date()
for d in doctors:
rows = []
for day in range(14):
date = start + timedelta(days=day)
# assume slots 9:00-12:00 and 14:00-17:00 with 30-min granularity
for hour in [9,9.5,10,10.5,11,11.5,14,14.5,15,15.5,16,16.5]:
slot_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=float(hour))
rows.append({'date': date.isoformat(), 'slot': slot_time.isoformat(), 'available': 1})
sheets[d['name']] = pd.DataFrame(rows)


with pd.ExcelWriter('data/doctor_schedules.xlsx') as writer:
for name, df in sheets.items():
df.to_excel(writer, sheet_name=name[:31], index=False)


print('Generated data/patients.csv and data/doctor_schedules.xlsx')