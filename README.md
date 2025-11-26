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

## 🌟 Why This Project Matters

This repository demonstrates real-world skills involved in AI engineering:

* Building **production-grade LLM APIs**
* Implementing **custom safety + guardrail systems**
* Using **FastAPI, SQLModel, Pydantic v2, and HuggingFace**
* Designing **modular and extensible AI systems**
* Supporting **agent tool-calling patterns similar to MCP**
