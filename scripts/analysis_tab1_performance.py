import pandas as pd
import os

# Load and clean data
df = pd.read_csv("outputs/final_cleaned_data.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Drop rows with missing values in key columns
df = df.dropna(subset=['Super Sector', 'Sector', 'Firm', 'Close'])

# ---- Filters ----
start_date = pd.to_datetime("2020-01-01")
end_date = pd.to_datetime("2025-05-31")

# Filter only by date (no filtering by Super Sector/firms)
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# ==== 1. % Price Change Per Firm ====
firm_pct_change = (
    filtered_df.sort_values('Date')
    .groupby(['Firm', 'Sector', 'Super Sector'])
    .agg(
        Start_Price=('Close', lambda x: x.iloc[0]),
        End_Price=('Close', lambda x: x.iloc[-1])
    )
    .reset_index()
)

firm_pct_change['Pct_Change'] = (
    (firm_pct_change['End_Price'] - firm_pct_change['Start_Price']) /
    firm_pct_change['Start_Price']
) * 100

# ==== 2. Sector-Level Summary ====
sector_summary = (
    firm_pct_change
    .groupby('Sector')
    .agg(
        Mean_Change=('Pct_Change', 'mean'),
        Median_Change=('Pct_Change', 'median'),
        Std_Dev=('Pct_Change', 'std'),
        Num_Firms=('Pct_Change', 'count')
    )
    .reset_index()
)

# ==== 3. Top & Bottom Movers ====
top_movers = firm_pct_change.sort_values(by='Pct_Change', ascending=False).head(5)
bottom_movers = firm_pct_change.sort_values(by='Pct_Change').head(5)

# ==== 4. Price Trend Data ====
# Use all firms in the filtered data
selected_firms = firm_pct_change['Firm'].unique().tolist()
trend_data = filtered_df[filtered_df['Firm'].isin(selected_firms)]

# ==== Save results ====
os.makedirs("output", exist_ok=True)

firm_pct_change.to_csv("output/company_price_changes.csv", index=False)
sector_summary.to_csv("output/sector_price_summary.csv", index=False)
top_movers.to_csv("output/top_movers.csv", index=False)
bottom_movers.to_csv("output/bottom_movers.csv", index=False)
trend_data.to_csv("output/price_trend_data.csv", index=False)

print("✅ Analysis complete. Results saved to /output/")
