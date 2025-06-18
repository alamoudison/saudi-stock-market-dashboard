import pandas as pd
import os

# Load the file
df = pd.read_csv("outputs/final_cleaned_data.csv")

# Combine mis-split sector and firm into one string for correction
def fix_sector_firm(row):
    combined = f"{row['Sector']},{row['Firm']}"
    # Remove extra spaces around comma, and fix & spacing
    combined = combined.replace(" ,", ",").replace(", ", ",")
    combined = combined.replace("&_", "& ").replace("_", " ").strip()

    # Now split into proper sector and firm
    if "_" in combined:
        # fallback if still bad
        return pd.Series([row['Sector'], row['Firm']])

    parts = combined.split(",", 1)
    if len(parts) == 2:
        sector = parts[0].strip()
        firm = parts[1].strip()
        return pd.Series([sector, firm])
    else:
        return pd.Series([row['Sector'], row['Firm']])

# Apply the cleaning to Sector and Firm
df[['Sector', 'Firm']] = df.apply(fix_sector_firm, axis=1)

# Fix the Super Sector header name
df.rename(columns={"Industry": "Super Sector"}, inplace=True)

# Save back to CSV
df.to_csv("outputs/final_cleaned_data.csv", index=False)
