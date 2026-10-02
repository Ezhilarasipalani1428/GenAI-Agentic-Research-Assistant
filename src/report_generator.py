"""
report_generator.py - Final report generation for the research workflow.

Purpose
-------
Takes the combined research material gathered for a topic and asks the model
to turn it into a structured academic report.

The model has a tokens-per-minute limit on the free tier, so the research
material is capped to a conservative size before the prompt is built. This
keeps the final request safely below the limit.
"""

from src.agent import run_agent

# Maximum number of characters of research material sent to the model.
# This is a conservative stand-in for a token limit (roughly 4 characters per
# token, so 24,000 characters is about 6,000 tokens).
MAX_RESEARCH_CHARS = 24_000

# Added to the end of the research when it had to be shortened.
TRUNCATION_NOTE = "[Research material truncated to fit the model context limit.]"


def _truncate_research(research: str, max_chars: int = MAX_RESEARCH_CHARS) -> str:
    """Shorten `research` to at most `max_chars` characters, cutting cleanly.

    If the text is already short enough it is returned unchanged. Otherwise it
    is cut at the last paragraph, sentence, or word boundary before the limit
    (so it doesn't end mid-word) and a short truncation note is appended.
    """
    if len(research) <= max_chars:
        return research

    cut = research[:max_chars]

    # Prefer a paragraph break, then a sentence end, then a space - but only if
    # that boundary is reasonably close to the limit (past the halfway point).
    for separator in ("\n\n", ". ", " "):
        position = cut.rfind(separator)
        if position > max_chars // 2:
            cut = cut[: position + (1 if separator == ". " else 0)]
            break

    return f"{cut.rstrip()}\n\n{TRUNCATION_NOTE}"


def generate_report(topic: str, research: str) -> str:
    """Generate the final structured report for `topic` from `research`.

    Args:
        topic: The research topic, as a non-empty string.
        research: The combined research material, as a non-empty string.

    Returns:
        The final report text.

    Raises:
        ValueError: If `topic` or `research` is not a non-empty string.
        RuntimeError: If the model request fails (raised by `run_agent`).
    """
    # Validate the inputs.
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string.")
    if not isinstance(research, str) or not research.strip():
        raise ValueError("research must be a non-empty string.")

    topic = topic.strip()

    # Keep the request small enough for the model's per-minute token limit.
    research = _truncate_research(research.strip())

    prompt = f"""Write a well-structured academic report on the topic: {topic}

Use exactly these sections, in this order:
1. Introduction
2. Key Findings
3. Benefits and Impacts
4. Challenges and Limitations
5. Conclusion

Rules:
- Base the report only on the supplied research material.
- Do not invent facts, statistics, studies, or sources.
- Use clear academic language.

Research material:
{research}
"""

    return run_agent(prompt)