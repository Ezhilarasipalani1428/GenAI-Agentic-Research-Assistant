"""
planner.py - Planning module for the Agentic AI Research & Report Generation System.

This module converts a research topic into a structured research plan.
"""

from src.agent import run_agent


def create_research_plan(topic: str) -> str:
    """
    Create a step-by-step research plan for the given topic.
    """

    if not isinstance(topic, str):
        raise ValueError("topic must be a string.")

    if not topic.strip():
        raise ValueError("topic must be a non-empty string.")

    prompt = f"""
Create a clear research plan for the following topic:

Topic: {topic.strip()}

Break the research into 5 to 7 specific tasks.

For each task:
- Give a short task title.
- Explain what information should be investigated.

Return only the numbered research plan.
"""

    return run_agent(prompt)