"""Text cleaning and feature helpers for the phishing email detector."""
import re

URL_RE = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
HTML_RE = re.compile(r"<[^>]+>")
NON_ALPHA_RE = re.compile(r"[^a-z\s]")
MULTI_SPACE_RE = re.compile(r"\s+")

URGENT_WORDS = [
    "urgent", "immediately", "verify", "suspended", "confirm", "password",
    "account", "click", "login", "security", "limited", "expire", "bank",
    "winner", "prize", "claim", "act now", "update",
]


def clean_text(text: str) -> str:
    """Lowercase, strip HTML, replace URLs / emails with tokens, drop punctuation."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = HTML_RE.sub(" ", text)
    text = URL_RE.sub(" urltoken ", text)
    text = EMAIL_RE.sub(" emailtoken ", text)
    text = NON_ALPHA_RE.sub(" ", text)
    return MULTI_SPACE_RE.sub(" ", text).strip()


def extract_signals(raw_text: str) -> dict:
    """Human-readable red flags shown in the Streamlit UI (not used by the model)."""
    raw = raw_text or ""
    lower = raw.lower()
    return {
        "Links": len(URL_RE.findall(raw)),
        "Email addresses": len(EMAIL_RE.findall(raw)),
        "Urgent / sensitive words": sum(lower.count(w) for w in URGENT_WORDS),
        "Exclamation marks": raw.count("!"),
        "ALL-CAPS words": sum(1 for w in raw.split() if len(w) > 3 and w.isupper()),
    }
