import streamlit as st
import pandas as pd
import plotly.express as px

# Title and header
st.title("Business Trends for Praveen Sir")
st.markdown("Built by **Timerio** | Powered by Data")

# Load refined Excel file
df = pd.read_excel("refined_dashboard_data_fixed.xlsx")

# Rename columns for consistency
df.columns = ['Branch', 'Month', 'Department', 'Revenue', 'Footfall', 'Month_dt', 'Revenue_fmt']

# Dropdown to select Branch
branch = st.selectbox("Select Branch", sorted(df['Branch'].unique()))

# Filter data by selected branch
filtered_df = df[df['Branch'] == branch]

# === 1. Monthly Revenue Trend ===
st.subheader(f"Monthly Revenue Trend - {branch}")
monthly_revenue = filtered_df.groupby('Month_dt')['Revenue'].sum().reset_index()
monthly_revenue['Month'] = monthly_revenue['Month_dt'].dt.strftime("%b '%y")
fig_rev = px.line(monthly_revenue, x='Month', y='Revenue', markers=True, text='Revenue')
fig_rev.update_traces(textposition="top center")
fig_rev.update_layout(yaxis_title='Revenue (₹ Lakhs)', xaxis_title='Month')
st.plotly_chart(fig_rev)


# === 2. Department vs Month Pivot (Footfall) ===
st.subheader(f"Department Footfall Pivot Table - {branch}")

# Create pivot with Month_dt for proper sort
pivot_df = filtered_df.pivot_table(
    index='Department',
    columns='Month_dt',
    values='Footfall',
    aggfunc='sum',
    fill_value=0
)

# Sort month columns
pivot_df = pivot_df[sorted(pivot_df.columns)]

# Rename columns to formatted month names
pivot_df.columns = [col.strftime("%b '%y") for col in pivot_df.columns]

st.dataframe(pivot_df.style.format('{:,.0f}'))
