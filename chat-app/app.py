import streamlit as st
from controllers.chat_controller import ChatController
from controllers.auth_controller import AuthController
from views.chat_view import ChatView
from views.auth_view import AuthView


# ---------- AUTH ----------
if "user_id" not in st.session_state:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email, pwd, login_btn = AuthView.login_form()
        if login_btn:
            user = AuthController.login(email, pwd)
            if user:
                st.session_state.user_id = user.id
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        email, pwd, reg_btn = AuthView.register_form()
        if reg_btn:
            user = AuthController.register(email, pwd)
            if user:
                st.success("Registered! Please login.")
            else:
                st.error("User already exists")

    st.stop()

# ---------- LOGOUT ----------
with st.sidebar:
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# ---------- CHAT ----------
if "current_chat_id" not in st.session_state:
    chat = ChatController.create_chat(st.session_state.user_id)
    st.session_state.current_chat_id = chat.id

chats = ChatController.get_all_chats(st.session_state.user_id)
ChatView.sidebar(
    chats,
    lambda: ChatController.create_chat(st.session_state.user_id),
    lambda cid: st.session_state.update({"current_chat_id": cid})
)
