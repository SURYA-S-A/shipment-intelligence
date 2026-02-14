from langchain_core.prompts import ChatPromptTemplate


# System prompt for answering questions based on shipment events
SHIPMENT_QUESTION_ANSWERING_SYSTEM_PROMPT = """You are a shipment intelligence assistant.

You will be provided with shipment event data. Use this information to answer the user's question accurately and concisely.

Guidelines:
- Answer based ONLY on the provided events
- Be specific and cite relevant events when possible
- If the events don't contain enough information to answer, say so clearly
- Keep responses focused and concise

Shipment Events:
{context}
"""


SHIPMENT_QUESTION_ANSWERING_USER_PROMPT = "Question: {question}"


def get_question_answering_prompt() -> ChatPromptTemplate:
    """Get prompt template for question answering over shipment events.

    This is a simple RAG prompt that answers user questions based on
    retrieved shipment event context.

    Returns:
        ChatPromptTemplate: Configured prompt template with context and question variables.
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", SHIPMENT_QUESTION_ANSWERING_SYSTEM_PROMPT),
            ("user", SHIPMENT_QUESTION_ANSWERING_USER_PROMPT),
        ]
    )
