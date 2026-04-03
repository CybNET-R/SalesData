import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Retail Insights 2024", layout="wide")

# 2. Load and Prepare Data
@st.cache_data
def load_data():
    df = pd.read_csv("Online Sales Data.csv")
    # Clean column names
    df.columns = df.columns.str.strip()
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Month_Num'] = df['Date'].dt.month
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Dashboard")
regions = st.sidebar.multiselect("Select Region:", options=df["Region"].unique(), default=df["Region"].unique())
categories = st.sidebar.multiselect("Select Category:", options=df["Product Category"].unique(), default=df["Product Category"].unique())

# Filter the dataframe based on selection
mask = (df["Region"].isin(regions)) & (df["Product Category"].isin(categories))
filtered_df = df[mask]

# 4. Main Interface
st.title("📦 Online Sales Marketplace: 2024 Performance")

# Executive Summary
with st.expander("Read Executive Summary"):
    st.write("""
    This analysis covers sales from January 1, 2024, to August 19, 2024. 
    The marketplace sells across Electronics, Home Appliances, Clothing, Books, 
    Beauty, and Sports. Operating in North America, Europe, and Asia, 
    most customers pay via Credit Card, PayPal, or Debit Card. 
    """)

# KPI Metrics
total_rev = filtered_df["Total Revenue"].sum()
total_units = filtered_df["Units Sold"].sum()
aov = total_rev / total_units if total_units > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"${total_rev:,.2f}")
c2.metric("Total Units Sold", f"{total_units:,}")
c3.metric("Avg Order Value", f"${aov:,.2f}")

# 5. Visualizations
st.subheader("Market Share & Payment Splits")
col1, col2, col3 = st.columns(3)

with col1:
    fig_pay = px.pie(filtered_df, names="Payment Method", values="Total Revenue", title="Revenue by Payment Method")
    st.plotly_chart(fig_pay, use_container_width=True)

with col2:
    fig_reg = px.pie(filtered_df, names="Region", values="Total Revenue", title="Revenue by Region")
    st.plotly_chart(fig_reg, use_container_width=True)

with col3:
    fig_cat_units = px.pie(filtered_df, names="Product Category", values="Units Sold", title="Units Sold by Category")
    st.plotly_chart(fig_cat_units, use_container_width=True)

st.subheader("Category & Product Performance")
col4, col5 = st.columns(2)

with col4:
    cat_units = filtered_df.groupby("Product Category")["Units Sold"].sum().reset_index().sort_values(by="Units Sold", ascending=False)
    fig_hist_cat = px.bar(cat_units, x="Product Category", y="Units Sold", title="Total Units per Category")
    st.plotly_chart(fig_hist_cat, use_container_width=True)

with col5:
    top_prods = filtered_df.groupby("Product Name")["Total Revenue"].sum().nlargest(10).reset_index()
    fig_hist_rev = px.bar(top_prods, x="Total Revenue", y="Product Name", orientation='h', title="Top 10 Products by Revenue")
    fig_hist_rev.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_hist_rev, use_container_width=True)

st.subheader("Monthly Growth Trends")
trend_df = filtered_df.groupby(['Month_Num', 'Month']).agg({'Units Sold':'sum', 'Total Revenue':'sum'}).reset_index().sort_values("Month_Num")

col6, col7 = st.columns(2)
with col6:
    fig_trend_units = px.line(trend_df, x="Month", y="Units Sold", markers=True, title="Monthly Units Sold")
    st.plotly_chart(fig_trend_units, use_container_width=True)

with col7:
    fig_trend_rev = px.line(trend_df, x="Month", y="Total Revenue", markers=True, title="Monthly Revenue Growth")
    st.plotly_chart(fig_trend_rev, use_container_width=True)