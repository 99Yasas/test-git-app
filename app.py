import streamlit as st
import pandas as pd
import yagmail
from io import BytesIO

# ---------- EMAIL CONFIG ----------
YOUR_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]
# ----------------------------------

st.set_page_config(page_title="Grocery Shop App", page_icon="🛒", layout="wide")

# Initialize session_state
if "bills" not in st.session_state:
    st.session_state.bills = []  # Stores each bill as a DataFrame

# Sidebar for navigation
page = st.sidebar.selectbox("Page", ["Add Bill", "View All Bills", "Send All Bills"])

# ---------------- ADD BILL PAGE ----------------
if page == "Add Bill":
    st.header("Add New Bill")

    # Let user create a table for the bill
    default_data = {
        "Product Code": ["", "", ""],
        "Product Name": ["", "", ""],
        "Price": [0, 0, 0]
    }
    bill_df = st.experimental_data_editor(pd.DataFrame(default_data), num_rows="dynamic")

    if st.button("Add Bill"):
        # Save this bill in session_state
        st.session_state.bills.append(bill_df)
        st.success("✅ Bill added for today!")

# ---------------- VIEW ALL BILLS PAGE ----------------
elif page == "View All Bills":
    st.header("All Bills Today")
    if len(st.session_state.bills) == 0:
        st.info("No bills added yet.")
    else:
        # Show all bills concatenated
        all_bills = pd.concat(st.session_state.bills, ignore_index=True)
        st.dataframe(all_bills)

# ---------------- SEND ALL BILLS PAGE ----------------
elif page == "Send All Bills":
    st.header("Send All Bills to Email")
    if len(st.session_state.bills) == 0:
        st.info("No bills to send.")
    else:
        if st.button("Send CSV via Email"):
            try:
                # Combine all bills
                all_bills = pd.concat(st.session_state.bills, ignore_index=True)

                # Save to in-memory CSV
                csv_buffer = BytesIO()
                all_bills.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)

                # Send email
                yag = yagmail.SMTP(YOUR_EMAIL, APP_PASSWORD)
                yag.send(
                    to=YOUR_EMAIL,
                    subject="All Bills for Today",
                    contents="Attached is the CSV of all bills.",
                    attachments=[("all_bills.csv", csv_buffer)]
                )
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"❌ Error sending email: {e}")
