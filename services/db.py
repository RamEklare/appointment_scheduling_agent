import pandas as pd

def load_patients(path="C:/Users/HP/medical_scheduling_agent/data/patients_sample_50.csv"):
    """Load patient data from your CSV."""
    return pd.read_csv(path)
