import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CodeAlpha Task 3 - Data Visualization", layout="wide")
st.title("📊 Task 3 — Data Visualization Dashboard")
st.caption("Turn raw data into clear charts and a small decision-support dashboard.")

def demo():
    rng=np.random.default_rng(11)
    dates=pd.date_range("2026-01-01",periods=120,freq="D")
    rows=[]
    regions=["North","South","East","West"]
    for day in dates:
        for r in regions:
            sales=max(0,int(rng.normal(2500,500)))
            orders=max(1,int(rng.normal(70,15)))
            rows.append([day,r,sales,orders])
    return pd.DataFrame(rows,columns=["date","region","sales","orders"])

up=st.sidebar.file_uploader("Upload CSV",type=["csv"])
df=pd.read_csv(up) if up else demo()
st.sidebar.info("The app automatically detects numeric columns and date-like columns.")

# detect date column
date_col=None
for c in df.columns:
    parsed=pd.to_datetime(df[c],errors="coerce")
    if parsed.notna().mean()>=0.7:
        date_col=c; df[c]=parsed; break

num_cols=df.select_dtypes(include=np.number).columns.tolist()
cat_cols=df.select_dtypes(include=["object","category"]).columns.tolist()

if not num_cols:
    st.error("The dataset needs at least one numeric column for the dashboard.")
    st.stop()

metric=st.sidebar.selectbox("Main metric",num_cols)
category=st.sidebar.selectbox("Category (optional)",["None"]+cat_cols)
st.metric(f"Total {metric}",f"{df[metric].sum():,.2f}")

if date_col:
    st.subheader("📈 Trend over time")
    daily=df.groupby(date_col,as_index=False)[metric].sum()
    fig,ax=plt.subplots()
    ax.plot(daily[date_col],daily[metric])
    ax.set_title(f"{metric} over time"); ax.set_xlabel("Date"); ax.set_ylabel(metric)
    fig.autofmt_xdate(); st.pyplot(fig)

if category!="None":
    st.subheader("🏆 Category comparison")
    grp=df.groupby(category)[metric].sum().sort_values(ascending=False)
    fig,ax=plt.subplots()
    ax.bar(grp.index.astype(str),grp.values)
    ax.set_title(f"{metric} by {category}"); ax.set_ylabel(metric)
    ax.tick_params(axis="x",rotation=30); st.pyplot(fig)

st.subheader("📦 Distribution")
fig,ax=plt.subplots()
ax.hist(df[metric].dropna(),bins=20)
ax.set_title(f"Distribution of {metric}"); ax.set_xlabel(metric); ax.set_ylabel("Frequency")
st.pyplot(fig)

if len(num_cols)>=2:
    st.subheader("🔗 Numeric relationship")
    y=st.selectbox("Compare with", [c for c in num_cols if c!=metric])
    fig,ax=plt.subplots()
    ax.scatter(df[metric],df[y],alpha=.6)
    ax.set_xlabel(metric); ax.set_ylabel(y); ax.set_title(f"{metric} vs {y}")
    st.pyplot(fig)

st.subheader("💡 Data story")
st.write(f"The dashboard focuses on **{metric}** and converts raw records into trend, comparison, distribution and relationship views. These visuals help a decision-maker see changes, high-performing categories and unusual values quickly.")
