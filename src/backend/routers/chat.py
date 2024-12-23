from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
import os
from pydantic import BaseModel
import textwrap

router = APIRouter()

load_dotenv()
model = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

class UserMessage(BaseModel):
    system: str = "Please answer in 50 words or less."
    human: str

class RagInput(BaseModel):
    question: str
    chroma_dir: str
    system: str = "Please answer in 50 words or less."

@router.post("/chat")
async def chat(user_message: UserMessage):
    messages = [
        SystemMessage(user_message.system), 
        HumanMessage(user_message.human),
    ]
    return {"message": model.invoke(messages).content}

@router.post("/rag")
async def rag(rag_input: RagInput):
    if not os.path.exists(rag_input.chroma_dir):
        raise HTTPException(status_code=404, detail="chroma_dir does not exists")
    
    template = textwrap.dedent("""
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum and keep the answer as concise as possible.
        
        {context}
        
        Question: {question}
        
        Helpful Answer:
    """.strip())

    # Retrieval
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=rag_input.chroma_dir,
    )
    retrieved_docs = await vector_store.asimilarity_search(rag_input.question, k=3)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Generation
    prompt_template = PromptTemplate.from_template(template)
    prompt = prompt_template.format(context=context, question=rag_input.question)

    messages = [
        SystemMessage(rag_input.system),
        HumanMessage(prompt),
    ]
    return {"message": model.invoke(messages).content}