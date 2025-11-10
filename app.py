import streamlit as st
import pandas as pd
import yagmail

st.set_page_config(page_title="Grocery Billing App", page_icon="🛒")

YOUR_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]

# Session state for full-day data
if "day_data" not in st.session_state:
    st.session_state.day_data = []

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Add Bill", "View All Bills"])


# -----------------------------------------------------
# ✅ PAGE 1: ADD BILL (Table Input)
# -----------------------------------------------------
if page == "Add Bill":

    st.title("🛒 Add Bill Items")
    st.write("Enter multiple products at once, then click ADD BILL.")

    # Temporary entry table for user to type items
    example = pd.DataFrame({
        "Product": [""],
        "Price": [0]
    })

    entry_table = st.data_editor(
        example,
        num_rows="dynamic",
        use_container_width=True,
        key="entry_editor"
    )

    if st.button("➕ Add Bill"):
        if entry_table["Product"].str.strip().eq("").all():
            st.warning("Please fill at least one product.")
        else:
            # Append each row to full-day data
            for _, row in entry_table.iterrows():
                if row["Product"].strip() != "" and row["Price"] > 0:
                    st.session_state.day_data.append(
                        {"Product": row["Product"], "Price": row["Price"]}
                    )

            st.success("✅ Bill added successfully!")

            # Clear the editor table
            st.session_state.entry_editor = example

    # Submit button to send email with all-day data
    if st.button("📤 Submit Full Day Report"):
        if len(st.session_state.day_data) == 0:
            st.error("No data to submit.")
        else:
            try:
                df = pd.DataFrame(st.session_state.day_data)
                file_path = "daily_report.csv"
                df.to_csv(file_path, index=False)

                yag = yagmail.SMTP(YOUR_EMAIL, APP_PASSWORD)
                yag.send(
                    to=YOUR_EMAIL,
                    subject="Daily Grocery Shop Report",
                    contents="Attached is the full day bill report.",
                    attachments=file_path
                )

                st.success("✅ Report emailed successfully!")
                st.balloons()

                # Clear after sending
                st.session_state.day_data = []

            except Exception as e:
                st.error(f"❌ Error sending email: {e}")


# -----------------------------------------------------
# ✅ PAGE 2: VIEW COMPLETE DAY DATA
# -----------------------------------------------------
if page == "View All Bills":

    st.title("📄 View Full Day Bills")

    if len(st.session_state.day_data) == 0:
        st.info("No data added yet.")
    else:
        df = pd.DataFrame(st.session_state.day_data)
        st.dataframe(df, use_container_width=True)

        total = df["Price"].sum()
        st.write(f"### ✅ Total Amount: Rs. {total:.2f}")
