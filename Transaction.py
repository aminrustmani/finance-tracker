import streamlit as st
import pandas as pd
import os
from datetime import date

# ==========================================
# Configuration
# ==========================================
FILE_NAME = "transactions.xlsx"

st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# ==========================================
# Create Excel file if it doesn't exist
# ==========================================
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(
        columns=["ID", "Date", "Description", "Debit", "Credit"]
    )
    df.to_excel(FILE_NAME, index=False)

# ==========================================
# Load Data
# ==========================================
try:
    df = pd.read_excel(FILE_NAME)
except Exception:
    df = pd.DataFrame(
        columns=["ID", "Date", "Description", "Debit", "Credit"]
    )

# ==========================================
# Ensure Required Columns Exist
# ==========================================
required_columns = ["ID", "Date", "Description", "Debit", "Credit"]

for col in required_columns:
    if col not in df.columns:
        if col == "ID":
            df[col] = range(1, len(df) + 1)
        elif col in ["Debit", "Credit"]:
            df[col] = 0.0
        else:
            df[col] = ""

# Reorder columns
df = df[required_columns]

# Save corrected structure if needed
df.to_excel(FILE_NAME, index=False)

# ==========================================
# Title
# ==========================================
st.title("💰 Daily Debit & Credit Tracker")

# ==========================================
# Add Transaction
# ==========================================
st.header("Add New Transaction")

with st.form("transaction_form"):

    trans_date = st.date_input(
        "Date",
        value=date.today()
    )

    description = st.text_input(
        "Description"
    )

    debit = st.number_input(
        "Debit Amount",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    credit = st.number_input(
        "Credit Amount",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    submit = st.form_submit_button("Add Transaction")

    if submit:

        if description.strip() == "":
            st.error("Please enter a description.")

        else:

            if len(df) == 0:
                new_id = 1
            else:
                new_id = int(pd.to_numeric(
                    df["ID"],
                    errors="coerce"
                ).max()) + 1

            new_row = pd.DataFrame([{
                "ID": new_id,
                "Date": trans_date,
                "Description": description,
                "Debit": debit,
                "Credit": credit
            }])

            df = pd.concat(
                [df, new_row],
                ignore_index=True
            )

            df.to_excel(FILE_NAME, index=False)

            st.success("Transaction Added Successfully!")
            st.rerun()

# ==========================================
# Summary
# ==========================================
st.header("Summary")

df["Debit"] = pd.to_numeric(
    df["Debit"],
    errors="coerce"
).fillna(0)

df["Credit"] = pd.to_numeric(
    df["Credit"],
    errors="coerce"
).fillna(0)

total_debit = df["Debit"].sum()
total_credit = df["Credit"].sum()
balance = total_credit - total_debit

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Debit",
    f"{total_debit:,.2f}"
)

col2.metric(
    "Total Credit",
    f"{total_credit:,.2f}"
)

col3.metric(
    "Balance",
    f"{balance:,.2f}"
)

# ==========================================
# Transaction Table
# ==========================================
st.header("Transactions")

st.info(
    "You can edit any cell directly. "
    "To delete a transaction, remove its row and click Save Changes."
)

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    key="transaction_editor"
)

# ==========================================
# Save Changes
# ==========================================
if st.button("💾 Save Changes"):

    edited_df["Debit"] = pd.to_numeric(
        edited_df["Debit"],
        errors="coerce"
    ).fillna(0)

    edited_df["Credit"] = pd.to_numeric(
        edited_df["Credit"],
        errors="coerce"
    ).fillna(0)

    # Reassign IDs to keep them clean
    edited_df["ID"] = range(
        1,
        len(edited_df) + 1
    )

    edited_df.to_excel(
        FILE_NAME,
        index=False
    )

    st.success("Changes Saved Successfully!")
    st.rerun()

# ==========================================
# Download Excel
# ==========================================
st.header("Download Records")

with open(FILE_NAME, "rb") as file:
    st.download_button(
        label="📥 Download Excel File",
        data=file,
        file_name="transactions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
