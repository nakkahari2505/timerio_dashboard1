import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit Page Config
st.set_page_config(layout="wide")

# Load Excel file
@st.cache_data
def load_data():
    xls = pd.ExcelFile("Reference_File.xlsx")
    revenue_df = xls.parse("Revenue and Footfall")
    modality_df = xls.parse("Modality counts")
    return revenue_df, modality_df

revenue_df, modality_df = load_data()

# Define month order
month_order = ["Apr'24", "May'24", "Jun'24", "Jul'24", "Aug'24", "Sep'24", "Oct'24", 
               "Nov'24", "Dec'24", "Jan'25", "Feb'25", "Mar'25", "Apr'25", "May'25", "Jun'25"]

# Apply correct month ordering
revenue_df['Month'] = pd.Categorical(revenue_df['Month'], categories=month_order, ordered=True)
modality_df['Month'] = pd.Categorical(modality_df['Month'], categories=month_order, ordered=True)

# Branch Dropdown
branches = revenue_df["Branch Name"].unique()
selected_branch = st.selectbox("Select Branch", branches)

# Filter Data
filtered_revenue = revenue_df[revenue_df["Branch Name"] == selected_branch].sort_values("Month")
filtered_modality = modality_df[modality_df["Branch Name"] == selected_branch]

# --- Revenue Line Chart ---
st.subheader(f"Revenue Trend for {selected_branch}")
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(filtered_revenue['Month'], filtered_revenue["Revenue(in_Lakhs)"], marker='o')
for i, val in enumerate(filtered_revenue["Revenue(in_Lakhs)"]):
    ax1.text(i, val, f"{val:.1f}", ha='center', va='bottom', fontsize=8)
ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue (in Lakhs)")
ax1.set_title("Month-wise Revenue")
st.pyplot(fig1)

# --- Footfall Line Chart ---
st.subheader(f"Footfall Trend for {selected_branch}")
fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(filtered_revenue['Month'], filtered_revenue["Footfall"], marker='o', color='orange')
for i, val in enumerate(filtered_revenue["Footfall"]):
    ax2.text(i, val, f"{int(val)}", ha='center', va='bottom', fontsize=8)
ax2.set_xlabel("Month")
ax2.set_ylabel("Footfalls")
ax2.set_title("Month-wise Footfall")
