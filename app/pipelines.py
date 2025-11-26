import time
from typing import Optional, Tuple
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from .config import settings
from .schemas import GenerateRequest, GenerateResponse, GuardrailFlags
from .guardrails import apply_guardrails
from .mcp_agent import agent
from .logging_utils import save_interaction

_model_id = settings.llm_model_id

device = "mps" if torch.backends.mps.is_available() else "cpu"

_tokenizer = AutoTokenizer.from_pretrained(_model_id)

_model = AutoModelForCausalLM.from_pretrained(
    _model_id,
    torch_dtype=torch.float16 if device == "mps" else torch.float32,
)

_model.to(device)

_generator = pipeline(
    "text-generation",
    model=_model,
    tokenizer=_tokenizer,
    device=device
)



device = "mps" if torch.backends.mps.is_available() else "cpu"

_generator = pipeline(
    "text-generation",
    model=_model,
    tokenizer=_tokenizer,
    device_map="mps",   # Force all layers on GPU
)


def generate_raw_answer(prompt: str, max_new_tokens: int, temperature: float) -> str:
    output = _generator(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        num_return_sequences=1,
        pad_token_id=_tokenizer.eos_token_id,
    )
    return output[0]["generated_text"]


def maybe_call_agent(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    lower = prompt.lower()
    if "current time" in lower or "what time is it" in lower:
        result = agent.call_tool("get_time_utc", {})
        return "get_time_utc", f"The current UTC time (via tool) is {result['utc_time']}."
    return None, None


def generate_with_guardrails(req: GenerateRequest) -> GenerateResponse:
    start = time.time()

    tool_name, tool_result_text = (None, None)

    # Agent call
    if req.enable_agent:
        tool_name, tool_result_text = maybe_call_agent(req.prompt)

    if tool_result_text is not None:
        # tool was used
        final_answer = tool_result_text

        flags = GuardrailFlags(
            violates_safety=False,
            contains_pii=False,
            hallucination_suspected=False,
            used_agent_tool=True,
            blocked=False,
            reasons=[]
        )

    else:
        # Model generation
        raw_answer = generate_raw_answer(
            req.prompt,
            max_new_tokens=req.max_new_tokens,
            temperature=req.temperature,
        )

        # Apply guardrails (returns ONLY flags)
        flags = apply_guardrails(req.prompt, raw_answer)

        final_answer = raw_answer

        # Log
        save_interaction(
            prompt=req.prompt,
            answer=final_answer,
            model_id=_model_id,
            flags=flags,
        )

    latency = time.time() - start

    return GenerateResponse(
        answer=final_answer,
        reasoning_trace=None,
        flags=flags,
        model_id=_model_id,
        latency_ms=int(latency * 1000),
        agent_tool_called=tool_name,
    )
