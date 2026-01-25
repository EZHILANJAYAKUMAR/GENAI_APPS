import streamlit as st

class ChatView:

    @staticmethod
    def sidebar(chats, new_chat_cb, select_cb, rename_cb):
        with st.sidebar:
            st.button("➕ New Chat", on_click=new_chat_cb)
            st.divider()

            for chat in chats:
                col1, col2 = st.columns([8, 2])

                with col1:
                    if st.button(chat.title, key=f"select_{chat.id}"):
                        select_cb(chat.id)

                with col2:
                    if st.button("✏️", key=f"edit_{chat.id}"):
                        st.session_state.editing_chat_id = chat.id
                        st.session_state[f"title_{chat.id}"] = chat.title
                        st.rerun()

            # Show edit input if editing
            if "editing_chat_id" in st.session_state:
                chat_id = st.session_state.editing_chat_id
                chat = next((c for c in chats if c.id == chat_id), None)
                if chat:
                    st.text_input(
                        "Rename chat",
                        key=f"title_{chat_id}"
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Save", key=f"save_{chat_id}"):
                            new_title = st.session_state[f"title_{chat_id}"]
                            rename_cb(chat_id, new_title)
                            del st.session_state.editing_chat_id
                            if f"title_{chat_id}" in st.session_state:
                                del st.session_state[f"title_{chat_id}"]
                            st.rerun()
                    with col2:
                        if st.button("Cancel", key=f"cancel_{chat_id}"):
                            del st.session_state.editing_chat_id
                            if f"title_{chat_id}" in st.session_state:
                                del st.session_state[f"title_{chat_id}"]
                            st.rerun()


    @staticmethod
    def render_messages(messages):
        for msg in messages:
            with st.chat_message(msg.role):
                st.write(msg.content)

    @staticmethod
    def chat_input():
        return st.chat_input("Type your message...")
