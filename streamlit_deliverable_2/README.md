# 311 Streamlit Dashboard

Converted from `Notebook_2_Prototype_311_Dashboard_KevinNguyen10-28-26.ipynb`.

## Features
- Date range filter (shared across all 3 charts)
- Interactive heatmap (Top 10 service types by weekday, optional exclusion of Information Request)
- Top 5/10/15 services (weekday selection and exclusion filter)
- Daily/weekly request trend line (service selection and exclusion filter)

## Run locally
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy to Streamlit Community Cloud
Upload `app.py`, `requirements.txt`, and `311_2025_dashboard.csv` to the root of a GitHub repository. In Streamlit Community Cloud select `app.py` as the main file.

The dashboard includes the 3 *custom interactive* notebook charts. The two original sample charts were intentionally omitted.
