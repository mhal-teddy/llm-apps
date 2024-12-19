from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

class UserMessage(BaseModel):
    system: str = "Please answer in 50 words or less."
    human: str

app = FastAPI()

model = ChatOpenAI(model="gpt-4o-mini")

@app.post("/chat")
async def chat(user_message: UserMessage):
    messages = [
        SystemMessage(user_message.system), 
        HumanMessage(user_message.human),
    ]
    return {"message": model.invoke(messages).content}
