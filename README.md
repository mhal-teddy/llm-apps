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