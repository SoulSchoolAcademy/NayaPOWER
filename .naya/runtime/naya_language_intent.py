from dataclasses import dataclass

NODE_ALIASES = {
    "smart node this",
    "naya node this",
    "smart note this",
    "note this",
    "remember this",
    "capture this",
    "document this",
}


@dataclass(frozen=True)
class IntentResult:
    intent: str
    requires_clarification: bool
    clarifying_question: str
    authority_expansion: bool


def interpret_naya_language(command: str) -> IntentResult:
    normalized = " ".join(command.lower().strip().split())
    if normalized.startswith("naya,"):
        normalized = normalized[5:].strip()

    if normalized in NODE_ALIASES:
        return IntentResult("CREATE_OR_UPDATE_NAYA_NODE", False, "", False)

    if normalized in {"play", "naya play", "play this"}:
        return IntentResult("PLAY_INTELLIGENCE", False, "", False)

    return IntentResult(
        "UNKNOWN",
        True,
        "I can infer the intended outcome when it is clear; otherwise, Is this your intention?",
        False,
    )
