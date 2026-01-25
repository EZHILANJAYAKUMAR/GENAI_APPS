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
    def generate_reply(cls, db_messages):
        """
        db_messages: List[ChatMessage ORM objects]
        """
        llm = cls.get_llm()

        # ✅ ONLY LangChain message objects go here
        lc_messages = [
            SystemMessage(content="You are a helpful AI assistant.")
        ]

        # OPTIONAL: limit history
        for msg in db_messages[-10:]:
            if msg.role == "user":
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                lc_messages.append(AIMessage(content=msg.content))

        # ✅ THIS is what invoke expects
        response = llm.invoke(lc_messages)

        return response.content
