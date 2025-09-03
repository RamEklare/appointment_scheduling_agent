import pandas as pd
from pathlib import Path

def export_appointments(appointments, path="data/appointments_export.xlsx"):
    Path("data").mkdir(exist_ok=True)
    df = pd.DataFrame(appointments)
    df.to_excel(path, index=False)
