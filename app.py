"""
Project 6: Data Visualization Dashboard

Goal: Build an interactive dashboard to explore the Titanic dataset,
letting users filter data and see live-updating visualizations.

Run with: streamlit run app.py
"""

# ---------- STEP 0: Import Libraries ----------
import streamlit as st        # for the dashboard/web app framework
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px    # for interactive charts (better than static matplotlib for a dashboard)

# ---------- STEP 1: Page Configuration ----------
# Sets up the browser tab title, icon, and page layout
st.set_page_config(
    page_title="Titanic Dashboard",
    page_icon="🚢",
    layout="wide"   # uses the full browser width instead of a narrow column
)

# ---------- STEP 2: Data Collection & Cleaning ----------
@st.cache_data  # caches the data so it doesn't reload every time a filter changes
def load_data():
    df = sns.load_dataset("titanic")
    df["age"] = df["age"].fillna(df["age"].median())
    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])
    df = df.drop(columns=["deck"])
    df = df.dropna(subset=["embark_town"])
    return df

df = load_data()

# ---------- STEP 3: Dashboard Title ----------
st.title("🚢 Titanic Survival Dashboard")
st.markdown(
    "Interactive dashboard to explore survival patterns in the Titanic dataset. "
    "Use the filters in the sidebar to slice the data and watch the charts update live."
)

# ---------- STEP 4: Sidebar Filters (Interactivity) ----------
st.sidebar.header("🔍 Filters")

# Filter 1: Passenger class (multi-select)
selected_class = st.sidebar.multiselect(
    "Passenger Class",
    options=sorted(df["pclass"].unique()),
    default=sorted(df["pclass"].unique())
)

# Filter 2: Gender
selected_sex = st.sidebar.multiselect(
    "Gender",
    options=df["sex"].unique(),
    default=list(df["sex"].unique())
)

# Filter 3: Age range (slider)
age_range = st.sidebar.slider(
    "Age Range",
    min_value=int(df["age"].min()),
    max_value=int(df["age"].max()),
    value=(int(df["age"].min()), int(df["age"].max()))
)

# Apply all filters to create a filtered dataframe
filtered_df = df[
    (df["pclass"].isin(selected_class)) &
    (df["sex"].isin(selected_sex)) &
    (df["age"].between(age_range[0], age_range[1]))
]

st.sidebar.markdown(f"**Showing {len(filtered_df)} of {len(df)} passengers**")

# ---------- STEP 5: Key Metrics (KPI Cards) ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Passengers", len(filtered_df))

with col2:
    survival_rate = filtered_df["survived"].mean() * 100 if len(filtered_df) > 0 else 0
    st.metric("Survival Rate", f"{survival_rate:.1f}%")

with col3:
    avg_age = filtered_df["age"].mean() if len(filtered_df) > 0 else 0
    st.metric("Average Age", f"{avg_age:.1f} yrs")

with col4:
    avg_fare = filtered_df["fare"].mean() if len(filtered_df) > 0 else 0
    st.metric("Average Fare", f"${avg_fare:.2f}")

st.divider()

# ---------- STEP 6: Interactive Visualizations ----------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Survival by Gender")
    gender_survival = filtered_df.groupby(["sex", "survived"]).size().reset_index(name="count")
    gender_survival["survived"] = gender_survival["survived"].map({0: "No", 1: "Yes"})
    fig1 = px.bar(
        gender_survival, x="sex", y="count", color="survived",
        color_discrete_map={"No": "#E74C3C", "Yes": "#2ECC71"},
        barmode="group"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Survival Rate by Class")
    class_survival = filtered_df.groupby("pclass")["survived"].mean().reset_index()
    class_survival["survived"] = class_survival["survived"] * 100
    fig2 = px.bar(
        class_survival, x="pclass", y="survived",
        labels={"survived": "Survival Rate (%)", "pclass": "Passenger Class"},
        color="survived", color_continuous_scale="viridis"
    )
    st.plotly_chart(fig2, use_container_width=True)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Age Distribution")
    fig3 = px.histogram(
        filtered_df, x="age", nbins=30, color_discrete_sequence=["#4C9AFF"]
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("Fare vs Age (by Survival)")
    fig4 = px.scatter(
        filtered_df, x="age", y="fare", color="survived",
        color_continuous_scale=["#E74C3C", "#2ECC71"],
        labels={"survived": "Survived"}
    )
    st.plotly_chart(fig4, use_container_width=True)

# ---------- STEP 7: Data Table (Optional Detail View) ----------
st.divider()
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df[["pclass", "sex", "age", "fare", "survived", "embark_town"]])

# ---------- STEP 8: Footer ----------
st.divider()
st.caption("Built with Streamlit + Plotly | Jyesta Data Science Internship - Project 6")