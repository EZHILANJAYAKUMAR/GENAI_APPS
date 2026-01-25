from db import SessionLocal
from models import ChatSession, ChatMessage
from services.ai_services import AIService

class ChatController:

    # ---------- DB ----------
    @staticmethod
    def get_db():
        return SessionLocal()

    # ---------- CHAT SESSION ----------
    @staticmethod
    def get_latest_chat(user_id):
        db = ChatController.get_db()
        chat = (
            db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.created_at.desc())
            .first()
        )
        db.close()
        return chat

    @staticmethod
    def get_all_chats(user_id):
        db = ChatController.get_db()
        chats = (
            db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.created_at.desc())
            .all()
        )
        db.close()
        return chats

    @staticmethod
    def create_chat(user_id):
        db = ChatController.get_db()
        chat = ChatSession(
            user_id=user_id,
            title="New Chat"
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)
        db.close()
        return chat

    @staticmethod
    def rename_chat(chat_id, title):
        db = ChatController.get_db()
        chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()

        if chat:
            chat.title = title
            db.commit()

        db.close()

    # ---------- MESSAGES ----------
    @staticmethod
    def get_messages(chat_id):
        db = ChatController.get_db()
        msgs = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == chat_id)
            .order_by(ChatMessage.created_at)
            .all()
        )
        db.close()
        return msgs

    @staticmethod
    def add_message(chat_id, role, content):
        db = ChatController.get_db()
        msg = ChatMessage(
            session_id=chat_id,
            role=role,
            content=content
        )
        db.add(msg)
        db.commit()
        db.close()

    @staticmethod
    def generate_ai_reply(chat_id):
        messages = ChatController.get_messages(chat_id)
        print("Generating AI reply for messages:", messages)
        return AIService.generate_reply(messages)

