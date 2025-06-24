import streamlit as st
import pandas as pd
import plotly.express as px

# Title and header
st.title("📊 Business Update for Praveen Sir")
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
fig_rev.update_layout(yaxis_title='Revenue (₹)', xaxis_title='Month')
st.plotly_chart(fig_rev)

# === 2. Monthly Footfall Trend ===
st.subheader(f"Monthly Footfall Trend - {branch}")
monthly_footfall = filtered_df.groupby('Month_dt')['Footfall'].sum().reset_index()
monthly_footfall['Month'] = monthly_footfall['Month_dt'].dt.strftime("%b '%y")
fig_foot = px.line(monthly_footfall, x='Month', y='Footfall', markers=True, text='Footfall')
fig_foot.update_traces(textposition="top center")
fig_foot.update_layout(yaxis_title='Footfalls', xaxis_title='Month')
st.plotly_chart(fig_foot)

# === 3. Department vs Month Pivot (Footfall) ===
st.subheader(f"Department Footfall Pivot Table - {branch}")
pivot_df = filtered_df.pivot_table(
    index='Department',
    columns='Month_dt',
    values='Footfall',
    aggfunc='sum',
    fill_value=0
)

# Format and sort month columns
pivot_df.columns = [d.strftime("%b '%y") for d in sorted(pivot_df.columns)]
pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)

st.dataframe(pivot_df.style.format('{:,.0f}'))

# Footer
st.markdown("---")
st.markdown("🧠 _Smart Insights. Simple Delivery. [Timerio.in](https://timerio.in)_")
