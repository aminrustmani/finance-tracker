import streamlit as st
import pandas as pd
import os
from datetime import date

# -----------------------------
# Configuration
# -----------------------------
FILE_NAME = "transactions.xlsx"

st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# Create Excel file if missing
# -----------------------------
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(
        columns=["ID", "Date", "Description", "Debit", "Credit"]
    )
    df.to_excel(FILE_NAME, index=False)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_excel(FILE_NAME)

# -----------------------------
# Title
# -----------------------------
st.title("💰 Daily Debit & Credit Tracker")

# -----------------------------
# Add Transaction Form
# -----------------------------
st.header("Add New Transaction")

with st.form("add_transaction"):

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

    submitted = st.form_submit_button("Add Transaction")

    if submitted:

        if description.strip() == "":
            st.error("Please enter a description.")
        else:

            if len(df) == 0:
                new_id = 1
            else:
                new_id = int(df["ID"].max()) + 1

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

            st.success("Transaction added successfully!")
            st.rerun()

# -----------------------------
# Summary
# -----------------------------
st.header("Summary")

total_debit = pd.to_numeric(
    df["Debit"],
    errors="coerce"
).fillna(0).sum()

total_credit = pd.to_numeric(
    df["Credit"],
    errors="coerce"
).fillna(0).sum()

balance = total_credit - total_debit

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Debit", f"{total_debit:,.2f}")

with col2:
    st.metric("Total Credit", f"{total_credit:,.2f}")

with col3:
    st.metric("Balance", f"{balance:,.2f}")

# -----------------------------
# Editable Transactions Table
# -----------------------------
st.header("Transactions")

if len(df) > 0:

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="editor"
    )

    col_save, col_refresh = st.columns(2)

    with col_save:
        if st.button("💾 Save Changes"):

            edited_df["Debit"] = pd.to_numeric(
                edited_df["Debit"],
                errors="coerce"
            ).fillna(0)

            edited_df["Credit"] = pd.to_numeric(
                edited_df["Credit"],
                errors="coerce"
            ).fillna(0)

            edited_df.to_excel(
                FILE_NAME,
                index=False
            )

            st.success("Changes saved successfully!")
            st.rerun()

    with col_refresh:
        if st.button("🔄 Refresh"):
            st.rerun()

else:
    st.info("No transactions found.")

# -----------------------------
# Download Excel File
# -----------------------------
st.header("Download Data")

with open(FILE_NAME, "rb") as file:
    st.download_button(
        label="📥 Download Excel File",
        data=file,
        file_name="transactions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
