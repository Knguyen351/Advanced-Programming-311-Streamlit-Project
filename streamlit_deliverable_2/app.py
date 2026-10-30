"""311 dashboard converted from the October 28 notebook."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="311 Requests Dashboard", page_icon="📊", layout="wide")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DATA_FILE = Path(__file__).with_name("311_2025_dashboard.csv")

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_FILE)
    data["request_date"] = pd.to_datetime(data["request_date"], errors="coerce").dt.normalize()
    data = data.dropna(subset=["request_date"]).copy()
    data["service_name"] = data["service_name"].fillna("Unknown").astype(str)
    data["day_of_week"] = data["request_date"].dt.day_name()
    return data

def apply_info_filter(data, exclude_info):
    if exclude_info:
        return data.loc[
            data["service_name"].str.strip().str.casefold() != "information request"
        ].copy()
    return data

def filter_dates(data, date_from, date_to):
    return data.loc[data["request_date"].between(pd.Timestamp(date_from), pd.Timestamp(date_to))].copy()

try:
    df = load_data()
except (OSError, pd.errors.ParserError) as exc:
    st.error(f"Unable to load 311_2025_dashboard.csv: {exc}")
    st.stop()

if df.empty:
    st.error("The dataset has no valid request dates.")
    st.stop()

st.title("📊 311 Requests Dashboard")
st.caption("Interactive dashboard adapted from Notebook 2 — 2025 reduced 311 dataset")

first_date = df["request_date"].min().date()
last_date = df["request_date"].max().date()

st.sidebar.header("Date range")
start = st.sidebar.date_input("Start date", value=first_date, min_value=first_date, max_value=last_date)
end = st.sidebar.date_input("End date", value=last_date, min_value=first_date, max_value=last_date)

if start > end:
    st.error("Start date must be on or before end date.")
    st.stop()

filtered_df = filter_dates(df, start, end)
st.caption(f"Showing requests from {start} through {end} (inclusive)")

if filtered_df.empty:
    st.warning("No requests in this date range. Choose other dates.")
    st.stop()

k1, k2, k3 = st.columns(3)
k1.metric("Requests in selected period", f"{len(filtered_df):,}")
k2.metric("Most common request", filtered_df["service_name"].value_counts().idxmax())
k3.metric("Days selected", f"{(end-start).days + 1:,}")

heat_tab, services_tab, trends_tab = st.tabs([
    "1 · Service heatmap", "2 · Top service requests", "3 · Request trends"
])

with heat_tab:
    st.subheader("Top 10 service request types by weekday")
    heat_exclude = st.checkbox("Exclude Information Request", value=False, key="heat_exclude")
    heat_data = apply_info_filter(filtered_df, heat_exclude)
    if heat_data.empty:
        st.info("No requests match these filters.")
    else:
        top_10 = heat_data["service_name"].value_counts().head(10).index
        heatmap_data = pd.crosstab(heat_data["service_name"], heat_data["day_of_week"])
        heatmap_data = heatmap_data.reindex(index=top_10, columns=DAYS, fill_value=0)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="Blues", linewidths=0.5, ax=ax)
        ax.set_title("Top 10 Types of 311 Requests by Day of Week")
        ax.set_xlabel("Day of Week")
        ax.set_ylabel("Service Type")
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption(f"Requests after filters: {len(heat_data):,}. A darker cell means more requests.")

with services_tab:
    st.subheader("Explore the most requested 311 services")
    c1, c2, c3 = st.columns(3)
    weekday = c1.selectbox("Select day", ["All Days"] + DAYS)
    top_n = c2.selectbox("Top requests", [5, 10, 15], index=1)
    service_exclude = c3.checkbox("Exclude Information Request", value=False, key="service_exclude")
    service_data = apply_info_filter(filtered_df, service_exclude)
    if weekday != "All Days":
        service_data = service_data[service_data["day_of_week"] == weekday]
    counts = service_data["service_name"].value_counts()
    if counts.empty:
        st.info("No requests match these filters.")
    else:
        st.write(f"**Total requests:** {len(service_data):,}  |  **Most requested service:** {counts.idxmax()} ({counts.max():,})")
        top_services = counts.head(top_n).sort_values()
        fig, ax = plt.subplots(figsize=(10, max(4, len(top_services) * 0.55)))
        bars = ax.barh(top_services.index, top_services.values, color="skyblue", edgecolor="black")
        ax.bar_label(bars, padding=3)
        ax.set_title(f"Top {top_n} Service Requests — {weekday}")
        ax.set_xlabel("Number of Requests")
        ax.set_ylabel("Service Type")
        ax.set_xlim(0, max(top_services.max() * 1.2, 1))
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

with trends_tab:
    st.subheader("311 request volume over time")
    t1, t2, t3 = st.columns(3)
    service_options = ["All Services"] + sorted(filtered_df["service_name"].unique().tolist())
    selected_service = t1.selectbox("Service type", service_options)
    view_by = t2.selectbox("View by", ["Daily", "Weekly"], index=1)
    trend_exclude = t3.checkbox("Exclude Information Request", value=False, key="trend_exclude")
    trend_data = apply_info_filter(filtered_df, trend_exclude)
    if selected_service != "All Services":
        trend_data = trend_data[trend_data["service_name"] == selected_service]
    if trend_data.empty:
        st.info("No requests match these filters. Choose another service type or turn off the exclusion.")
    else:
        all_dates = pd.date_range(start, end, freq="D")
        daily_counts = trend_data.groupby("request_date").size().reindex(all_dates, fill_value=0)
        trend = daily_counts.resample("W-SUN").sum() if view_by == "Weekly" else daily_counts
        label = "week" if view_by == "Weekly" else "day"
        st.write(f"**Total requests:** {len(trend_data):,}  |  **Average per {label}:** {trend.mean():,.1f}")
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(trend.index, trend.values, marker="o", color="royalblue", linewidth=2)
        ax.set_title(f"311 Request Trends — {selected_service}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Requests")
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        if view_by == "Weekly":
            st.caption("Weeks end on Sunday; edge weeks can include fewer than 7 selected days.")

st.divider()
st.caption("Source: reduced 2025 311 request dataset. Counts represent records, not necessarily telephone calls.")
