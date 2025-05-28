import os
import pandas as pd

# Absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Root of the project
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

# Build absolute paths
input_path = os.path.join(project_root, "data", "data.csv")
output_path = os.path.join(project_root, "data", "data_fixed.csv")

# Load, clean, export
df = pd.read_csv(input_path, encoding="ISO-8859-1")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M')
df.to_csv(output_path, index=False)