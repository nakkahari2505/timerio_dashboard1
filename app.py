import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def check_password():
    def password_entered():
        if st.session_state["password"] == "YourSecretPassword":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Clear the password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input
        st.text_input(
            "Enter password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Wrong password
        st.text_input(
            "Enter password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Correct password
        return True

if check_password():
    # Your real app goes here
    st.title("Secure Sales Dashboard")
    st.write("Welcome to the dashboard!")


# Load the Excel file
@st.cache_data
def load_data():
    xls = pd.ExcelFile("Reference_File.xlsx")
    revenue_df = xls.parse("Revenue and Footfall")
    modality_df = xls.parse("Modality counts")
    return revenue_df, modality_df

revenue_df, modality_df = load_data()

# Sort months in correct chronological order
month_order = [
    "Apr'24", "May'24", "Jun'24", "Jul'24", "Aug'24", "Sep'24",
    "Oct'24", "Nov'24", "Dec'24", "Jan'25", "Feb'25", "Mar'25",
    "Apr'25", "May'25", "Jun'25"
]
revenue_df["MMM'YY"] = pd.Categorical(revenue_df["MMM'YY"], categories=month_order, ordered=True)
modality_df["MMM'YY"] = pd.Categorical(modality_df["MMM'YY"], categories=month_order, ordered=True)

# Branch Selection
branch_list = revenue_df["Branch Name"].unique()
selected_branch = st.selectbox("Select Branch", branch_list)

# Filtered Data
filtered_revenue = revenue_df[revenue_df["Branch Name"] == selected_branch].sort_values("MMM'YY")
filtered_modality = modality_df[modality_df["Branch Name"] == selected_branch]

# Revenue Line Chart
st.subheader(f"Revenue Trend for {selected_branch}")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(filtered_revenue["MMM'YY"], filtered_revenue["Revenue(in_Lakhs)"], marker='o')
for i, val in enumerate(filtered_revenue["Revenue(in_Lakhs)"]):
    ax1.text(i, val, f"{val:.1f}", ha='center', va='bottom', fontsize=8)
ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue (in Lakhs)")
ax1.set_title("Month-wise Revenue")
st.pyplot(fig1)

# Footfall Line Chart
st.subheader(f"Footfall Trend for {selected_branch}")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(filtered_revenue["MMM'YY"], filtered_revenue["Footfall"], color='orange', marker='o')
for i, val in enumerate(filtered_revenue["Footfall"]):
    ax2.text(i, val, f"{int(val):,}", ha='center', va='bottom', fontsize=8)
ax2.set_xlabel("Month")
ax2.set_ylabel("Footfall")
ax2.set_title("Month-wise Footfall")
st.pyplot(fig2)

# Pivot Table for Modality Counts
st.subheader(f"Modality Count Table for {selected_branch}")
pivot_modality = pd.pivot_table(
    filtered_modality,
    values='Count',
    index='Depart_Grouping_H',
    columns="MMM'YY",
    aggfunc='sum',
    fill_value=0
)

# Format numbers with comma for readability
pivot_modality = pivot_modality.applymap(lambda x: f"{int(x):,}")
st.dataframe(pivot_modality)
