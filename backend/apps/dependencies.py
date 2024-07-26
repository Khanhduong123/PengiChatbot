from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

from config import settings
from apps.documents.config import document_config
from apps.documents.searcher import DocumentSearch

client_qdrant = QdrantClient(
    url=settings.QDRANT_URL, prefer_grpc=True, api_key=settings.QDRANT_KEY
)

embeddings_document_model = OpenAIEmbeddings(
    model=document_config.EMBEDDING_MODEL, dimensions=document_config.EMBEDDING_DIM
)

document_search = DocumentSearch(
    client_qdrant=client_qdrant, model=embeddings_document_model
)