from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="311 Dashboard", layout="wide")

st.title("311 Service Request Dashboard")
st.write(
    "Explore 2025 Philadelphia service requests by date and agency. "
    "All metrics and charts update with your selections."
)

# Load the CSV from the same folder as app.py.
data_path = Path(__file__).parent / "311_2025_dashboard.csv"
df = pd.read_csv(data_path, dtype={"zipcode": "string"})

# Convert dates and keep only 2025 records.
df["request_date"] = pd.to_datetime(
    df["request_date"], errors="coerce"
)
df = df[df["request_date"].dt.year == 2025].copy()
df["request_date"] = df["request_date"].dt.date

# Clean ZIP codes: remove .0 and exclude missing or invalid codes.
df["zipcode"] = (
    df["zipcode"]
    .str.strip()
    .str.replace(r"\.0$", "", regex=True)
)
df["zipcode"] = df["zipcode"].where(
    df["zipcode"].str.fullmatch(r"\d{5}", na=False)
)

if df.empty:
    st.error("The dataset contains no valid 2025 requests.")
    st.stop()

# Date controls.
min_date = df["request_date"].min()
max_date = df["request_date"].max()

st.sidebar.header("Filter Requests")

start_date = st.sidebar.date_input(
    "Start date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# Additional interactive control.
agencies = sorted(df["agency_responsible"].dropna().unique())

selected_agency = st.sidebar.selectbox(
    "Agency",
    ["All agencies"] + agencies
)

if start_date > end_date:
    st.error("Start date must be on or before end date.")
    st.stop()

# Apply the date filter.
filtered_df = df[
    (df["request_date"] >= start_date)
    & (df["request_date"] <= end_date)
].copy()

# Apply the agency filter.
if selected_agency != "All agencies":
    filtered_df = filtered_df[
        filtered_df["agency_responsible"] == selected_agency
    ].copy()

st.caption(
    f"Available data: {min_date:%b %d, %Y}–{max_date:%b %d, %Y}. "
    "This file covers October–December, not the full year."
)

# Three summary metrics.
col1, col2, col3 = st.columns(3)

col1.metric("Total requests", f"{len(filtered_df):,}")
col2.metric(
    "Service types",
    filtered_df["service_name"].nunique()
)
col3.metric(
    "Known ZIP codes",
    filtered_df["zipcode"].nunique()
)

st.caption(
    "Known ZIP codes counts distinct valid ZIP codes. "
    "Requests with missing ZIP codes remain in other metrics and charts."
)

if filtered_df.empty:
    st.warning("No requests match your selections.")
    st.stop()

# Chart 1.
st.subheader("Top 10 Request Types")

top_services = (
    filtered_df["service_name"]
    .value_counts()
    .head(10)
    .sort_values()
)

if top_services.empty:
    st.info("No service types are recorded for these requests.")
else:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    top_services.plot.barh(ax=ax1, color="steelblue")
    ax1.set_title("Top 10 Request Types")
    ax1.set_xlabel("Number of Requests")
    ax1.set_ylabel("Service Type")
    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

# Chart 2.
st.subheader("Requests by Agency")

agency_counts = (
    filtered_df["agency_responsible"]
    .value_counts()
    .sort_values()
)

if agency_counts.empty:
    st.info("No agencies are recorded for these requests.")
else:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    agency_counts.plot.barh(ax=ax2, color="seagreen")
    ax2.set_title("Requests by Agency")
    ax2.set_xlabel("Number of Requests")
    ax2.set_ylabel("Agency")
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# Chart 3: include zero-request days within the selected period.
st.subheader("Requests Over Time")

date_range = pd.date_range(start_date, end_date).date

requests_by_day = (
    filtered_df.groupby("request_date")
    .size()
    .reindex(date_range, fill_value=0)
)

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(
    pd.to_datetime(requests_by_day.index),
    requests_by_day.values,
    color="darkorange",
    marker=".",
    linewidth=1.5
)
ax3.set_title("Daily 311 Requests")
ax3.set_xlabel("Request Date")
ax3.set_ylabel("Number of Requests")
fig3.autofmt_xdate()
fig3.tight_layout()
st.pyplot(fig3)
plt.close(fig3)
