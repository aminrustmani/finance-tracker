import streamlit as st
import pandas as pd
from datetime import date
import os

FILE_NAME = "transactions.xlsx"

st.title("Daily Debit & Credit Tracker")

# Create Excel file if it doesn't exist
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Description", "Debit", "Credit"])
    df.to_excel(FILE_NAME, index=False)

with st.form("transaction_form"):
    trans_date = st.date_input("Date", date.today())
    description = st.text_input("Description")
    debit = st.number_input("Debit Amount", min_value=0.0)
    credit = st.number_input("Credit Amount", min_value=0.0)

    submit = st.form_submit_button("Save Record")

if submit:
    df = pd.read_excel(FILE_NAME)

    new_row = {
        "Date": trans_date,
        "Description": description,
        "Debit": debit,
        "Credit": credit
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)

    st.success("Record Saved Successfully!")

# Display records
df = pd.read_excel(FILE_NAME)
st.subheader("Transaction Records")
st.dataframe(df)

# Calculate balance
total_debit = df["Debit"].sum()
total_credit = df["Credit"].sum()
balance = total_credit - total_debit

st.write(f"**Total Debit:** {total_debit}")
st.write(f"**Total Credit:** {total_credit}")
st.write(f"**Balance:** {balance}")

# Download Excel
with open(FILE_NAME, "rb") as f:
    st.download_button(
        "Download Excel File",
        f,
        file_name="transactions.xlsx"
    )