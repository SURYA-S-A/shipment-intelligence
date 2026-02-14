from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from shipment_intelligence_api.core.settings import settings


def get_llm() -> BaseChatModel:
    """
    Get configured LLM instance.

    Returns:
        BaseChatModel: Initialized LLM
    """
    return init_chat_model(
        model=settings.LLM_MODEL,
        model_provider=settings.LLM_PROVIDER,
        api_key=settings.LLM_API_KEY,
    )
