# 🚀 LLM Guardrail Inference Pipeline

*A lightweight, production-ready backend for secure LLM inference, fully open-source.*

This project implements a modern LLM backend featuring:

* 🧠 **LLM text generation** using HuggingFace Transformers
* 🔐 **Safety guardrails**: PII detection, harmful content filtering, hallucination heuristics
* 📦 **Structured outputs** with Pydantic v2
* 🤖 **Agent tool-calling** (“MCP-style”) — includes a real working UTC-time tool
* 🗄️ **Persistent interaction logging** via SQLModel + SQLite
* ⚡ **FastAPI REST API** with full Swagger / OpenAPI documentation
* 🔧 **Configurable model loading** (TinyLlama, Phi-2, Phi-1.5 Mini, etc.)

This serves as a **lightweight open-source alternative** to:
GuardrailsAI • OpenAI Moderation • Anthropic Constitutional AI
…but implemented fully from scratch for transparency, learning, and extensibility.

---

## ✨ Key Features

### 🧠 1. HuggingFace LLM Text Generation

* Supports any open HuggingFace causal model
* TinyLlama (default), Phi-2, Phi-1.5 Mini, GPT-like endpoints
* Clean generation pipeline with temperature, top-k, max tokens

### 🔐 2. Custom Guardrail System

Includes:

* PII detectors (regex-based)
* Unsafe-content filters
* Hallucination heuristics (unverifiable citations, fake references)
* Unified `GuardrailFlags` schema for downstream consumption

### 🤖 3. Agent Tool-Calling (“MCP Style”)

* Pluggable tools
* Example: UTC Time Lookup
* Framework ready for additional tools (web search, DB query, file ops, etc.)

### 🗄️ 4. Persistent Logging

* Uses **SQLModel + SQLite**
* Stores prompts, responses, guardrail triggers, timestamps, and model metadata
* Perfect for dashboards, RLHF datasets, or audits

### ⚡ 5. FastAPI Backend with Auto Docs

Once running:

* **Swagger UI:**
  👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* **OpenAPI schema:**
  👉 [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## ⚙️ Installation Guide

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/LLM-Guardrail-Pipeline.git
cd LLM-Guardrail-Pipeline
```

### 2️⃣ Create & activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

**Optional: Enable GPU/MPS acceleration**

```bash
pip install "accelerate>=0.26.0"
```

---

## ▶️ Running the Server

Start the API server:

```bash
uvicorn app.main:app --reload
```

Server will be live at:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧩 Project Structure

```
app/
 ├── main.py               # FastAPI entry point
 ├── pipelines.py          # LLM generation + guardrail integration
 ├── guardrails.py         # Safety filtering, PII, hallucinations
 ├── schemas.py            # Pydantic models (requests/responses)
 ├── mcp_agent.py          # Tool-calling agent
 └── logging_utils.py      # SQLModel/SQLite persistence
```

---

# 🐳 **Deploying with Docker (Production-Ready)**

This project ships with a **production-grade Docker image** supporting FastAPI, SQLModel, HuggingFace Transformers, and optional MPS acceleration (Mac M1/M2/M3).
The container is optimized using:

* Slim Python 3.12 base
* Multi-stage caching
* No pip cache
* `.dockerignore` to reduce image bloat
* Uvicorn with multiple workers for production

---

## **1. Build the Docker Image**

From the project root:

```bash
docker build -t llm-guardrails .
```

This will:

* Install system dependencies
* Install Python dependencies
* Copy your application code
* Expose port 8000
* Configure the production Uvicorn entrypoint

---

## **2. Run the Container**

You must pass your `.env` file so the API can load your model:

```bash
docker run -p 8000:8000 --env-file .env llm-guardrails
```

Now your API is live at:

* **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** → Swagger UI
* **[http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)** → OpenAPI schema

---

## **3. Using the API in Production**

A typical request:

```json
POST /generate
{
  "prompt": "Explain reinforcement learning in one sentence.",
  "max_new_tokens": 60,
  "temperature": 0.7
}
```

You can call it from curl:

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain RL in one sentence."}'
```

---

## **4. Local Development with Hot Reload (docker-compose)**

If you want the server to auto-reload on code changes:

Create `docker-compose.yaml`:

```yaml
version: "3.9"

services:
  api:
    build: .
    container_name: llm_guardrails
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Run:

```bash
docker compose up
```

Now you can iterate locally while still inside Docker.

---

## **5. Dockerfile (Included)**

A clean, optimized production Dockerfile is included:

```dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

---

## **6. `.dockerignore` (Included)**

This keeps your image small and prevents leaking secrets:

```
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
.env
.git/
.gitignore
.cache/
.idea/
.DS_Store
models/
huggingface/
```

---

## **7. Notes for Mac M1/M2/M3 Users (MPS Acceleration)**

Macs with Apple Silicon can run HuggingFace models with hardware acceleration via MPS.

To enable (optional):

Modify your requirements:

```
pip install torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu
```

Transformers will pick up MPS automatically inside or outside Docker.

---

## 🌟 Why This Project Matters

This repository demonstrates real-world skills involved in AI engineering:

* Building **production-grade LLM APIs**
* Implementing **custom safety + guardrail systems**
* Using **FastAPI, SQLModel, Pydantic v2, and HuggingFace**
* Designing **modular and extensible AI systems**
* Supporting **agent tool-calling patterns similar to MCP**
