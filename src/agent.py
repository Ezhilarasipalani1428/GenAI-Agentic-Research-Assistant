"""
agent.py - Core module for the Agentic AI Research & Report Generation System.

Purpose
-------
This module is the central entry point of the agent. It provides:

1. `get_client()`            - a reusable Groq client (API key from root `.env`).
2. `run_agent(task)`         - send a single task to the model and return the text.
3. `run_research_workflow()` - orchestrates the multi-step research workflow:
       plan -> extract tasks -> research each task -> combine -> final report.

The individual workflow steps live in their own modules:
    - src/planner.py          -> create_research_plan()
    - src/researcher.py       -> research_task()
    - src/report_generator.py -> generate_report()

Usage
-----
    from src.agent import run_research_workflow

    report = run_research_workflow("Impact of AI on healthcare")
    print(report)
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq, GroqError

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# The project root is one level above the `src/` folder that contains this file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# Load variables from the root `.env` file into the process environment.
load_dotenv(dotenv_path=ENV_PATH)

# Groq model to use. Override it by setting GROQ_MODEL in the `.env` file.
# Note: "llama-3.3-70b-versatile" was shut down by Groq on 16 Aug 2026, so the
# default is the production model "openai/gpt-oss-120b" (available on the free
# tier). Check https://console.groq.com/docs/models for the current list.
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Tells the model what role it plays.
SYSTEM_INSTRUCTION = (
    "You are an AI research agent. Your purpose is to help users investigate "
    "topics and produce well-structured reports. In future versions you will "
    "perform planning, research, analysis, and report generation. For now, "
    "respond to the user's task clearly, accurately, and concisely."
)

# Holds the shared client so we only create it once (see `get_client`).
_client: Groq | None = None


# ---------------------------------------------------------------------------
# Client setup
# ---------------------------------------------------------------------------

def get_client() -> Groq:
    """Return a reusable Groq client, creating it on first use.

    The API key is read from the `GROQ_API_KEY` environment variable
    (populated from the root `.env` file). The key is never printed or logged.
    The Groq SDK applies a 60-second request timeout by default, so requests
    cannot hang indefinitely.

    Raises:
        EnvironmentError: If `GROQ_API_KEY` is missing or empty.
    """
    global _client

    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key or not api_key.strip():
            raise EnvironmentError(
                "GROQ_API_KEY is not set. Add a line like "
                "GROQ_API_KEY=your_key_here to the .env file in the project "
                f"root ({ENV_PATH}) and try again."
            )

        _client = Groq(api_key=api_key.strip())

    return _client


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _validate_text(value: str, name: str) -> str:
    """Check that `value` is a non-empty string and return it stripped."""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string.")
    if not value.strip():
        raise ValueError(f"{name} must be a non-empty string.")
    return value.strip()


def _generate(prompt: str) -> str:
    """Send `prompt` to Groq and return the generated text.

    Raises:
        EnvironmentError: If the API key is missing.
        RuntimeError: If the API call fails or returns no text.
    """
    client = get_client()

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
        )
    except GroqError as exc:
        raise RuntimeError(f"Groq API request failed: {exc}") from exc
    except Exception as exc:  # e.g. network problems or timeouts
        raise RuntimeError(
            f"Unexpected error while calling Groq: {exc}"
        ) from exc

    # The generated text lives in the first choice's message.
    text = response.choices[0].message.content if response.choices else None

    if not text or not text.strip():
        raise RuntimeError(
            "Groq returned an empty response. The request may have been "
            "blocked or produced no text."
        )

    return text


def extract_research_tasks(plan: str) -> list[str]:
    """Extract the numbered tasks (e.g. '1. ...' or '2) ...') from a plan.

    Raises:
        RuntimeError: If no numbered tasks are found in the plan.
    """
    tasks = []
    for line in plan.splitlines():
        match = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if match:
            tasks.append(match.group(1).strip())

    if not tasks:
        raise RuntimeError(
            "Could not find any numbered research tasks in the generated plan."
        )

    return tasks


# ---------------------------------------------------------------------------
# Single-task agent
# ---------------------------------------------------------------------------

def run_agent(task: str) -> str:
    """Send a task to the model and return its response text.

    Args:
        task: The user's request, as a non-empty string.

    Returns:
        The text generated by the model.

    Raises:
        ValueError: If `task` is not a string or is empty/whitespace only.
        EnvironmentError: If `GROQ_API_KEY` is not configured.
        RuntimeError: If the Groq API call fails or returns no text.
    """
    task = _validate_text(task, "task")
    return _generate(task)


# ---------------------------------------------------------------------------
# Full workflow
# ---------------------------------------------------------------------------

def run_research_workflow(topic: str) -> str:
    """Run the full research workflow for `topic` and return the final report.

    Steps:
        1. Create a research plan          (src.planner)
        2. Extract the numbered tasks      (extract_research_tasks, above)
        3. Research each task              (src.researcher)
        4. Combine the results
        5. Generate the final report       (src.report_generator)

    Raises:
        ValueError: If `topic` is not a non-empty string.
        EnvironmentError: If `GROQ_API_KEY` is not configured.
        RuntimeError: If any Groq call fails or no tasks can be extracted.
    """
    # These modules may themselves import `get_client` from this file, so we
    # import them here (inside the function) to avoid a circular import.
    from src.planner import create_research_plan
    from src.report_generator import generate_report
    from src.researcher import research_task

    topic = _validate_text(topic, "topic")

    # 1. Plan
    plan = create_research_plan(topic)

    # 2. Extract tasks
    tasks = extract_research_tasks(plan)

    # 3. Research each task
    sections = []
    for number, task in enumerate(tasks, start=1):
        findings = research_task(task)
        sections.append(f"Task {number}: {task}\n{findings}")

    # 4. Combine
    combined_results = "\n\n".join(sections)

    # 5. Final report
    return generate_report(topic, combined_results)