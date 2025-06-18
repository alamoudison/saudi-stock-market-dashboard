import pandas as pd

# Load the CSV
df = pd.read_csv("outputs/final_cleaned_data.csv")

# Define known bad sector,firm patterns and how to fix them
fix_map = {
    'Food,& Beverages': ('Food & Beverages',),
    'Capital,Goods': ('Capital Goods',),
    'Commercial,& Professional': ('Commercial & Professional',),
    'Consumer,Durables & Apparel': ('Consumer Durables & Apparel',),
    'Consumer,Services': ('Consumer Services',),
    'Media,and Entertainment': ('Media and Entertainment',),
    'Consumer,Discretionary Distribution & Retail': ('Consumer Discretionary Distribution & Retail',),
    'Consumer,Staples Distribution & Retail': ('Consumer Staples Distribution & Retail',),
    'Household,& Personal Products': ('Household & Personal Products',),
    'Health,Care Equipment & Svc': ('Health Care Equipment & Svc',),
    'Pharma,Biotech & Life Science': ('Pharma Biotech & Life Science',),
    'Financial,Services': ('Financial Services',),
    'Software,& Services': ('Software & Services',),
    'Telecommunication,Services': ('Telecommunication Services',)
}

# Clean Sector and Firm by correcting misplaced commas
def fix_sector_firm(row):
    sector = row['Sector']
    firm = row['Firm']
    combo = f"{sector},{firm}"

    for wrong, fixed in fix_map.items():
        if combo.startswith(wrong):
            new_sector = fixed[0]
            new_firm = combo[len(wrong)+1:].strip()
            return pd.Series([new_sector, new_firm])
    return pd.Series([sector, firm])

# Apply fixes
df[['Sector', 'Firm']] = df.apply(fix_sector_firm, axis=1)

# Save back to CSV
df.to_csv("outputs/final_cleaned_data.csv", index=False)
