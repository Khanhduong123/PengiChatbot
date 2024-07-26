from datetime import datetime
import hashlib
from typing import List, Optional

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status

from apps.dependencies import document_search
from apps.documents.schemas import ResponseSchema, DocumentQdrantCreate, DocumentQdrantModel, DocumentResponse, DocumentsQdrant
from apps.documents.service import DocumentService


from utils.logging import LOGGER
from utils.utils import get_admin_user


router = APIRouter()
document_service = DocumentService(document_search=document_search)


@router.get("/", response_model=List[DocumentResponse])
async def get_documents(user=Depends(get_admin_user)):
    docs = [
        DocumentResponse(
            **{
                **doc.model_dump()
            }
        )
        for doc in DocumentsQdrant.get_docs()
    ]
    return docs

@router.post("/upload_document", response_model=Optional[DocumentQdrantModel])
async def upload_document(file: UploadFile = File(...), user=Depends(get_admin_user)):
  
    document_data = DocumentQdrantCreate(
        file_name=file.filename,
        file_type=file.content_type.lower(),
        file_status=True,
        created_at=datetime.now(),
        user_id=user.id
    )
    LOGGER.info(document_data)
    doc = DocumentsQdrant.insert_new_doc(document_data)

    await document_service.upload_document(file=file,document_id=doc.id)

    return doc
   




@router.delete("/delete_document", response_model=ResponseSchema)
async def delete_document(document_id: int):
    DocumentsQdrant.delete_doc_by_id(document_id)
    await document_service.delete_document(document_id=document_id)

    return ResponseSchema(message="Delete successfully!")