from apps.chats.config import chat_config
from apps.dependencies import document_search
from utils.logging import LOGGER

class DocumentRetrieval:
    @staticmethod
    async def get_relevant_document(question):
        relevant_docs = await document_search.search(
            question=question, top_k=chat_config.DOCUMENT_TOP_K
        )

        query_context = ""
        for document in relevant_docs:
            query_context += document["content"] + "\n\n"

        rel_doc = [
            {
                "page": doc["page"],
                "document_name": doc["document_name"],
                "document_id": doc["document_id"],
                "content": doc["content"],
            }
            for doc in relevant_docs
        ]
        return {"context": query_context, "relevant_docs": rel_doc}

    @staticmethod
    def get_relevant_document_sync(question):
        relevant_docs = document_search.search_sync(
            question=question, top_k=chat_config.DOCUMENT_TOP_K
        )

        query_context = ""
        for document in relevant_docs:
            query_context += document["content"] + "\n\n"

        rel_doc = [
            {
                "page": doc["page"],
                "document_name": doc["document_name"],
                "document_id": doc["document_id"],
                "content": doc["content"],
            }
            for doc in relevant_docs
        ]
        return {"context": query_context, "relevant_docs": rel_doc}
