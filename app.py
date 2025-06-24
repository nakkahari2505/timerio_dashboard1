import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel("refined_dashboard_data_fixed.xlsx")

# Convert Month_dt to datetime
df['Month_dt'] = pd.to_datetime(df['Month_dt'])

# Page title
st.title("Branch Trends for Praveen Sir")

# Branch selection at top
branches = df['Branch'].unique()
selected_branch = st.selectbox("Select Branch", sorted(branches))

# Filtered data
df_filtered = df[df['Branch'] == selected_branch].sort_values("Month_dt")

# Line chart - Revenue trend
revenue_monthly = df_filtered.groupby("Month_dt")["Revenue"].sum().reset_index()
fig_revenue = px.line(revenue_monthly, x="Month_dt", y="Revenue", markers=True, text="Revenue")
fig_revenue.update_traces(textposition="top center", texttemplate='%{y:.1f}')
fig_revenue.update_layout(title="Monthly Revenue Trend", yaxis_title="Revenue (₹ Lakhs)", xaxis_title="Month")
st.plotly_chart(fig_revenue)

# Pivot Table - Department vs Month for FOOTFALL
pivot_df = df_filtered.pivot_table(index="Department", columns="Month_dt", values="Footfall", aggfunc="sum", fill_value=0)

# Ensure months are sorted correctly
pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)

# Rename columns for display
pivot_df.columns = [col.strftime('%b %y') for col in pivot_df.columns]

st.subheader("Department-wise Footfall by Month")
st.dataframe(pivot_df.style.format("{:.0f}"))
