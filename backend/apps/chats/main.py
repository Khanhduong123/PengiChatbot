from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from apps.chats.router import router as chat_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthcheck() -> bool:
    return True


app.include_router(chat_router, tags=["Chat"])