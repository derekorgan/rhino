from langchain.chat_models import ChatOpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming import StreamingStdOutCallbackHandler
from app.core.config import get_settings

class LLMService:
    """Base LLM service configuration"""
    
    def __init__(self):
        self.settings = get_settings()
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4",
            openai_api_key=self.settings.OPENAI_API_KEY,
            callback_manager=self.callback_manager,
            streaming=True
        )
    
    @property
    def get_llm(self):
        return self.llm
