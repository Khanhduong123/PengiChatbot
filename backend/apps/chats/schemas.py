from typing import List

from pydantic import BaseModel


class ReferenceSchema(BaseModel):
    document_id: int
    document_name: str
    content: str
    page: int


class RequestSchema(BaseModel):
    question: str


class StreamingRequestSchema(BaseModel):
    question: str


class ResponseSchema(BaseModel):
    question: str
    answer: str
    relevant_docs: List[ReferenceSchema]

