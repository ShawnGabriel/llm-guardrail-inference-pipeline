from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="User query or instruction")
    max_new_tokens: int = Field(default=128, ge=1, le=512)
    enable_agent: bool = Field(default=False, description="Allow agent tool calls")
    temperature: float = Field(default=0.7, ge=0.0, le=1.5)


class GuardrailFlags(BaseModel):
    violates_safety: bool = False
    contains_pii: bool = False
    hallucination_suspected: bool = False
    used_agent_tool: bool = False
    blocked: bool = False
    reasons: List[str] = []


class GenerateResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    answer: str
    reasoning_trace: Optional[str] = None
    flags: GuardrailFlags
    model_id: str
    latency_ms: int
    agent_tool_called: Optional[str] = None


class AgentToolRequest(BaseModel):
    tool_name: str
    arguments: dict


class AgentToolResponse(BaseModel):
    tool_name: str
    result: dict


class HealthResponse(BaseModel):
    status: str = "ok"
