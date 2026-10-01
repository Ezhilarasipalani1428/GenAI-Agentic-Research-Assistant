import streamlit as st

from src.agent import run_research_workflow


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Agentic AI Research & Report Generation System")

st.write(
    "Enter a research topic and the AI agent will plan the research, "
    "gather information, and generate a structured report."
)

topic = st.text_input(
    "Research Topic",
    placeholder="Example: Impact of artificial intelligence on education",
)

if st.button("Generate Research Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Research agent is working..."):
            try:
                report = run_research_workflow(topic)

                st.success("Research report generated successfully!")

                st.markdown("## Final Report")
                st.markdown(report)

                st.download_button(
                    label="Download Report",
                    data=report,
                    file_name="research_report.txt",
                    mime="text/plain",
                )

            except Exception as exc:
                st.error(f"An error occurred: {exc}")