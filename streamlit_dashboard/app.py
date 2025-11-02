import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Stroke Risk Dashboard", page_icon="🧠", layout="wide")

# DB connection (cached) ----------------------------------------------------------------------------------------------------------------------------
@st.cache_resource
def get_engine():
    pg = st.secrets["postgres"]
    url = f"postgresql+psycopg2://{pg['user']}:{pg['password']}@{pg['host']}:{pg['port']}/{pg['database']}"
    return create_engine(url, pool_pre_ping=True)

# Query data (cached to 5 mins) ----------------------------------------------------------------------------------------------------------------------
@st.cache_data(ttl=300)  # 5-min cache
def load_data():
    q = text("""
        SELECT *
        FROM stroke_data_processed
    """)
    with get_engine().connect() as conn:
        df = pd.read_sql(q, conn)
    # Standardise column names 
    df.columns = [c.lower().strip() for c in df.columns]
    return df

st.title("Stroke Risk Dashboard")
st.caption("Live data from AWS RDS (PostgreSQL) • Built with Streamlit")

# Load
df = load_data()
if df.empty:
    st.warning("No data found. Check the table `stroke_data_processed`.")
    st.stop()

# Sidebar filters ------------------------------------------------------------------------------------------------------------------------------------
with st.sidebar:
    st.header("Filters")
    gender = st.multiselect("gender", sorted(df["gender"].dropna().unique().tolist()))
    work = st.multiselect("Work type", sorted(df["work_type"].dropna().unique().tolist())) if "work_type" in df.columns else []
    smoking = st.multiselect("Smoking status", sorted(df["smoking_status"].dropna().unique().tolist())) if "smoking_status" in df.columns else []
    age_range = st.slider("Age range", 0, int(df["age"].max()), (0, int(df["age"].max())))

# Apply filters
f = df.copy()
if gender:       f = f[f["gender"].isin(gender)]
if work:      f = f[f["work_type"].isin(work)]
if smoking:   f = f[f["smoking_status"].isin(smoking)]
f = f[(f["age"] >= age_range[0]) & (f["age"] <= age_range[1])]

# KPIs ----------------------------------------------------------------------------------------------------------------------------------------------
total = len(f)
stroke_rate = f["stroke"].mean() if "stroke" in f.columns else 0
avg_glucose = f["avg_glucose_level"].mean() if "avg_glucose_level" in f.columns else None
avg_bmi = f["bmi"].mean() if "bmi" in f.columns else None

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows (after filters)", f"{total:,}")
col2.metric("Stroke rate", f"{stroke_rate*100:0.2f}%")
if avg_glucose is not None: col3.metric("Avg. glucose", f"{avg_glucose:0.1f}")
if avg_bmi is not None:     col4.metric("Avg. BMI", f"{avg_bmi:0.1f}")

# Charts  ------------------------------------------------------------------------------------------------------------------------------------------
import plotly.express as px

tab1, tab2, tab3 = st.tabs(["Distributions", "Risk by Factor", "Correlation"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        if "age" in f.columns:
            st.plotly_chart(px.histogram(f, x="age", nbins=30, title="Age distribution"), use_container_width=True)
    with c2:
        if "bmi" in f.columns:
            st.plotly_chart(px.histogram(f, x="bmi", nbins=30, title="BMI distribution"), use_container_width=True)

with tab2:
    if "stroke" in f.columns:
        # stroke by smoking status
        if "smoking_status" in f.columns:
            grp = f.groupby("smoking_status", dropna=False)["stroke"].mean().reset_index()
            st.plotly_chart(px.bar(grp, x="smoking_status", y="stroke", title="Stroke rate by Smoking status",
                                   labels={"stroke":"stroke rate"}), use_container_width=True)
        # stroke vs glucose (scatter)
        if {"avg_glucose_level","stroke"}.issubset(f.columns):
            st.plotly_chart(px.scatter(f, x="avg_glucose_level", y="age", color="stroke",
                                       title="Glucose vs Age (colored by stroke)"),
                            use_container_width=True)

with tab3:
    numeric_cols = f.select_dtypes("number")
    if not numeric_cols.empty:
        corr = numeric_cols.corr(numeric_only=True)
        st.dataframe(corr.style.background_gradient(cmap="RdBu", axis=None), use_container_width=True)
    else:
        st.info("No numeric columns to show correlation.")

# Data table ----------------------------------------------------------------------------------------------------------------------------------------------
st.subheader("Data (sample)")
st.dataframe(f.head(50), use_container_width=True)
