import streamlit as st

class ChatView:

    @staticmethod
    def sidebar(chats, new_chat_cb, select_cb, rename_cb):
        with st.sidebar:
            st.button("➕ New Chat", on_click=new_chat_cb)
            st.divider()

            for chat in chats:
                if "editing_chat_id" in st.session_state and st.session_state.editing_chat_id == chat.id:
                    # Show rename form with Save and Cancel buttons side by side
                    with st.form(key=f"rename_form_{chat.id}"):
                        new_title = st.text_input("Rename", value=chat.title, label_visibility="collapsed")
                        
                        # Horizontal layout for buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            submitted = st.form_submit_button("Save", type="primary")
                        with col2:
                            cancel = st.form_submit_button("Cancel", type="secondary")

                        if submitted:
                            rename_cb(chat.id, new_title)
                            del st.session_state.editing_chat_id
                            st.rerun()

                        if cancel:
                            del st.session_state.editing_chat_id
                            st.rerun()
                else:
                    # Normal chat display
                    col1, col2 = st.columns([8, 2])
                    with col1:
                        if st.button(chat.title, key=f"select_{chat.id}"):
                            select_cb(chat.id)
                    with col2:
                        if st.button("✏️", key=f"edit_{chat.id}"):
                            st.session_state.editing_chat_id = chat.id
                            st.rerun()

    @staticmethod
    def render_messages(messages):
        for msg in messages:
            with st.chat_message(msg.role):
                st.write(msg.content)

    @staticmethod
    def chat_input():
        return st.chat_input("Type your message...")
