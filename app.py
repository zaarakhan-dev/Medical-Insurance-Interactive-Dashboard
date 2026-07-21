import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Medical Insurance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Medical Insurance Interactive Dashboard")

st.markdown(
"""
Explore the Medical Insurance dataset using interactive visualizations created with Plotly and Streamlit.
"""
)

df = pd.read_csv("insurance.csv")

st.sidebar.header("Filters")

selected_smoker = st.sidebar.multiselect(
    "Smoker",
    options=df["smoker"].unique(),
    default=df["smoker"].unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=df["sex"].unique(),
    default=df["sex"].unique()
)

selected_region = st.sidebar.multiselect(
    "Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

age_range = st.sidebar.slider(
    "Age",
    int(df["age"].min()),
    int(df["age"].max()),
    (
        int(df["age"].min()),
        int(df["age"].max())
    )
)

filtered_df = df[
    (df["smoker"].isin(selected_smoker)) &
    (df["sex"].isin(selected_gender)) &
    (df["region"].isin(selected_region)) &
    (df["age"] >= age_range[0]) &
    (df["age"] <= age_range[1])
]

st.write("Filtered Records:", filtered_df.shape[0])

st.sidebar.markdown("---")

st.sidebar.info("""
### About

This dashboard analyzes the Medical Insurance Dataset using interactive Plotly visualizations.

Created by:
**Zaara Khan**
""")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Records",
        len(filtered_df)
    )

with col2:
    st.metric(
        "💰 Avg Charge",
        f"${filtered_df['charges'].mean():,.0f}"
    )

with col3:
    st.metric(
        "🧍 Avg BMI",
        f"{filtered_df['bmi'].mean():.1f}"
    )

with col4:
    smokers = filtered_df[filtered_df["smoker"] == "yes"].shape[0]

    st.metric(
        "🚬 Smokers",
        smokers
    )

st.markdown("---")

st.markdown("### Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.success(f"Average Age: {filtered_df['age'].mean():.1f} years")

with col2:
    st.info(f"Maximum Charge: ${filtered_df['charges'].max():,.0f}")

with col3:
    st.warning(f"Minimum Charge: ${filtered_df['charges'].min():,.0f}")

st.markdown("---")

st.subheader("Insurance Charges Distribution")

fig = px.histogram(
    filtered_df,
    x="charges",
    nbins=30,
    color="smoker",
    title="Distribution of Insurance Charges"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Average Insurance Charges by Region")

region_avg = (
    filtered_df.groupby("region")["charges"]
    .mean()
    .reset_index()
)

fig = px.bar(
    region_avg,
    x="region",
    y="charges",
    color="region",
    title="Average Insurance Charges by Region",
    text_auto=".0f"
)

fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Relationship Between BMI and Insurance Charges")

fig = px.scatter(
    filtered_df,
    x="bmi",
    y="charges",
    color="smoker",
    size="age",
    hover_data=["age", "children", "region"],
    title="BMI vs Insurance Charges"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Average Insurance Charges by Age")

age_avg = (
    filtered_df.groupby("age")["charges"]
    .mean()
    .reset_index()
)

fig = px.line(
    age_avg,
    x="age",
    y="charges",
    markers=True,
    title="Average Insurance Charges by Age"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Smoker Distribution")

smoker_count = (
    filtered_df["smoker"]
    .value_counts()
    .reset_index()
)

smoker_count.columns = ["Smoker", "Count"]

fig = px.pie(
    smoker_count,
    names="Smoker",
    values="Count",
    title="Smoker vs Non-Smoker Distribution",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Insurance Charges by Region")

fig = px.box(
    filtered_df,
    x="region",
    y="charges",
    color="region",
    title="Distribution of Insurance Charges Across Regions"
)

st.plotly_chart(fig, use_container_width=True)  

st.markdown("---")

st.subheader("Correlation Heatmap")

corr_df = filtered_df.copy()

corr_df["sex"] = corr_df["sex"].map({"male": 1, "female": 0})
corr_df["smoker"] = corr_df["smoker"].map({"yes": 1, "no": 0})
corr_df["region"] = corr_df["region"].astype("category").cat.codes

corr = corr_df.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(8,6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax
)

st.pyplot(fig)

st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_insurance_data.csv",
    mime="text/csv"
)

st.markdown("---")

st.subheader("Filtered Dataset")

st.dataframe(filtered_df)

st.markdown("---")

st.caption(
    "Medical Insurance Dashboard | Built using Streamlit & Plotly | Summer Internship Project 2026"
)