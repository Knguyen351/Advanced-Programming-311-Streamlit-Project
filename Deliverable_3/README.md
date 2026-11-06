# 311 Service Request Dashboard

## Project
A Streamlit dashboard analyzing 311 request records in a reduced dataset for **October 1–December 31, 2025**. The dashboard provides a weekday/service heatmap, a ranked service bar chart, and daily/weekly time trends.

## Dataset and source
- Deployed dataset: `dashboard_data.csv` (reduced dataset supplied for the course, with `request_date`, `service_name`, `day_of_week`, and other fields).
- **Original data publisher and source URL: TO BE CONFIRMED BY STUDENT.** Add the verified original dataset URL, attribution, and license/terms before submission. Do not claim a source without verifying it.
- Scope: October–December 2025 only. These are request records, not necessarily telephone calls. The file is a reduced extract, so avoid generalizing to all requests outside this time window.
- Privacy: includes ZIP codes and service categories but no obvious names, phone numbers, or street addresses. Confirm the data license and that the extract is approved for public release.

## Audience
Municipal service planners, public-sector analysts, and residents interested in patterns of demand for city services.

## Analysis questions
1. Which 311 service types are most frequent on each weekday?
2. What are the leading service categories for a chosen weekday, including when Information Request is excluded?
3. How does service demand change daily or weekly and by service category?

## Interactivity and metrics
- Shared global date range, and per-chart filters for Information Request, weekday, Top 5/10/15, service category, and daily/weekly grouping.
- Three dynamic metrics: total requests, busiest weekday, and top service category.
- Each chart provides a filter-responsive finding.

## Run locally
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Published dashboard
**Streamlit application URL: https://advanced-programming-311-app-project-9yckcubyk2srapxtihqy4r.streamlit.app/


## GitHub repository
**Public repository URL: ADD URL AFTER UPLOAD**

## AI-use statement
I used ChatGPT to assist with drafting and debugging Python and Streamlit code, charts, layout, and project documentation. I am responsible for selecting analysis questions, verifying data and findings, understanding the code, and testing the published application.

## Before submitting
- [ ] Confirm and cite the official dataset publisher, source URL, and applicable data license.
- [ ] Push `app.py`, `dashboard_data.csv`, `requirements.txt`, and `README.md` to a public repository.
- [ ] Deploy through Streamlit Community Cloud and replace URL placeholders.
- [ ] Test dates, every checkbox/dropdown, all three charts and metrics in a private/incognito browser session.
- [ ] Confirm no error messages or debug output.
