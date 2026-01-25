import streamlit as st
from controllers.chat_controller import ChatController
from controllers.auth_controller import AuthController
from views.chat_view import ChatView
from views.auth_view import AuthView

st.set_page_config(layout="wide", page_title="LLM ChatBot-App")

# ================= AUTH =================
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

# ================= LOGOUT =================
with st.sidebar:
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# ================= INIT CHAT =================
if "current_chat_id" not in st.session_state:
    latest_chat = ChatController.get_latest_chat(st.session_state.user_id)
    if latest_chat:
        st.session_state.current_chat_id = latest_chat.id
    else:
        chat = ChatController.create_chat(st.session_state.user_id)
        st.session_state.current_chat_id = chat.id

# ================= CALLBACKS =================
def new_chat():
    chat = ChatController.create_chat(st.session_state.user_id)
    st.session_state.current_chat_id = chat.id

def select_chat(chat_id):
    st.session_state.current_chat_id = chat_id

def rename_chat(chat_id, new_title):
    ChatController.rename_chat(chat_id, new_title)

# ================= SIDEBAR =================
chats = ChatController.get_all_chats(st.session_state.user_id)
ChatView.sidebar(chats, new_chat, select_chat, rename_chat)

# ================= CHAT VIEW =================
messages = ChatController.get_messages(st.session_state.current_chat_id)
ChatView.render_messages(messages)

user_input = ChatView.chat_input()

if user_input:
    ChatController.add_message(
        st.session_state.current_chat_id,
        "user",
        user_input
    )

    ai_reply = ChatController.generate_ai_reply(
        st.session_state.current_chat_id
    )

    ChatController.add_message(
        st.session_state.current_chat_id,
        "assistant",
        ai_reply
    )

    st.rerun()
