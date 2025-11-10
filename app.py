import streamlit as st
import pandas as pd
import yagmail
from io import BytesIO

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Grocery Billing App", page_icon="🛒")
YOUR_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]

# ----------------- SESSION STATE -----------------
if "day_data" not in st.session_state:
    st.session_state.day_data = []  # Stores all bills of the day

# Initialize editor key if not exists
if "entry_editor" not in st.session_state:
    st.session_state["entry_editor"] = pd.DataFrame({"Product": [""], "Price": [0.0]})

# ----------------- SIDEBAR NAVIGATION -----------------
page = st.sidebar.radio("Navigate", ["Add Bill", "View All Bills", "Send Full Day Report"])

# ----------------- PAGE 1: ADD BILL -----------------
if page == "Add Bill":
    st.title("🛒 Add Bill Items")
    st.write("Enter multiple products at once, then click ➕ Add Bill.")

    # Table editor for user input
    entry_table = st.data_editor(
        st.session_state["entry_editor"],
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

            st.success(f"✅ Bill added successfully! Total items: {len(entry_table)}")

            # --- Reset the editor table safely ---
            st.session_state["entry_editor"] = pd.DataFrame({"Product": [""], "Price": [0.0]})

# ----------------- PAGE 2: VIEW ALL BILLS -----------------
elif page == "View All Bills":
    st.title("📄 View Full Day Bills")
    if len(st.session_state.day_data) == 0:
        st.info("No data added yet.")
    else:
        df = pd.DataFrame(st.session_state.day_data)
        st.dataframe(df, use_container_width=True)
        total = df["Price"].sum()
        st.write(f"### ✅ Total Amount: Rs. {total:.2f}")

# ----------------- PAGE 3: SEND FULL DAY REPORT -----------------
elif page == "Send Full Day Report":
    st.title("📤 Send Full Day Report via Email")

    if len(st.session_state.day_data) == 0:
        st.info("No bills to send.")
    else:
        if st.button("Send CSV via Email"):
            try:
                # Combine all day data
                df = pd.DataFrame(st.session_state.day_data)

                # Save CSV in memory (no file on disk)
                csv_buffer = BytesIO()
                df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)

                # Send email
                yag = yagmail.SMTP(YOUR_EMAIL, APP_PASSWORD)
                yag.send(
                    to=YOUR_EMAIL,
                    subject="Daily Grocery Shop Report",
                    contents="Attached is the full day bill report.",
                    attachments=[("daily_report.csv", csv_buffer)]
                )

                st.success("✅ Report emailed successfully!")
                st.balloons()

                # Clear day data after sending
                st.session_state.day_data = []

            except Exception as e:
                st.error(f"❌ Error sending email: {e}")
