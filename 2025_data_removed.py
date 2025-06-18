import pandas as pd

# Load the main data source
df = pd.read_csv("output/final_cleaned_data.csv")

# Ensure Date column is in datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Filter out all rows where the year is 2025
df = df[df["Date"].dt.year != 2025]

# Save the cleaned data back
df.to_csv("output/final_cleaned_data.csv", index=False)

print("✅ 2025 data removed and saved to output/final_cleaned_data.csv.")
