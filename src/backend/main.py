from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from src.backend.routers import chat, upload


app = FastAPI()
app.include_router(chat.router)
app.include_router(upload.router)
