import os
import pandas as pd
from datetime import datetime

def generate_report(prompt: str, responses: dict):
    os.makedirs("data/comparision_reports", exist_ok=True)

    rows = []
    for model_name, response in responses.items():
        rows.append({
            "Model": model_name,
            "Response": response,
            "Prompt": prompt,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    df = pd.DataFrame(rows)
    df.to_csv("data/comparision_reports/report.csv", index=False)
    
    return "data/comparision_reports/report.csv"