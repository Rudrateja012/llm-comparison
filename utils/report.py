import pandas as pd
import os
from datetime import datetime

def generate_report(prompt:str,response:dict):
    os.makedirs("data/completions_reports", exist_ok=True)
    