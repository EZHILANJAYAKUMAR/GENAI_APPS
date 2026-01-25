import streamlit as st

class AuthView:

    @staticmethod
    def login_form():
        with st.form("login_form"):
            st.subheader("🔐 Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            return email, password, submitted

    @staticmethod
    def register_form():
        with st.form("register_form"):
            st.subheader("📝 Register")
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            if password and confirm_password and password != confirm_password:
                st.error("Passwords do not match")
            submitted = st.form_submit_button("Register")
            return full_name, email, password, submitted
    


