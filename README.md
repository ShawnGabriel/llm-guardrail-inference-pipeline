# **LLM Guardrail Inference Pipeline**

A production-ready **generative AI inference service** built with FastAPI, HuggingFace, PyTorch, SQLModel, and Docker—featuring configurable LLM generation, enterprise-grade safety guardrails, and MCP-style tool calling.

This project serves as an open-source alternative to GuardrailsAI, OpenAI Moderation APIs, and Anthropic Constitutional AI, offering a fully transparent and customizable implementation.

---

## 🚀 **Key Features**

### **1. Pluggable HuggingFace LLM Inference**

Supports multiple decoder-only LLMs (TinyLlama, Phi-2, Llama, GPT-style), with:

* Temperature sampling
* Max token limits
* MPS/GPU acceleration
* Safe fallback behavior

---

### **2. PyTorch-Based AI Safety Guardrails**

Custom safety framework built in PyTorch:

* **Toxicity classifier**
* **Hallucination similarity scoring**
* **PII pattern detection**
* **Response blocking with reasons**

Designed for enterprise-grade validation, security, and compliance.

---

### **3. MCP-Style Agent Tool Calling**

Supports deterministic tool execution (e.g., UTC time lookup).
Prevents unsafe or hallucinated tool usage by:

* Explicit prompts
* Deterministic routing
* Structured tool responses

---

### **4. Persistent Telemetry & Logging**

Using SQLModel + SQLite, the server logs:

* Prompts
* Model responses
* Guardrail flags
* Similarity + toxicity metrics
* Latency
* Model ID

Enables evaluation, monitoring, and future fine-tuning.

---

### **5. FastAPI Backend with Auto-Docs**

* `/generate` endpoint
* Swagger UI (`/docs`)
* OpenAPI schema (`/openapi.json`)

---

### **6. Production-Ready Docker Container**

Includes:

* Optimized `Dockerfile`
* `.dockerignore` to exclude checkpoints, datasets, caches
* Reproducible builds

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/llm-guardrail-inference-pipeline.git
cd llm-guardrail-inference-pipeline
```

### Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Optional (GPU/MPS Acceleration)

```bash
pip install "accelerate>=0.26.0"
```

---

## ▶️ Run the server

```bash
uvicorn app.main:app
```

### Swagger docs

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Running with Docker

```bash
docker build -t llm-guardrails .
docker run -p 8000:8000 llm-guardrails
```
