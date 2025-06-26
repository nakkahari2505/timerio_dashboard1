import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
@st.cache_data
def load_data():
    xls = pd.ExcelFile("Reference_File.xlsx")
    revenue_df = xls.parse("Revenue and Footfall")
    modality_df = xls.parse("Modality counts")
    return revenue_df, modality_df

revenue_df, modality_df = load_data()

# Sort months in correct chronological order
month_order = ['Apr\'24', 'May\'24', 'Jun\'24', 'Jul\'24', 'Aug\'24', 'Sep\'24', 'Oct\'24', 'Nov\'24', 'Dec\'24', 'Jan\'25', 'Feb\'25', 'Mar\'25','Apr\'25','May\'25','Jun\'25']
revenue_df['MMM\'YY'] = pd.Categorical(revenue_df["MMM'YY"], categories=month_order, ordered=True)
modality_df['MMM\'YY'] = pd.Categorical(modality_df["MMM'YY"], categories=month_order, ordered=True)

# Sidebar/Top Dropdown
branch_list = revenue_df["Branch Name"].unique()
selected_branch = st.selectbox("Select Branch", branch_list)

# Filtered data
filtered_revenue = revenue_df[revenue_df["Branch Name"] == selected_branch].sort_values("MMM'YY")
filtered_modality = modality_df[modality_df["Branch Name"] == selected_branch]

# Revenue Trend
st.subheader(f"Revenue Trend for {selected_branch}")
fig1, ax1 = plt.subplots()
ax1.plot(filtered_revenue["MMM'YY"], filtered_revenue["Revenue(in_Lakhs)"], marker='o')
ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue (in Lakhs)")
ax1.set_title("Month-wise Revenue")
st.pyplot(fig1)

# Footfall Trend
st.subheader(f"Footfall Trend for {selected_branch}")
fig2, ax2 = plt.subplots()
ax2.plot(filtered_revenue["MMM'YY"], filtered_revenue["Footfall"], color='orange', marker='o')
ax2.set_xlabel("Month")
ax2.set_ylabel("Footfall")
ax2.set_title("Month-wise Footfall")
st.pyplot(fig2)

# Modality Count Cross Tab
st.subheader(f"Modality Count Table for {selected_branch}")
pivot_modality = pd.pivot_table(
    filtered_modality,
    values='Count',
    index='Depart_Grouping_H',
    columns='MMM\'YY',
    aggfunc='sum',
    fill_value=0
)
st.dataframe(pivot_modality)
