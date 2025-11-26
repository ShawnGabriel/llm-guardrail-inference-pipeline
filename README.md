This project implements a production-ready LLM backend that performs:
- LLM text generation using HuggingFace Transformers
- Safety guardrails (PII detection, harmful content, hallucination heuristics)
- Structured schema responses using Pydantic v2
- Agent tool-calling (e.g., time lookup)
- Persistent logging with SQLModel + SQLite
- FastAPI REST API with automatic Swagger docs
- Configurable model loading (TinyLlama, Phi-2, GPT-like endpoints, etc.)
It is a lightweight open-source alternative to tools like Guardrails AI, OpenAI moderation, or Anthropic Constitutional AI, but fully implemented from scratch.

🚀 Features
1. HuggingFace LLM Text Generation
2. Custom Guardrail System
3. Agent Tool-Calling ("MCP-Style")
4. Persistent Logging (SQLModel + SQLite)
5. FastAPI Backend with Auto Docs
Once the server runs:
👉 Swagger UI
http://127.0.0.1:8000/docs
👉 OpenAPI schema
http://127.0.0.1:8000/openapi.json

⚙️ Installation
1. Clone the project
git clone https://github.com/YOUR_USERNAME/LLM-Guardrail-Pipeline.git
cd LLM-Guardrail-Pipeline
2. Create & activate environment
python3 -m venv .venv
source .venv/bin/activate
3. Install requirements
pip install -r requirements.txt
(Optional) Install Accelerate for GPU/MPS:
pip install "accelerate>=0.26.0"

Running the Server
uvicorn app.main:app
