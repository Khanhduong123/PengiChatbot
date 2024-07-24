from pydantic import BaseModel
from peewee import *
from playhouse.shortcuts import model_to_dict
from typing import List, Union, Optional
import time
import logging

from utils.utils import decode_token
from utils.misc import get_gravatar_url

from apps.webui.internal.db import DB

import json

from config import SRC_LOG_LEVELS, CHROMA_CLIENT

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Documents DB Schema
####################

class Document(Model):
    collection_name = CharField()
    name = CharField(unique=True)
    title = TextField()
    filename = TextField()
    content = TextField(null=True)
    user_id = CharField()
    timestamp = BigIntegerField()

    class Meta:
        database = DB


class DocumentModel(BaseModel):
    collection_name: str
    name: str
    title: str
    filename: str
    content: Optional[str] = None
    user_id: str
    timestamp: int  # timestamp in epoch


# ####################
# # Forms
# ####################


class DocumentResponse(BaseModel):
    collection_name: str
    name: str
    title: str
    filename: str
    content: Optional[dict] = None
    user_id: str
    timestamp: int  # timestamp in epoch


class DocumentUpdateForm(BaseModel):
    name: str
    title: str


class DocumentForm(DocumentUpdateForm):
    collection_name: str
    filename: str
    content: Optional[str] = None


class DocumentsTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([Document])

    def insert_new_doc(
        self, user_id: str, form_data: DocumentForm
    ) -> Optional[DocumentModel]:
        document = DocumentModel(
            **{
                **form_data.model_dump(),
                "user_id": user_id,
                "timestamp": int(time.time()),
            }
        )

        try:
            result = Document.create(**document.model_dump())
            if result:
                return document
            else:
                return None
        except:
            return None

    def get_doc_by_name(self, name: str) -> Optional[DocumentModel]:
        try:
            document = Document.get(Document.name == name)
            return DocumentModel(**model_to_dict(document))
        except:
            return None

    def get_docs(self) -> List[DocumentModel]:
        return [
            DocumentModel(**model_to_dict(doc))
            for doc in Document.select()
            # .limit(limit).offset(skip)
        ]

    def update_doc_by_name(
        self, name: str, form_data: DocumentUpdateForm
    ) -> Optional[DocumentModel]:
        try:
            query = Document.update(
                title=form_data.title,
                name=form_data.name,
                timestamp=int(time.time()),
            ).where(Document.name == name)
            query.execute()

            doc = Document.get(Document.name == form_data.name)
            return DocumentModel(**model_to_dict(doc))
        except Exception as e:
            log.exception(e)
            return None

    def update_doc_content_by_name(
        self, name: str, updated: dict
    ) -> Optional[DocumentModel]:
        try:
            doc = self.get_doc_by_name(name)
            doc_content = json.loads(doc.content if doc.content else "{}")
            doc_content = {**doc_content, **updated}

            query = Document.update(
                content=json.dumps(doc_content),
                timestamp=int(time.time()),
            ).where(Document.name == name)
            query.execute()

            doc = Document.get(Document.name == name)
            return DocumentModel(**model_to_dict(doc))
        except Exception as e:
            log.exception(e)
            return None

    def delete_doc_by_name(self, name: str) -> bool:
        try:
            query = Document.delete().where((Document.name == name))
            query.execute()  # Remove the rows, return number of rows removed.

            return True
        except:
            return False
    def get_all_collection_names(self) -> List[str]:
        try:
            query = Document.select(Document.collection_name).distinct()
            return [doc.collection_name for doc in query]
        except Exception as e:
            log.exception(e)
            return []
    def get_relevant_document(self, query: str, embedding_function, k: int):
        try:
            query_embedding = embedding_function(query)
            results = []
            query_context = ""
            
            # for collection_name in collection_names:
            collection = CHROMA_CLIENT.get_collection(name="PengiCollection")
            result = collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
            )
            log.info(result)
            if 'ids' in result and 'distances' in result and 'metadatas' in result and 'documents' in result:
                for idx, doc_id in enumerate(result['ids'][0]):
                    metadata = result['metadatas'][0][idx]
                    document_content = result['documents'][0][idx]
                    
                    query_context += document_content + "\n\n"
                    
                    results.append({
                        "page": metadata['page'],
                        "document_name": metadata['source'],
                        "document_id": doc_id,
                        "content": document_content,
                    })
            return {"context": query_context.strip(), "relevant_docs": results}
        except Exception as e:
            log.exception(e)
            return None

Documents = DocumentsTable(DB)
