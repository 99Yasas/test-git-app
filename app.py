import streamlit as st
import pandas as pd
import yagmail
import os

st.set_page_config(page_title="Grocery Billing App", page_icon="🛒")

YOUR_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]

# Initialize items list in session state
if "data_items" not in st.session_state:
    st.session_state.data_items = []

st.title("🛒 Grocery Billing System")
st.write("Add product details below and generate the daily bill report.")

# --- INPUT AREA ---
col1, col2 = st.columns(2)

with col1:
    product = st.text_input("Product Name or Code")

with col2:
    price = st.number_input("Price", min_value=0.0, step=0.5)

add_btn = st.button("➕ Add Item")

# --- ADD ITEM ---
if add_btn:
    if product.strip() == "":
        st.warning("Enter the product name or code.")
    elif price <= 0:
        st.warning("Enter a valid price.")
    else:
        st.session_state.data_items.append({
            "Product": product,
            "Price": price
        })
        st.success("Item added!")

# --- DISPLAY TABLE ---
if len(st.session_state.data_items) > 0:
    st.subheader("Current Bill Items")
    df = pd.DataFrame(st.session_state.data_items)
    st.dataframe(df, use_container_width=True)

    total = df["Price"].sum()
    st.write(f"### ✅ Total: Rs. {total:.2f}")

# --- SUBMIT EMAIL ---
if st.button("📤 Submit & Email Report"):
    if len(st.session_state.data_items) == 0:
        st.error("You cannot submit an empty report.")
    else:
        try:
            # Save to Excel
            file_path = "daily_report.xlsx"
            df = pd.DataFrame(st.session_state.data_items)
            df.to_excel(file_path, index=False)

            # Send email
            yag = yagmail.SMTP(YOUR_EMAIL, APP_PASSWORD)
            yag.send(
                to=YOUR_EMAIL,
                subject="Daily Grocery Shop Report",
                contents="Attached is today's bill report.",
                attachments=file_path
            )

            st.success("✅ Report emailed successfully!")
            st.balloons()

            # Clear table after sending
            st.session_state.data_items = []

        except Exception as e:
            st.error(f"❌ Error sending email: {e}")
