from dotenv import load_dotenv
from fastapi import APIRouter, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import tempfile

router = APIRouter()

load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

@router.post("/pdf_upload")
async def pdf_upload(file: UploadFile, chroma_dir: str = Form()):
    # load
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code="400", detail="Only PDF file is allowed.")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(await file.read())
            file_path = f.name

        loader = PyPDFLoader(file_path)
        docs = loader.load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.unlink(file_path)

    # text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True,
    )
    all_splits = text_splitter.split_documents(docs)

    # vector store
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=chroma_dir,
    )
    vector_store.add_documents(documents=all_splits)
    
    return JSONResponse(status_code=204, content=None)