import streamlit as st

class AuthView:

    @staticmethod
    def login_form():
        st.subheader("🔐 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        return email, password, st.button("Login")

    @staticmethod
    def register_form():
        st.subheader("📝 Register")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pwd")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_conf_pwd")
        # secret_question_1 = st.text_input("Secret Question 1", key="reg_sec_q1")
        # secret_answer_1 = st.text_input("Secret Answer 1", key="reg_sec_a1") 
        # secret_question_2 = st.text_input("Secret Question 2", key="reg_sec_q2")
        # secret_answer_2 = st.text_input("Secret Answer 2", key="reg_sec_a2")
        # secret_question_3 = st.text_input("Secret Question 3", key="reg_sec_q3")
        # secret_answer_3 = st.text_input("Secret Answer 3", key="reg_sec_a3")
        

        if password != confirm_password:
            st.error("Passwords do not match")
        return email, password, st.button("Register")
    


