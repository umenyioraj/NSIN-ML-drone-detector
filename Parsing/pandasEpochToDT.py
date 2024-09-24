import pandas as pd

input_csv = ""
output_csv = ""

# Read from csv where the datetimes are stored line by line in epoch time
df = pd.read_csv(input_csv)
df['DetectionTime'] = pd.to_datetime(df['DetectionTime'], unit='us', errors='coerce')
df.to_csv(output_csv, index=False)
