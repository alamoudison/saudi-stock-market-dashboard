import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import base64
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Saudi Arabia Stock Dashboard", layout="wide")
pio.templates.default = "plotly_white"

# --- Helper: Image to Base64 ---
def img_to_base64(filename):
    with open(filename, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Load Assets ---
logo1 = img_to_base64("assets/my_logo.png")
logo2 = img_to_base64("assets/tadawul_logo.png")

# --- Load Custom CSS ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("assets/style.css")

# --- Header ---
st.markdown(
    f"""
    <div class='header'>
        <img src='data:image/png;base64,{logo1}' alt='Logo 1'>
        <div>
            <h1>Saudi Arabia Main Market Performance</h1>
            <p style='margin: 0; font-size: 18px; font-style:italic;'>by Abdulrahman Alamoudi</p>
        </div>
        <img src='data:image/png;base64,{logo2}' alt='Logo 2'>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Summary",
    "📈 Performance Charts",
    "📉 Volatility & Drawdowns",
    "🔗 Correlation",
    "🧾 Raw Data"
])

# =======================
# 📊 Tab 1: Summary
# =======================
with tab1:
    st.subheader("📊 Market Performance by Super Sector, Sector, and Firm")

    company_data = pd.read_csv("output/company_price_changes.csv")
    sector_data = pd.read_csv("output/sector_price_summary.csv")
    top_movers = pd.read_csv("output/top_movers.csv")
    bottom_movers = pd.read_csv("output/bottom_movers.csv")
    trend_data = pd.read_csv("output/price_trend_data.csv")
    trend_data["Date"] = pd.to_datetime(trend_data["Date"])

    # --- Super Sector Selectbox ---
    all_supers = sorted(trend_data["Super Sector"].dropna().unique())
    super_options = ["All Super Sectors"] + all_supers
    selected_super = st.selectbox("🧱 Select Super Sector (for Firm Filters)", super_options)

    # --- Sector filter (default to Materials & Energy if available) ---
    if selected_super != "All Super Sectors":
        sectors = trend_data[trend_data["Super Sector"] == selected_super]["Sector"].dropna().unique()
    else:
        sectors = trend_data["Sector"].dropna().unique()

    default_sectors = [s for s in ["Materials", "Energy"] if s in sectors]
    selected_sectors = st.multiselect("🏷️ Select Sector(s)", sorted(sectors), default=default_sectors)

    # --- Firm filter (default to the two firms if available) ---
    firms = trend_data[trend_data["Sector"].isin(selected_sectors)]["Firm"].dropna().unique()
    default_firms = [f for f in ["Saudi Aramco Base Oil Co.", "Saudi Arabian Oil Co.", "Arabian Drilling Co.","Saudi Arabia Refineries Co."] if f in firms]
    selected_firms = st.multiselect("🏢 Select Firm(s)", sorted(firms), default=default_firms)


    min_date = trend_data["Date"].min().date()
    max_date = trend_data["Date"].max().date()
    date_range = st.slider("📅 Select Date Range", min_value=min_date, max_value=max_date,
                           value=(min_date, max_date), format="YYYY-MM-DD")

    trend_filtered = trend_data[
        (trend_data["Sector"].isin(selected_sectors)) &
        (trend_data["Firm"].isin(selected_firms)) &
        (trend_data["Date"].dt.date >= date_range[0]) &
        (trend_data["Date"].dt.date <= date_range[1])
    ]

    view_mode = st.radio("🧭 View Mode", ["Grouped by Sector", "Top & Bottom Movers"], horizontal=True)

    st.markdown("### 📈 % Change Overview")
    if view_mode == "Grouped by Sector":
        filtered_company_data = company_data[company_data["Firm"].isin(selected_firms)]
        fig = px.bar(filtered_company_data, x="Firm", y="Pct_Change", color="Sector")
        fig.update_layout(
            title="% Change per Firm",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="black"),
            xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("#### 📋 Sector Summary Stats")
        st.dataframe(sector_data, use_container_width=True)
    else:
        st.markdown("#### 🔝 Top 5 Movers")
        st.dataframe(top_movers, use_container_width=True)
        fig_top = px.bar(top_movers, x="Firm", y="Pct_Change", color="Sector")
        fig_top.update_layout(
            title="Top 5 Gainers",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="black"),
            xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig_top, use_container_width=True)

        st.markdown("#### 🔻 Bottom 5 Movers")
        st.dataframe(bottom_movers, use_container_width=True)
        fig_bottom = px.bar(bottom_movers, x="Firm", y="Pct_Change", color="Sector")
        fig_bottom.update_layout(
            title="Bottom 5 Losers",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="black"),
            xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig_bottom, use_container_width=True)

    st.markdown("### 📉 Price Trend Over Time (Firm-Level)")
    fig_trend = px.line(trend_filtered, x="Date", y="Close", color="Firm")
    fig_trend.update_layout(
        title="Price Trend for Selected Firms",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="black"),
        xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=10)
            )
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("### 🧱📅 Price Trend by Super Sector or Sector")
    trend_level = st.radio("Select Aggregation Level", ["Super Sector", "Sector"], horizontal=True)

    if trend_level == "Super Sector":
        trend_filtered_super = trend_data[(trend_data["Date"].dt.date >= date_range[0]) &
                                          (trend_data["Date"].dt.date <= date_range[1])]
        super_avg = trend_filtered_super.groupby(["Date", "Super Sector"], as_index=False)["Close"].mean()
        fig_super = px.line(super_avg, x="Date", y="Close", color="Super Sector")
        fig_super.update_layout(
            title="Average Price Trend by Super Sector",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="black"),
            xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig_super, use_container_width=True)
    else:
        trend_filtered_sec = trend_data[(trend_data["Date"].dt.date >= date_range[0]) &
                                        (trend_data["Date"].dt.date <= date_range[1])]
        sector_avg = trend_filtered_sec.groupby(["Date", "Sector"], as_index=False)["Close"].mean()
        fig_sec = px.line(sector_avg, x="Date", y="Close", color="Sector")
        fig_sec.update_layout(
            title="Average Price Trend by Sector",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="black"),
            xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig_sec, use_container_width=True)

# =======================
# 📈 Tab 2: Performance Charts
# =======================
with tab2:
    st.subheader("📈 Detailed Performance Charts")
    performance_data = pd.read_csv("output/price_trend_data.csv")
    performance_data["Date"] = pd.to_datetime(performance_data["Date"])
    firms = performance_data["Firm"].dropna().unique()
    selected_firms_perf = st.multiselect("🏢 Select Firm(s) to Compare", sorted(firms), default=list(firms[:2]))

    fig_perf = px.line(performance_data[performance_data["Firm"].isin(selected_firms_perf)],
                       x="Date", y="Close", color="Firm")
    fig_perf.update_layout(
        title="Stock Price Comparison",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="black"),
        xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.5,
            title=None,
            font=dict(size=10)
        )
    )
    st.plotly_chart(fig_perf, use_container_width=True)

# =======================
# 📉 Tab 3: Volatility & Drawdowns
# =======================
with tab3:
    st.subheader("📉 Volatility & Drawdown Analysis")
    volatility_data = performance_data.copy()
    volatility_data.set_index("Date", inplace=True)

    for firm in selected_firms_perf:
        firm_data = volatility_data[volatility_data["Firm"] == firm]["Close"]
        returns = firm_data.pct_change().dropna()
        drawdown = (firm_data / firm_data.cummax()) - 1
        fig_dd = px.area(drawdown, title=f"{firm} Drawdown", labels={"value": "Drawdown"})
        fig_dd.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="black"),
            xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=10)
            )
        )
        st.markdown(f"### 📉 {firm} Volatility & Drawdown")
        st.line_chart(returns, height=150, use_container_width=True)
        st.plotly_chart(fig_dd, use_container_width=True)

# =======================
# 🔗 Tab 4: Correlation
# =======================
with tab4:
    st.subheader("🔗 Correlation Analysis")
    corr_sector = pd.read_csv("outputs/correlation_by_sector.csv", index_col=0)
    corr_super = pd.read_csv("outputs/correlation_by_super_sector.csv", index_col=0)

    corr_type = st.radio("Select Correlation Type", ["Sector", "Super Sector"], horizontal=True)

    if corr_type == "Sector":
        st.markdown("### 🔗 Sector-Level Correlation Matrix")
        data_to_plot = corr_sector
        title = "Sector Return Correlation Matrix"
    else:
        st.markdown("### 🔗 Super Sector-Level Correlation Matrix")
        data_to_plot = corr_super
        title = "Super Sector Return Correlation Matrix"

    fig, ax = plt.subplots(figsize=(14, 10))
    sns.set(style="whitegrid")
    heatmap = sns.heatmap(
        data_to_plot,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        center=0,
        linewidths=0.7,
        linecolor="#E0E0E0",
        cbar_kws={"shrink": 0.75}
    )
    ax.set_title(title, fontsize=18, weight="bold", pad=15, color='black')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    st.pyplot(fig)

# =======================
# 🧾 Tab 5: Raw Data
# =======================
with tab5:
    st.subheader("🧾 Explore Raw Data")
    file_map = {
        "Company Price Changes": "output/company_price_changes.csv",
        "Sector Summary": "output/sector_price_summary.csv",
        "Top Movers": "output/top_movers.csv",
        "Bottom Movers": "output/bottom_movers.csv",
        "Trend Data": "output/price_trend_data.csv"
    }

    selected_file = st.selectbox("Select Dataset to View", list(file_map.keys()))
    df_raw = pd.read_csv(file_map[selected_file])
    st.dataframe(df_raw, use_container_width=True)
    st.download_button("📥 Download CSV", df_raw.to_csv(index=False), file_name=selected_file.replace(" ", "_") + ".csv")
