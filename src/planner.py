"""
planner.py - Research planning step of the research workflow.

Purpose
-------
Asks the model to break a research topic into a small, fixed number of
research tasks. The plan is returned as a numbered list so that
`extract_research_tasks()` in `agent.py` can split it into individual tasks.

The number of tasks is kept small (exactly 4) to limit the number of API
calls and stay within the model's free-tier rate limits.
"""

from src.agent import run_agent

# How many research tasks the plan should contain.
NUMBER_OF_TASKS = 4


def create_research_plan(topic: str) -> str:
    """Create a numbered research plan with exactly 4 tasks for `topic`.

    Args:
        topic: The research topic, as a non-empty string.

    Returns:
        The research plan as text, one numbered task per line
        (1. ..., 2. ..., 3. ..., 4. ...).

    Raises:
        ValueError: If `topic` is not a non-empty string.
        RuntimeError: If the model request fails (raised by `run_agent`).
    """
    # Validate the input.
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string.")

    topic = topic.strip()

    prompt = f"""Create a research plan for the topic: {topic}

Write EXACTLY {NUMBER_OF_TASKS} research tasks. Each task must cover a different
important dimension of the topic (for example: background and definitions,
current developments, benefits and impacts, challenges and limitations).
The tasks must not repeat or overlap each other.

Each task must be a single line made of:
- a short task title, followed by a colon
- a brief explanation of what information should be investigated

Format rules:
- Output ONLY the numbered list, exactly like this:
1. Task title: what to investigate
2. Task title: what to investigate
3. Task title: what to investigate
4. Task title: what to investigate
- Use plain text only (no bold, headings, or bullet points).
- Do not add any introduction, notes, or closing text.
"""

    return run_agent(prompt)