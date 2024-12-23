# llm-apps
## Setup
1. Get OpenAI API KEY and write it to .env file.
```
# .env
OPENAI_API_KEY=<YOUR_API_KEY>
```

2. Install dependencies
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run server
```
uvicorn src.backend.main:app --reload
```

## Chat
You can chat with OpenAI model.
```
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"human": "What is the capital of Japan?"}'
```

## RAG
### Indexing
You can upload only PDF file. Uploaded file is embedded and stored in chroma.
```
curl -X POST -F "file=@/path/your_file.pdf" -F "chroma_dir=/path/your_dir" http://127.0.0.1:8000/pdf_upload
```

### Retrieval and Generation
```
curl -X POST "http://127.0.0.1:8000/rag" -H "Content-Type: application/json" -d '{"question": "Your question", "chroma_dir": "/path/your_dir"}'
```