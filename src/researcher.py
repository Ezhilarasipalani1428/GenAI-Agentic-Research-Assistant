"""
researcher.py - Research module for the Agentic AI Research & Report Generation System.

This module researches individual tasks produced by the planner.
"""

from src.agent import run_agent


def research_task(task: str) -> str:
    """
    Research a single task and return a structured summary.
    """

    if not isinstance(task, str):
        raise ValueError("task must be a string.")

    if not task.strip():
        raise ValueError("task must be a non-empty string.")

    prompt = f"""
Research the following topic and provide a concise factual summary.

Research task:
{task.strip()}

Include:
1. Key information
2. Important facts or concepts
3. Major benefits or impacts
4. Important challenges or limitations

Do not invent statistics, studies, organizations, or specific sources.
Clearly state when information is general rather than source-specific.
"""

    return run_agent(prompt)