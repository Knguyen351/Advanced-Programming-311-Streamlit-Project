from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="2025 311 Dashboard", layout="wide")
st.title("2025 311 Service Requests Dashboard")

# Place the CSV file in the same folder as app.py.
DATA_FILE = Path(__file__).parent / "311_2025_dashboard(1).csv"
DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_FILE)
    data["request_date"] = pd.to_datetime(data["request_date"], errors="coerce")
    return data.dropna(subset=["request_date"])


if not DATA_FILE.exists():
    st.error(f"CSV not found: {DATA_FILE.name}. Put it in the same folder as app.py.")
    st.stop()

df = load_data()
first_date = df["request_date"].min().date()
last_date = df["request_date"].max().date()

# Interactive controls replace START_DATE and END_DATE.
st.sidebar.header("Filters")
start_date = st.sidebar.date_input(
    "Start date", value=first_date, min_value=first_date, max_value=last_date
)
end_date = st.sidebar.date_input(
    "End date", value=last_date, min_value=first_date, max_value=last_date
)
selected_day = st.sidebar.selectbox("Show service types for", ["All Days"] + DAYS)
top_n = st.sidebar.selectbox("Number of top services", [5, 10, 15], index=1)

if start_date > end_date:
    st.error("Start date must be on or before end date.")
    st.stop()

filtered_df = df[
    df["request_date"].dt.date.between(start_date, end_date)
].copy()

st.write(f"**Selected period:** {start_date} through {end_date}")
st.metric("Requests in selected period", f"{len(filtered_df):,}")

if filtered_df.empty:
    st.warning("No requests match these dates.")
    st.stop()

# Chart 1: How many requests were received on each weekday?
st.subheader("1. Requests by Day of Week")
weekday_counts = filtered_df["day_of_week"].value_counts().reindex(DAYS, fill_value=0)
fig1, ax1 = plt.subplots(figsize=(9, 4))
bars1 = ax1.bar(weekday_counts.index, weekday_counts.values, color="steelblue")
ax1.bar_label(bars1, padding=3, fontsize=9)
ax1.set_ylabel("Number of requests")
ax1.set_ylim(0, max(weekday_counts.max() * 1.15, 1))
ax1.tick_params(axis="x", rotation=25)
fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

# Chart 2: Top service types for all days or one selected weekday.
st.subheader(f"2. Top {top_n} Service Types — {selected_day}")
service_df = filtered_df
if selected_day != "All Days":
    service_df = filtered_df[filtered_df["day_of_week"] == selected_day]

service_counts = service_df["service_name"].value_counts()
if service_counts.empty:
    st.info("No service requests match the selected weekday and date range.")
else:
    st.write(
        f"**Most requested service:** {service_counts.index[0]} "
        f"({service_counts.iloc[0]:,} requests)"
    )
    top_services = service_counts.head(top_n).sort_values()
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    bars2 = ax2.barh(top_services.index, top_services.values, color="steelblue")
    ax2.bar_label(bars2, padding=3, fontsize=9)
    ax2.set_xlabel("Number of requests")
    ax2.set_xlim(0, max(top_services.max() * 1.18, 1))
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

st.caption("Source: reduced 2025 311 service requests dataset")
