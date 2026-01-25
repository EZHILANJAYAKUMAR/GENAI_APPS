import streamlit as st
from controllers.chat_controller import ChatController
from controllers.auth_controller import AuthController
from views.chat_view import ChatView
from views.auth_view import AuthView

st.set_page_config(layout="wide", page_title="LLM ChatBot-App 🚀")

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
        full_name, email, pwd, reg_btn = AuthView.register_form()
        if reg_btn:
            user = AuthController.register(full_name, email, pwd)
            if user:
                st.success("Registered! Please login.")
            else:
                st.error("User already exists")

    st.stop()

# ================= CALLBACKS =================
def new_chat():
    chat = ChatController.create_chat(st.session_state.user_id)
    st.session_state.current_chat_id = chat.id

def select_chat(chat_id):
    st.session_state.current_chat_id = chat_id

def rename_chat(chat_id, new_title):
    ChatController.rename_chat(chat_id, new_title)

def delete_chat(chat_id):
    ChatController.delete_chat(chat_id)
    # If deleting current chat, switch to latest or create new
    if "current_chat_id" in st.session_state and st.session_state.current_chat_id == chat_id:
        latest_chat = ChatController.get_latest_chat(st.session_state.user_id)
        if latest_chat:
            st.session_state.current_chat_id = latest_chat.id
        else:
            # No chats left, remove current_chat_id to show welcome screen
            if "current_chat_id" in st.session_state:
                del st.session_state.current_chat_id

# ================= SIDEBAR =================
chats = ChatController.get_all_chats(st.session_state.user_id)
ChatView.sidebar(chats, new_chat, select_chat, rename_chat, delete_chat)

# ================= CHAT VIEW =================
if "current_chat_id" in st.session_state:
    current_chat = ChatController.get_chat(st.session_state.current_chat_id)
    st.header(current_chat.title)

    # Add padding to prevent overlap
    st.markdown('<div style="padding-top: 20px;"></div>', unsafe_allow_html=True)

    messages = ChatController.get_messages(st.session_state.current_chat_id)
    ChatView.render_messages(messages)

    if "waiting" not in st.session_state:
        st.session_state.waiting = False

    if st.session_state.waiting:
        with st.spinner("Generating response..."):
            ai_reply = ChatController.generate_ai_reply(
                st.session_state.current_chat_id
            )

            ChatController.add_message(
                st.session_state.current_chat_id,
                "assistant",
                ai_reply
            )

            st.session_state.waiting = False

            st.rerun()
    else:
        user_input = ChatView.chat_input()

        if user_input:
            ChatController.add_message(
                st.session_state.current_chat_id,
                "user",
                user_input
            )

            # Update chat title if it's the first message
            current_chat = ChatController.get_chat(st.session_state.current_chat_id)
            if current_chat.title == "New Chat":
                new_title = ChatController.generate_chat_title(st.session_state.current_chat_id)
                ChatController.rename_chat(st.session_state.current_chat_id, new_title)

            st.session_state.waiting = True

            st.rerun()
else:
    st.markdown('</div>', unsafe_allow_html=True)
    # Add padding to prevent overlap
    st.markdown('<div style="padding-top: 120px;"></div>', unsafe_allow_html=True)
    
    # Welcome screen
    st.title("Welcome to LLM ChatBot App! 🤖")
    st.markdown("""
    This is an AI-powered chatbot application where you can:
    
    - **Chat with AI**: Have intelligent conversations with our advanced language model
    - **Manage Sessions**: Create, rename, and delete chat sessions
    - **Persistent History**: Your conversations are saved and can be resumed anytime
    
    ### Getting Started:
    1. Click "➕ New Chat" in the sidebar to start a conversation
    2. Type your message and press Enter
    3. The AI will respond with helpful, contextual answers
    
    ### Features:
    - Real-time AI responses
    - Session management
    - User authentication
    - Responsive design
    
    Start chatting now!
    """)
