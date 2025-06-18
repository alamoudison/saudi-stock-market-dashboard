import pandas as pd
import os

# Correct file paths
BASE_DIR = r'C:\Users\user\saudi-stock-market-dashboard-main\outputs'
INPUT_CSV = os.path.join(BASE_DIR, 'final_cleaned_data.csv')
SECTOR_OUTPUT = os.path.join(BASE_DIR, 'correlation_by_sector.csv')
SUPER_SECTOR_OUTPUT = os.path.join(BASE_DIR, 'correlation_by_super_sector.csv')

def main():
    df = pd.read_csv(INPUT_CSV, parse_dates=['Date'])
    df = df.dropna(subset=['% Change'])

    # Pivot to get daily % Change per sector
    sector_pivot = df.groupby(['Date', 'Sector'])['% Change'].mean().unstack()
    sector_corr = sector_pivot.corr()
    sector_corr.to_csv(SECTOR_OUTPUT)

    # Pivot to get daily % Change per Super Sector
    super_sector_pivot = df.groupby(['Date', 'Super Sector'])['% Change'].mean().unstack()
    super_sector_corr = super_sector_pivot.corr()
    super_sector_corr.to_csv(SUPER_SECTOR_OUTPUT)

    print(f"✅ Correlation matrices saved to:\n- Sector: {SECTOR_OUTPUT}\n- Super Sector: {SUPER_SECTOR_OUTPUT}")

if __name__ == '__main__':
    main()
