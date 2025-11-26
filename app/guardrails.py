import re
from typing import Tuple
from .schemas import GuardrailFlags


# Simple example categories of disallowed content
DISALLOWED_KEYWORDS = [
    "kill yourself",
    "how to make a bomb",
    "child pornography",
    "credit card full number",
]


PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),           # phone-like
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),           # SSN-like
    re.compile(r"\b\d{16}\b"),                      # 16-digit string
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+"),  # email
]


def check_content_policy(text: str) -> Tuple[bool, str]:
    lowered = text.lower()
    for kw in DISALLOWED_KEYWORDS:
        if kw in lowered:
            return True, f"Blocked due to disallowed content: '{kw}'"
    return False, ""


def check_pii(text: str) -> Tuple[bool, str]:
    for pattern in PII_PATTERNS:
        if pattern.search(text):
            return True, "Potential PII detected."
    return False, ""


def detect_hallucination(prompt: str, answer: str) -> Tuple[bool, str]:
    hallucination_keywords = [
        "as cited in",
        "according to the study by",
        "source:",
        "reference:"
    ]
    if any(kw in answer.lower() for kw in hallucination_keywords) and "http" not in answer:
        return True, "Answer appears to reference unverifiable sources."
    return False, ""


def apply_guardrails(prompt: str, answer: str) -> GuardrailFlags:
    violates_safety, safety_reason = check_content_policy(answer)
    pii_found, pii_reason = check_pii(answer)
    hallucination_suspected, halluc_reason = detect_hallucination(prompt, answer)

    reasons = []
    if safety_reason:
        reasons.append(safety_reason)
    if pii_reason:
        reasons.append(pii_reason)
    if halluc_reason:
        reasons.append(halluc_reason)

    blocked = violates_safety or pii_found

    return GuardrailFlags(
        violates_safety=violates_safety,
        contains_pii=pii_found,
        hallucination_suspected=hallucination_suspected,
        used_agent_tool=False,
        blocked=blocked,
        reasons=reasons,
    )
