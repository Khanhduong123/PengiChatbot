from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from apps.chats.naive_rag.pipeline import NaiveRAGPipeline
from apps.chats.schemas import (
    RequestSchema,
    ResponseSchema,
    StreamingRequestSchema,
)

router = APIRouter()

pipeline = NaiveRAGPipeline()


@router.post("/get_answer", response_model=ResponseSchema)
async def get_answer(data: RequestSchema):
    result = await pipeline.execute(
        question=data.question,
    )

    return result


@router.post("/get_answer_streaming", response_class=StreamingResponse)
async def get_answer_streaming(data: StreamingRequestSchema):
    generator = pipeline.execute_streaming(
        question=data.question,
    )

    return StreamingResponse(generator, media_type="text/event-stream")
