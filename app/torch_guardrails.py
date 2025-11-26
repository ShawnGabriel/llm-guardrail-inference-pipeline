import re
from typing import Optional, Tuple

try:
    import torch
    from torch import nn
except ImportError:
    # Fallback mode: PyTorch not installed, functions will no-op
    torch = None
    nn = None


_TOKEN_PATTERN = re.compile(r"\w+")

# Small vocabulary with some "risky" words so the model isn't totally random
_BASE_VOCAB = [
    "the", "a", "an", "you", "i", "we", "they", "to", "and", "of", "in", "for", "on",
    "kill", "hate", "bomb", "attack", "suicide", "weapon", "drugs", "steal", "fraud",
    "credit", "card", "social", "security", "ssn", "password", "secret",
]

_VOCAB = {tok: idx for idx, tok in enumerate(_BASE_VOCAB)}
_VOCAB_SIZE = len(_VOCAB)
_EMBED_DIM = 32


def _tokenize(text: str):
    return _TOKEN_PATTERN.findall(text.lower())


class TinyTextEncoder(nn.Module):
    """
    Very small text encoder:
      - Embeds tokens
      - Averages embeddings
      - Projects through a tanh layer
    """

    def __init__(self, vocab_size: int, embed_dim: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, indices: torch.Tensor) -> torch.Tensor:
        # indices: (N,)
        embedded = self.embedding(indices)  # (N, D)
        pooled = embedded.mean(dim=0)       # (D,)
        return torch.tanh(self.proj(pooled))


class TorchGuardrailModel:
    """
    Tiny PyTorch model used for:
      - Toxicity scoring (Option A)
      - Prompt–answer similarity (Option C)
    """

    def __init__(self):
        self.enabled = torch is not None and nn is not None
        if not self.enabled:
            return

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.encoder = TinyTextEncoder(_VOCAB_SIZE, _EMBED_DIM).to(self.device)
        self.risk_head = nn.Sequential(
            nn.Linear(_EMBED_DIM, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        ).to(self.device)

        self.encoder.eval()
        self.risk_head.eval()

    def _encode_text(self, text: str) -> torch.Tensor:
        tokens = _tokenize(text)
        ids = [_VOCAB[t] for t in tokens if t in _VOCAB]
        if not ids:
            # Fallback token if we didn't match anything
            ids = [0]
        idx_tensor = torch.tensor(ids, dtype=torch.long, device=self.device)
        with torch.no_grad():
            return self.encoder(idx_tensor)  # (D,)

    def toxicity_score(self, text: str) -> float:
        """
        Returns a probability-like score in [0, 1].
        NOTE: weights are random unless you later fine-tune and load from a checkpoint.
        """
        with torch.no_grad():
            rep = self._encode_text(text)
            logit = self.risk_head(rep)
            prob = torch.sigmoid(logit).item()
            return float(prob)

    def similarity(self, text_a: str, text_b: str) -> float:
        """
        Cosine similarity between prompt & answer encodings.
        """
        with torch.no_grad():
            rep_a = self._encode_text(text_a)
            rep_b = self._encode_text(text_b)
            num = torch.dot(rep_a, rep_b)
            denom = (rep_a.norm() * rep_b.norm() + 1e-8)
            sim = num / denom
            return float(sim.item())


# Global singleton used by the guardrail system
_MODEL = TorchGuardrailModel()


def score_with_torch(prompt: str, answer: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Returns (toxicity_score, similarity_score).
    If PyTorch isn't available or something fails, returns (None, None).
    """
    if not _MODEL.enabled:
        return None, None

    try:
        toxicity = _MODEL.toxicity_score(answer)
        similarity = _MODEL.similarity(prompt, answer)
        return toxicity, similarity
    except Exception:
        # Fail soft – guardrails still work with regex & heuristics
        return None, None
