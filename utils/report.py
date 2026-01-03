import pandas as pd
import os
from datetime import datetime

def generate_report(prompt:str,response:dict):
    os.makedirs("data/completions_reports", exist_ok=True)

    row = []
    for model,output in response.items():
        row.append({
            "model": model,
            "prompt": prompt,
            "Response": output,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })  