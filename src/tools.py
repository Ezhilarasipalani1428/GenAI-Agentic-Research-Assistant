"""
tools.py - Research tools for the Agentic AI Research & Report Generation System.

Provides real-time web research using Gemini's Google Search grounding.
"""

from src.agent import get_client, MODEL_NAME
from google.genai import types


def web_research(query: str) -> str:
    """
    Research a query using Gemini with Google Search grounding.
    """

    if not isinstance(query, str):
        raise ValueError("query must be a string.")

    if not query.strip():
        raise ValueError("query must be a non-empty string.")

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"""
Research the following topic using current web information:

{query.strip()}

Provide a concise factual summary.
Include important current information and identify relevant sources
where available.
Do not invent facts or sources.
""",
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ]
        ),
    )

    if not response.text:
        raise RuntimeError("Web research returned an empty response.")

    return response.text