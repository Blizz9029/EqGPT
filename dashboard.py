
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Watchlist - SC - Yearly.csv")
    df.columns = df.iloc[0]  # Set second row as header
    df = df.drop(index=0).reset_index(drop=True)
    return df

df = load_data()

st.title("📊 Stock Watchlist Dashboard")

# --- Sidebar filters ---
st.sidebar.header("🔍 Filter Companies")

industry_filter = st.sidebar.multiselect("Select Industry", options=df["Industry"].unique())
min_pe, max_pe = st.sidebar.slider("P/E Ratio Range", 0, 100, (0, 50))
min_roe = st.sidebar.slider("Minimum RoE %", 0, 100, 10)

# --- Filter data ---
def preprocess_column(col):
    return pd.to_numeric(df[col].str.replace(',', '').str.strip(), errors='coerce')

df["PE"] = preprocess_column("PE")
df["RoE %"] = preprocess_column("RoE %")

filtered_df = df[
    (df["PE"] >= min_pe) & 
    (df["PE"] <= max_pe) & 
    (df["RoE %"] >= min_roe)
]

if industry_filter:
    filtered_df = filtered_df[filtered_df["Industry"].isin(industry_filter)]

# --- Show filtered data ---
st.subheader("📋 Filtered Company Data")
st.dataframe(filtered_df)

# --- Company level details ---
st.subheader("📈 Company Insights")
company = st.selectbox("Select a Company", options=filtered_df["Name"].unique())

company_data = filtered_df[filtered_df["Name"] == company].iloc[0]

st.markdown(f"### {company}")
st.write("**Industry**:", company_data["Industry"])
st.write("**Current Price**:", company_data["Current Price"])
st.write("**P/E Ratio**:", company_data["PE"])
st.write("**RoE %**:", company_data["RoE %"])

# --- Plot Return Trends ---
years = ["Return over 1year", "Return over 3years", "Return over 5years", "Return over 7years", "Return over 10years"]
returns = [pd.to_numeric(company_data[y], errors='coerce') for y in years]

fig, ax = plt.subplots()
ax.plot(years, returns, marker='o')
ax.set_title("Return Trend Over Years")
ax.set_ylabel("Return %")
st.pyplot(fig)
