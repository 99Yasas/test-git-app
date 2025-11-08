import streamlit as st
import yagmail

# ---------- EMAIL CONFIG ----------
# We are using Streamlit secrets for safety
YOUR_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]
# ----------------------------------

st.set_page_config(page_title="Send me a message", page_icon="✉️")
st.title("Send me a message")
st.write("Type your message below and I will receive it instantly!")

# Input fields
name = st.text_input("Your Name (optional)")
message = st.text_area("Your Message")

# Submit button
if st.button("Submit"):
    if message.strip() != "":
        try:
            # Prepare email content
            email_subject = "New Message from Web App"
            if name.strip() != "":
                email_content = f"From: {name}\n\n{message}"
            else:
                email_content = message

            # Send email
            yag = yagmail.SMTP(YOUR_EMAIL, APP_PASSWORD)
            yag.send(to=YOUR_EMAIL, subject=email_subject, contents=email_content)

            st.success("✅ Your message has been sent!")
            # Clear input fields
            st.session_state["name"] = ""
            st.session_state["message"] = ""
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
    else:
        st.error("Please type a message first.")


