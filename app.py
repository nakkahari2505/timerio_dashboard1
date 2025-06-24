import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel("refined_dashboard_data_fixed.xlsx")

# Convert Month_dt to datetime for sorting
df['Month_dt'] = pd.to_datetime(df['Month_dt'])

# Sidebar filters
branches = df['Branch'].unique()
selected_branch = st.sidebar.selectbox("Select Branch", sorted(branches))

# Filter by branch
df_filtered = df[df['Branch'] == selected_branch]

# Sort by Month_dt
df_filtered = df_filtered.sort_values("Month_dt")

# Title
st.title("Sales Dashboards - Praveen Sir")
st.subheader(f"Branch: {selected_branch}")

# Revenue Line Chart
revenue_monthly = df_filtered.groupby("Month_dt")["Revenue"].sum().reset_index()
fig_revenue = px.line(revenue_monthly, x="Month_dt", y="Revenue", markers=True, text="Revenue")
fig_revenue.update_traces(textposition="top center", texttemplate='%{y:.1f}')
fig_revenue.update_layout(title="Monthly Revenue Trend", yaxis_title="Revenue (₹ Lakhs)", xaxis_title="Month")
st.plotly_chart(fig_revenue)

# Department-wise Pivot Table
pivot_df = df_filtered.pivot_table(index="Department", columns="Month_dt", values="Revenue", aggfunc="sum", fill_value=0)
pivot_df = pivot_df[sorted(pivot_df.columns)]
st.subheader("Department-wise Revenue by Month")
st.dataframe(pivot_df.style.format("{:.1f}"))
