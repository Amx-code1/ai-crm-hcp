from fastapi import FastAPI
from agent import graph_app
from db import engine
from models import Base, ChatRequest
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.post("/chat")
async def chat(data: ChatRequest):
    res = graph_app.invoke({"input": data.message})
    return {"response": res.get("output")}