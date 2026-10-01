"""
report_generator.py - Report generation module for the Agentic AI Research
& Report Generation System.
"""

from src.agent import run_agent


def generate_report(topic: str, research: str) -> str:
    """
    Generate a structured research report from collected research.
    """

    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string.")

    if not isinstance(research, str) or not research.strip():
        raise ValueError("research must be a non-empty string.")

    prompt = f"""
Write a well-structured research report on the following topic:

Topic:
{topic.strip()}

Research material:
{research.strip()}

Use the following structure:

# {topic.strip()}

## Introduction
Explain the topic and why it is important.

## Key Findings
Present the main findings from the research material.

## Benefits and Impacts
Explain the major benefits and impacts.

## Challenges and Limitations
Explain important challenges and limitations.

## Conclusion
Summarize the main points and provide a balanced conclusion.

Use clear, academic language.
Do not invent facts, statistics, studies, or sources.
Base the report only on the supplied research material.
"""

    return run_agent(prompt)