import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("📊 Sales Dashboard Prototype")
st.markdown("Built by **Timerio** | Powered by Data")

# Load refined data
df = pd.read_excel("refined_dashboard_data_fixed.xlsx")

# Rename for readability
df.columns = ['Branch', 'Month', 'Department', 'Revenue', 'Footfall', 'Month_dt', 'Revenue_fmt']

# Sidebar filter
branch = st.selectbox("Select Branch", sorted(df['Branch'].unique()))

# Filter data
filtered_df = df[df['Branch'] == branch]

# Revenue Line Chart
st.subheader(f"Monthly Revenue Trend - {branch}")
monthly_revenue = filtered_df.groupby('Month_dt')['Revenue'].sum().reset_index()
monthly_revenue['Month'] = monthly_revenue['Month_dt'].dt.strftime("%b '%y")
fig = px.line(monthly_revenue, x='Month', y='Revenue', markers=True, labels={'Revenue': 'Revenue (₹)'})
st.plotly_chart(fig)

# Department vs Month Pivot (Footfall)
st.subheader(f"Department Footfall Pivot Table - {branch}")
pivot_df = filtered_df.pivot_table(index='Department', columns=filtered_df['Month_dt'].dt.strftime("%b '%y"),
                                   values='Footfall', aggfunc='sum', fill_value=0)
st.dataframe(pivot_df.style.format('{:,.0f}'))

# Footer
st.markdown("---")
st.markdown("🧠 _Smart Insights. Simple Delivery. Timerio.in_")
