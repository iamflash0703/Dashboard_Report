# 📊 Titanic Interactive Dashboard

An interactive data visualization dashboard built with Streamlit and Plotly to explore survival patterns in the Titanic dataset — with live filters and real-time updating charts. Part of Jyesta Data Science Internship.

## 🌐 Live Demo
[View Live Dashboard]()

## 📌 Overview
Unlike the previous static analysis projects, this dashboard lets users interactively filter the data (by class, gender, age) and see visualizations, KPI metrics, and a data table update in real time — similar to tools like Tableau or Power BI, built entirely in Python.

## 🛠️ Tools & Libraries
- Python
- Streamlit (dashboard framework)
- Plotly Express (interactive charts)
- Pandas, NumPy, Seaborn

## 🔍 Features
1. **Sidebar Filters** — Passenger Class, Gender (multi-select), Age Range (slider).
2. **KPI Metrics** — Total Passengers, Survival Rate, Average Age, Average Fare (live-updating).
3. **Interactive Charts** — Survival by Gender, Survival Rate by Class, Age Distribution, Fare vs Age (all built with Plotly for hover tooltips and zoom).
4. **Data Table** — Filtered dataset viewable in detail.
5. **Caching** — Uses `@st.cache_data` for fast performance on filter changes.

## 📁 Files
- `app.py` — full Streamlit dashboard code
- `requirements.txt` — dependencies for deployment

Browser will automatically open at `localhost:8501`.
