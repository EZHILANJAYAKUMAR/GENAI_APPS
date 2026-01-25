import streamlit as st
from models import User
from controllers.auth_controller import AuthController

class ChatView:

    @staticmethod
    def sidebar(chats, new_chat_cb, select_cb, rename_cb, delete_cb):
        with st.sidebar:
            st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                width: 350px !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Profile Section
            if 'user_full_name' not in st.session_state or st.session_state.user_full_name is None:
                # Fetch from DB if not in session
                db = AuthController.get_db()
                user = db.query(User).filter(User.id == st.session_state.user_id).first()
                db.close()
                if user and user.full_name:
                    st.session_state.user_full_name = user.full_name
            st.image(f"https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg", width=100)
            user_name = st.session_state.get('user_full_name')
            st.write("**Welcome, {}!**".format(user_name.replace('%20', ' ')))
            st.divider()

            st.button("➕ New Chat", on_click=new_chat_cb)
            st.divider()

            for chat in chats:
                title_display = chat.title if len(chat.title) <= 30 else chat.title[:27] + "..."
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
                elif "confirm_delete" in st.session_state and st.session_state.confirm_delete == chat.id:
                    # Show delete confirmation
                    st.warning(f"Delete '{title_display}'?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes", key=f"confirm_delete_{chat.id}"):
                            delete_cb(chat.id)
                            del st.session_state.confirm_delete
                            st.rerun()
                    with col2:
                        if st.button("No", key=f"cancel_delete_{chat.id}"):
                            del st.session_state.confirm_delete
                            st.rerun()
                else:
                    # Normal chat display
                    title_display = chat.title if len(chat.title) <= 20 else chat.title[:17] + "..."
                    col1, col2, col3 = st.columns([6, 2, 2])
                    with col1:
                        if st.button(title_display, key=f"select_{chat.id}", help=chat.title):
                            select_cb(chat.id)
                    with col2:
                        if st.button("✏️", key=f"edit_{chat.id}"):
                            st.session_state.editing_chat_id = chat.id
                            st.rerun()
                    with col3:
                        if st.button("🗑️", key=f"delete_{chat.id}"):
                            st.session_state.confirm_delete = chat.id
                            st.rerun()

    @staticmethod
    def render_messages(messages):
        for msg in messages:
            if msg.role == "user":
                # User message on the right
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.empty()
                with col2:
                    with st.chat_message("user"):
                        st.write(msg.content)
            else:
                # Assistant message on the left
                col1, col2 = st.columns([1, 1])
                with col1:
                    with st.chat_message("assistant"):
                        st.write(msg.content)
                with col2:
                    st.empty()

    @staticmethod
    def chat_input():
        return st.chat_input("Type your message...")
