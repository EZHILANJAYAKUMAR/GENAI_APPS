import streamlit as st

class ChatView:

    @staticmethod
    def sidebar(chats, on_new_chat, on_select_chat):
        with st.sidebar:
            st.title("💬 Chats")

            if st.button("➕ New Chat"):
                on_new_chat()

            st.divider()

            for chat in chats:
                if st.button(chat.title, key=f"chat_{chat.id}"):
                    on_select_chat(chat.id)

    @staticmethod
    def render_messages(messages):
        for msg in messages:
            with st.chat_message(msg.role):
                st.write(msg.content)

    @staticmethod
    def chat_input():
        return st.chat_input("Type your message...")
