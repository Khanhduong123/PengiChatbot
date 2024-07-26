import uuid
from qdrant_client import QdrantClient, grpc
from tqdm import tqdm

from apps.documents.config import document_config

from utils.logging import LOGGER

class DocumentSearch:
    def __init__(self, client_qdrant: QdrantClient, model):
        self.client_grpc = client_qdrant
        self.embeddings_model = model
        self.collection_name = document_config.COLLECTION_NAME
        self.vector_size = document_config.EMBEDDING_DIM
        self.batch_size = document_config.BATCH_SIZE

        if self.check_collection() is False:
            LOGGER.info(f"Create {document_config.COLLECTION_NAME} collection!")
            self.create_collection()

        LOGGER.info("Init document searcher")

    def create_collection(self):
        response = self.client_grpc.grpc_collections.Create(
            grpc.CreateCollection(
                collection_name=self.collection_name,
                vectors_config=grpc.VectorsConfig(
                    params=grpc.VectorParams(
                        size=self.vector_size,
                        distance=grpc.Distance.Cosine,
                    )
                ),
                timeout=10,
            )
        )

        return response

    def check_collection(self):
        response = self.client_grpc.collection_exists(
            collection_name=self.collection_name
        )

        return response

    def add_patching_points(self, list_chunks):
        num_features = len(list_chunks)
        num_batches = (num_features + self.batch_size - 1) // self.batch_size

        for i in tqdm(range(num_batches)):
            # Split into batches
            start_idx = i * self.batch_size
            end_idx = min((i + 1) * self.batch_size, num_features)

            ids = [str(uuid.uuid4()) for _ in range(start_idx, end_idx)]
            payload = list_chunks[start_idx:end_idx]

            list_content = [doc["content"] for doc in payload]
            vectors = self.embeddings_model.embed_documents(list_content)

            self.client_grpc.upload_collection(
                collection_name=self.collection_name,
                vectors=vectors,
                payload=payload,
                ids=ids,
            )

    async def search(self, question, top_k=2):
        vectors = self.embeddings_model.embed_documents([question])

        response = await self.client_grpc.async_grpc_points.Search(
            grpc.SearchPoints(
                collection_name=self.collection_name,
                vector=vectors[0],
                limit=top_k,
                with_payload=grpc.WithPayloadSelector(enable=True),
            )
        )

        results = []
        for data in response.result:
            results.append(
                {
                    "score": data.score,
                    "content": data.payload["content"].string_value,
                    "document_name": data.payload["document_name"].string_value,
                    "document_id": data.payload["document_id"].integer_value,
                    "page": data.payload["page"].integer_value,
                }
            )

        # print(results)
        return results

    def search_sync(self, question, top_k=2):
        vectors = self.embeddings_model.embed_documents([question])

        response = self.client_grpc.grpc_points.Search(
            grpc.SearchPoints(
                collection_name=self.collection_name,
                vector=vectors[0],
                limit=top_k,
                with_payload=grpc.WithPayloadSelector(enable=True),
            )
        )

        results = []
        for data in response.result:
            results.append(
                {
                    "score": data.score,
                    "content": data.payload["content"].string_value,
                    "document_name": data.payload["document_name"].string_value,
                    "document_id": data.payload["document_id"].integer_value,
                    "page": data.payload["page"].integer_value,
                }
            )

        # print(results)
        return results

    async def delete_document(self, document_id):
        points = grpc.PointsSelector(
            filter=grpc.Filter(
                must=[
                    grpc.Condition(
                        field=grpc.FieldCondition(
                            key="document_id", match=grpc.Match(integer=document_id)
                        )
                    )
                ]
            )
        )

        response = await self.client_grpc.async_grpc_points.Delete(
            grpc.DeletePoints(collection_name=self.collection_name, points=points)
        )

        # print(response)

        return response