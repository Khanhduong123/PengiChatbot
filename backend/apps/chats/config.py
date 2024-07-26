from pydantic_settings import BaseSettings


class ChatConfig(BaseSettings):
    DOCUMENT_EMBEDDING_DIM: int = 384
    DOCUMENT_THRESHOLD: float = 0.85
    DOCUMENT_TOP_K: int = 3
    FAQ_THRESHOLD: float = 0.85
    MODEL_GPT: str = "gpt-3.5-turbo"
    TEMPERATURE: float = 0
    PROMPT_NOT_FOUND: str = (
        "I apologize, the documents do not seem to contain any data related to the question. "
        "You can ask other questions related to the documents."
    )



chat_config = ChatConfig()
