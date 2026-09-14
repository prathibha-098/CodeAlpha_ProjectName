import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="CodeAlpha Task 2 - EDA", layout="wide")
st.title("🔎 Task 2 — Exploratory Data Analysis")
st.caption("Upload a CSV and explore structure, quality, statistics, trends and anomalies.")

def demo_data():
    rng=np.random.default_rng(7)
    n=250
    age=rng.integers(18,70,n)
    income=np.clip(rng.normal(55000,15000,n),15000,120000)
    spend=np.clip(rng.normal(2500,900,n),200,7000)
    score=np.clip(rng.normal(650,70,n),350,850)
    df=pd.DataFrame({"age":age,"annual_income":income.round(0),"monthly_spend":spend.round(2),"credit_score":score.round(0)})
    df.loc[[10,80],"monthly_spend"]=np.nan
    df.loc[30,"annual_income"]=180000
    return df

uploaded=st.sidebar.file_uploader("Upload CSV", type=["csv"])
df=pd.read_csv(uploaded) if uploaded else demo_data()
st.sidebar.write("Using:", "uploaded dataset" if uploaded else "built-in demo dataset")

st.subheader("1. Meaningful questions")
st.markdown("- What variables and data types are present?\n- Are there missing or duplicate records?\n- What are the central tendencies and spread?\n- Which values look unusual?\n- What relationships or trends exist?")

c1,c2,c3,c4=st.columns(4)
c1.metric("Rows", df.shape[0]); c2.metric("Columns", df.shape[1])
c3.metric("Missing cells", int(df.isna().sum().sum()))
c4.metric("Duplicate rows", int(df.duplicated().sum()))

tab1,tab2,tab3,tab4=st.tabs(["📋 Structure","📊 Statistics","⚠️ Data Quality","📈 Relationships"])
with tab1:
    info=pd.DataFrame({"column":df.columns,"dtype":[str(x) for x in df.dtypes],"non_null":[int(x) for x in df.notna().sum()],"unique":[int(x) for x in df.nunique()]})
    st.dataframe(info,use_container_width=True)
    st.dataframe(df.head(20),use_container_width=True)
with tab2:
    st.dataframe(df.describe(include="all").T,use_container_width=True)
with tab3:
    miss=df.isna().sum().sort_values(ascending=False)
    st.write("Missing values by column")
    st.dataframe(miss.rename("missing").to_frame(),use_container_width=True)
    num=df.select_dtypes(include=np.number)
    if not num.empty:
        st.write("Potential outliers using the IQR rule")
        out=[]
        for col in num.columns:
            q1,q3=num[col].quantile([.25,.75]); iqr=q3-q1
            count=int(((num[col]<q1-1.5*iqr)|(num[col]>q3+1.5*iqr)).sum())
            out.append({"column":col,"outlier_count":count})
        st.dataframe(pd.DataFrame(out),use_container_width=True)
with tab4:
    nums=df.select_dtypes(include=np.number)
    if len(nums.columns)>=2:
        col1,col2=st.columns(2)
        x=col1.selectbox("X variable",nums.columns,index=0)
        y=col2.selectbox("Y variable",nums.columns,index=1)
        fig,ax=plt.subplots()
        ax.scatter(df[x],df[y],alpha=.65)
        ax.set_xlabel(x); ax.set_ylabel(y); ax.set_title(f"{x} vs {y}")
        st.pyplot(fig)
        st.write("Correlation:", round(df[x].corr(df[y]),3))
    else:
        st.warning("Upload a dataset with at least two numeric columns for the relationship plot.")

st.subheader("Conclusion")
st.write("Use the tables and plots above to identify patterns, anomalies, missing data and relationships before making business decisions.")
