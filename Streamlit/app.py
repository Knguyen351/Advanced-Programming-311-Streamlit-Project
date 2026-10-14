import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up the page.
st.set_page_config(page_title="311 Dashboard", layout="wide")
st.title("311 Service Request Dashboard")
st.write("Choose a date range to explore requests.")

# Read the CSV and convert request_date into dates.
df = pd.read_csv("311_2025_dashboard.csv")
df["request_date"] = pd.to_datetime(
    df["request_date"], errors="coerce"
).dt.date

# Remove rows that do not have a valid date.
df = df.dropna(subset=["request_date"])

# Find the available date range.
min_date = df["request_date"].min()
max_date = df["request_date"].max()

# Let the user choose dates.
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

# Stop if the selected dates are backward.
if start_date > end_date:
    st.error("Start date must be on or before end date.")
    st.stop()

# Filter the data using the selected dates.
filtered_df = df[
    (df["request_date"] >= start_date)
    & (df["request_date"] <= end_date)
].copy()

# Show summary numbers.
st.metric("Total requests", f"{len(filtered_df):,}")

# Stop if the selected period has no requests.
if filtered_df.empty:
    st.warning("No requests in this date range.")
    st.stop()

# Chart 1: Top request types.
st.subheader("Top 10 Request Types")

top_services = (
    filtered_df["service_name"]
    .value_counts()
    .head(10)
    .sort_values()
)

fig1, ax1 = plt.subplots(figsize=(10, 5))
top_services.plot.barh(ax=ax1, color="steelblue")
ax1.set_xlabel("Number of Requests")
ax1.set_ylabel("Service Type")
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

# Chart 2: Requests by agency.
st.subheader("Requests by Agency")

agency_counts = (
    filtered_df["agency_responsible"]
    .value_counts()
    .sort_values()
)

fig2, ax2 = plt.subplots(figsize=(10, 5))
agency_counts.plot.barh(ax=ax2, color="seagreen")
ax2.set_xlabel("Number of Requests")
ax2.set_ylabel("Agency")
fig2.tight_layout()

st.pyplot(fig2)
plt.close(fig2)