import streamlit as st
import yagmail

# ---------- EMAIL CONFIG ----------
# Use Streamlit Secrets for safety
YOUR_EMAIL = st.secrets["EMAIL"]         # Sender email (your Gmail)
APP_PASSWORD = st.secrets["APP_PASSWORD"] # Gmail App Password
# ----------------------------------

st.set_page_config(page_title="Contact App", page_icon="✉️")
st.title("Send me a message")
st.write("Type your name and message below. I will receive it instantly!")

# Input fields
name = st.text_input("Your Name (optional)")
message = st.text_area("Your Message")

# Submit button
if st.button("Submit"):
    if message.strip() != "":
        try:
            # Email subject and content
            subject = "New Message from Web App"
            if name.strip() != "":
                content = f"App: My Web App\nFrom: {name}\n\nMessage:\n{message}"
            else:
                content = f"App: My Web App\nMessage:\n{message}"

            # Send email
            yag = yagmail.SMTP(YOUR_EMAIL, APP_PASSWORD)
            yag.send(to=YOUR_EMAIL, subject=subject, contents=content)

            st.success("✅ Your message has been sent!")

            # Clear input fields after submission
            st.session_state["name"] = ""
            st.session_state["message"] = ""
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
    else:
        st.error("Please type a message first.")






