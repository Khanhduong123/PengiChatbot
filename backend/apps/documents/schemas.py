from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from peewee import *
from apps.webui.internal.db import DB
from playhouse.shortcuts import model_to_dict

class ResponseSchema(BaseModel):
    message: str


class DeleteSchema(BaseModel):
    document_name: str
    
    
class ReferenceDocumentQdrant(Model):
    content = TextField(null=True)
    document_name = CharField(unique=True)
    page = IntegerField()
    message_id = IntegerField()
    document_id = IntegerField()
    class Meta:
        database = DB

class DocumentQdrant(Model):
    file_name = TextField()
    file_type = TextField()
    file_status = BooleanField()
    user_id = CharField()
    created_at = DateTimeField()

    class Meta:
        database = DB

class ReferenceDocumentQdrantBase(BaseModel):
    content: Optional[str]
    document_name: str
    page: int
    message_id: int
    document_id: int

class ReferenceDocumentQdrantCreate(ReferenceDocumentQdrantBase):
    pass
class ReferenceDocumentQdrantModel(ReferenceDocumentQdrantBase):
    id: int
    
class DocumentQdrantBase(BaseModel):
    file_name: str
    file_type: str
    file_status: bool
    created_at: datetime
    user_id: str

class DocumentQdrantCreate(DocumentQdrantBase):
    pass

class DocumentQdrantModel(DocumentQdrantBase):
    id: int
    reference_documents: List[ReferenceDocumentQdrantModel] = []

class DocumentQdrantUpdateForm(BaseModel):
    file_name: Optional[str]
    file_type: Optional[str]
    file_status: Optional[bool]
    user_id: Optional[int]
    
    
    
####################
# Forms
####################
class DocumentResponse(BaseModel):
    file_name: str
    file_type: str
    file_status: bool
    created_at: datetime
    user_id: str



class DocumentsQdrantTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([DocumentQdrant])

    def insert_new_doc(self,  document_data: DocumentQdrantCreate) -> Optional[DocumentQdrantModel]:
        try:
            result = DocumentQdrant.create(**document_data.model_dump())
            if result:
                return result
            else:
                return None
        except:
            return None
    def delete_doc_by_id(self, id: int) -> bool:
        try:
            query = DocumentQdrant.delete().where((DocumentQdrant.id == id))
            query.execute()

            return True
        except:
            return False

    def get_docs(self) -> List[DocumentQdrantModel]:
        return [
            DocumentQdrantModel(**model_to_dict(doc))
            for doc in DocumentQdrant.select()
        ]

DocumentsQdrant = DocumentsQdrantTable(DB)