from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    GenerateRequest,
    GenerateResponse,
    AgentToolRequest,
    AgentToolResponse,
    HealthResponse,
)
from .pipelines import generate_with_guardrails
from .mcp_agent import agent
from .logging_utils import init_db, list_recent

app = FastAPI(
    title="Cloud-Native LLM Guardrail Pipeline",
    version="0.1.0",
    description="LLM + guardrails + agent tools + logging",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok")


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    return generate_with_guardrails(req)


@app.post("/agent/call", response_model=AgentToolResponse)
def call_agent(req: AgentToolRequest):
    result = agent.call_tool(req.tool_name, req.arguments)
    return AgentToolResponse(tool_name=req.tool_name, result=result)


@app.get("/interactions/recent")
def get_recent_interactions(limit: int = 20):
    return list_recent(limit)
