from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
from pydantic import ConfigDict
from .config import settings


class Interaction(SQLModel, table=True):
    # Prevent Pydantic from warning about "model_id"
    model_config = ConfigDict(protected_namespaces=())

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    prompt: str
    answer: str
    model_id: str

    violates_safety: bool = False
    contains_pii: bool = False
    hallucination_suspected: bool = False
    used_agent_tool: bool = False
    blocked: bool = False

    reasons: str = ""  # semicolon-separated reasons


engine = create_engine(settings.database_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def save_interaction(
    prompt: str,
    answer: str,
    model_id: str,
    flags,
) -> None:
    interaction = Interaction(
        prompt=prompt,
        answer=answer,
        model_id=model_id,
        violates_safety=flags.violates_safety,
        contains_pii=flags.contains_pii,
        hallucination_suspected=flags.hallucination_suspected,
        used_agent_tool=flags.used_agent_tool,
        blocked=flags.blocked,
        reasons="; ".join(flags.reasons),
    )
    with Session(engine) as session:
        session.add(interaction)
        session.commit()


def list_recent(limit: int = 20) -> List[Interaction]:
    with Session(engine) as session:
        stmt = select(Interaction).order_by(Interaction.timestamp.desc()).limit(limit)
        return list(session.exec(stmt))
