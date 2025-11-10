import streamlit as st
import pandas as pd
import yagmail
from io import BytesIO
import datetime

# ---------------- EMAIL CONFIG ----------------
YOUR_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]
# ----------------------------------------------

st.set_page_config(page_title="Grocery Billing App", page_icon="🧾")
st.title("Grocery Shop Billing System 🛒")

# ------------- SESSION STATE TABLE -------------
if "items" not in st.session_state:
    st.session_state.items = []  # list of dicts
# -----------------------------------------------

st.subheader("Add Item to Bill")

# Input fields
col1, col2 = st.columns(2)
with col1:
    product = st.text_input("Product Code / Name")
with col2:
    price = st.number_input("Price (Rs)", min_value=0.0, step=1.0)

# Add button
if st.button("Add Item"):
    if product.strip() == "":
        st.error("Product name cannot be empty.")
    else:
        st.session_state.items.append({
            "Product": product,
            "Price (Rs)": price
        })
        st.success("✅ Item added!")

# Convert to DataFrame for display
df = pd.DataFrame(st.session_state.items)

st.subheader("Current Bill Items")
st.table(df)

# ---------------- DAY END SUBMIT ----------------
st.subheader("Day-End Report")

if st.button("Submit & Email Report"):
    if df.empty:
        st.error("No items to submit.")
    else:
        try:
            # Create Excel file in memory
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Report")

            buffer.seek(0)

            # Email sending
            yag = yagmail.SMTP(YOUR_EMAIL, APP_PASSWORD)

            today = datetime.date.today().strftime("%Y-%m-%d")
            subject = f"Grocery Shop Daily Report - {today}"
            body = f"Attached is today's report containing {len(df)} items."

            yag.send(
                to=YOUR_EMAIL,
                subject=subject,
                contents=body,
                attachments={f"daily_report_{today}.xlsx": buffer.getvalue()}
            )

            st.success("✅ Report emailed successfully!")

            # Clear table
            st.session_state.items = []

        except Exception as e:
            st.error(f"❌ Error sending email: {e}")






