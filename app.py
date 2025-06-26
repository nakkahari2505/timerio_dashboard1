import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load data
@st.cache_data
def load_data():
    xls = pd.ExcelFile('Reference_File.xlsx')
    revenue_df = xls.parse("Revenue and Footfall")
    modality_df = xls.parse("Modality counts")
    return revenue_df, modality_df

# Load data
revenue_df, modality_df = load_data()

# Clean data
revenue_df['Month'] = pd.to_datetime(revenue_df['Month'], format='%b-%y')
revenue_df.sort_values(by='Month', inplace=True)
modality_df['Month'] = pd.to_datetime(modality_df['Month'], format='%b-%y')
modality_df.sort_values(by='Month', inplace=True)

# UI
st.title("Branch Performance Dashboard")
branches = revenue_df['Branch'].unique()
selected_branch = st.selectbox("Select Branch", branches)

# Filter for selected branch
branch_data = revenue_df[revenue_df['Branch'] == selected_branch]

# Plot Revenue
st.subheader(f"Revenue Trend for {selected_branch}")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(branch_data['Month'], branch_data['Revenue'], marker='o')
for i, value in enumerate(branch_data['Revenue']):
    ax1.text(branch_data['Month'].iloc[i], value + 0.5, f"{value:.1f}", ha='center')
ax1.set_title("Month-wise Revenue")
ax1.set_ylabel("Revenue (in Lakhs)")
ax1.grid(True)
st.pyplot(fig1)

# Plot Footfalls
st.subheader(f"Footfall Trend for {selected_branch}")
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(branch_data['Month'], branch_data['Footfalls'], marker='o', color='orange')
for i, value in enumerate(branch_data['Footfalls']):
    ax2.text(branch_data['Month'].iloc[i], value + 10, f"{int(value):,}", ha='center')
ax2.set_title("Month-wise Footfalls")
ax2.set_ylabel("Footfall Count")
ax2.grid(True)
st.pyplot(fig2)

# Modality Pivot Table
st.subheader(f"Modality Trends for {selected_branch}")
branch_modality = modality_df[modality_df['Branch'] == selected_branch]
pivot_table = branch_modality.pivot_table(index='Modality', columns=branch_modality['Month'].dt.strftime('%b-%y'),
                                           values='Footfalls', aggfunc='sum', fill_value=0)
pivot_table = pivot_table.applymap(lambda x: f"{int(x):,}")
st.dataframe(pivot_table)
