# -------------------------------------------
# STEP 1: IMPORT LIBRARIES
# -------------------------------------------
import pandas as pd
import numpy as np

# -------------------------------------------
# STEP 2: LOAD & CLEAN DATA
# -------------------------------------------
df = pd.read_csv("outputs/cleaned_combined_with_industry.csv", low_memory=False)

# Convert date to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Convert price columns to numeric (in case of issues)
price_cols = ['Open', 'High', 'Low', 'Close']
for col in price_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing prices or sector info
df.dropna(subset=price_cols + ['Sector', 'Industry', 'Firm'], inplace=True)

# Sort by firm and date
df.sort_values(by=['Firm', 'Date'], inplace=True)

# -------------------------------------------
# STEP 3: FEATURE ENGINEERING
# -------------------------------------------

# Daily Return
df['Daily_Return'] = df.groupby('Firm')['Close'].pct_change()

# Monthly Returns
df['Month'] = df['Date'].dt.to_period('M')
monthly_returns = df.groupby(['Firm', 'Month'])['Close'].last().pct_change().reset_index()
monthly_returns['Month'] = monthly_returns['Month'].astype(str)

# 30-Day Rolling Volatility
df['Rolling_Volatility_30d'] = df.groupby('Firm')['Daily_Return'].rolling(window=30).std().reset_index(0, drop=True)

# Max Drawdown Function
def calculate_max_drawdown(prices):
    roll_max = prices.cummax()
    drawdown = (prices - roll_max) / roll_max
    return drawdown.min()

# Max Drawdown per Firm
drawdowns = []
for firm, group in df.groupby('Firm'):
    mdd = calculate_max_drawdown(group['Close'])
    drawdowns.append({'Firm': firm, 'Max_Drawdown': mdd})
drawdown_df = pd.DataFrame(drawdowns).sort_values(by='Max_Drawdown')

# -------------------------------------------
# STEP 4: ANALYSIS FOR DASHBOARD
# -------------------------------------------

# Industry-Level Avg Close per Day (for line plots)
industry_avg_close = df.groupby(['Date', 'Industry'])['Close'].mean().unstack()

# Sector-Level Avg Return
df['Sector_Avg_Daily_Return'] = df.groupby(['Date', 'Sector'])['Daily_Return'].transform('mean')
sector_perf = df.groupby('Sector')['Daily_Return'].mean().sort_values(ascending=False)

# Industry-Level Avg Return
industry_perf = df.groupby('Industry')['Daily_Return'].mean().sort_values(ascending=False)

# Firm-Level Summary Stats
firm_summary = df.groupby('Firm').agg({
    'Daily_Return': ['mean', 'std'],
    'Rolling_Volatility_30d': 'mean',
    'Close': ['min', 'max', 'mean']
})
firm_summary.columns = ['_'.join(col).strip() for col in firm_summary.columns.values]
firm_summary.reset_index(inplace=True)

# Sector-Level Correlation Matrices
sector_corrs = {}
for sector, group in df.groupby('Sector'):
    # First, aggregate to daily mean return per firm to remove duplicates
    daily_returns = group.groupby(['Date', 'Firm'])['Daily_Return'].mean().reset_index()
    
    # Now pivot safely
    pivot = daily_returns.pivot(index='Date', columns='Firm', values='Daily_Return')
    
    # Compute correlation matrix
    sector_corrs[sector] = pivot.corr()

# Industry Top Performer Over Entire Period
industry_cum_return = df.groupby(['Firm', 'Industry']).agg({
    'Close': ['first', 'last']
})
industry_cum_return.columns = ['First_Close', 'Last_Close']
industry_cum_return['Total_Return'] = (industry_cum_return['Last_Close'] - industry_cum_return['First_Close']) / industry_cum_return['First_Close']
industry_perf_summary = industry_cum_return.groupby('Industry')['Total_Return'].mean().sort_values(ascending=False)

# -------------------------------------------
# STEP 5: SAVE OUTPUTS FOR DASHBOARD
# -------------------------------------------
df.to_csv("outputs/final_cleaned_data.csv", index=False)
monthly_returns.to_csv("outputs/monthly_returns.csv", index=False)
drawdown_df.to_csv("outputs/drawdowns.csv", index=False)
firm_summary.to_csv("outputs/firm_summary.csv", index=False)
industry_perf_summary.to_csv("outputs/industry_performance_summary.csv")
sector_perf.to_csv("outputs/sector_performance_summary.csv")

print("✅ CLEANING + ANALYSIS COMPLETE")
