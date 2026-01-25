from langchain_groq import ChatGroq
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from config import Config


class AIService:
    _llm = None

    @classmethod
    def get_llm(cls):
        if cls._llm is None:
            cls._llm = ChatGroq(
                api_key=Config.GROQ_API_KEY,
                model_name=Config.MODEL_NAME,
                temperature=0.7
            )
        return cls._llm

    @classmethod
    def generate_reply(cls, messages, system_message="You are a helpful AI assistant."):
        """
        messages: List of ChatMessage ORM objects or dicts with 'role' and 'content' keys
        system_message: Custom system message (optional)
        """
        llm = cls.get_llm()

        # ✅ ONLY LangChain message objects go here
        lc_messages = [
            SystemMessage(content=system_message)
        ]

        # OPTIONAL: limit history to last 50 messages for better context
        for msg in messages[-50:]:
            role = msg.role if hasattr(msg, 'role') else msg['role']
            content = msg.content if hasattr(msg, 'content') else msg['content']
            if role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))

        # ✅ THIS is what invoke expects
        response = llm.invoke(lc_messages)

        return response.content
