# 🤖 Agentic AI Research & Report Generation System

An Agentic AI system that accepts a research topic, creates a structured research plan, investigates each research task, and generates a well-organized academic report.

The project demonstrates an agent-based workflow using Python, Streamlit, and the Groq API.

## ✨ Features

* 🧠 AI-powered research planning
* 📋 Automatic breakdown of a topic into 4 research tasks
* 🔎 AI-based research summarization for each task
* 📝 Automated academic report generation
* 📊 Structured report sections
* 🖥️ Interactive Streamlit interface
* 📥 Download generated reports as `.txt` files
* 🔐 Environment-variable based API key configuration
* ⚙️ Modular Python architecture

## 🔄 System Workflow

```text
User enters research topic
        ↓
AI Agent
        ↓
Research Planning
        ↓
4 Research Tasks
        ↓
Research Each Task
        ↓
Combine Research Findings
        ↓
Generate Final Report
        ↓
Display Report in Streamlit
        ↓
Download Report
```

## 🏗️ Architecture

The system is divided into separate modules:

### Agent

`src/agent.py`

Acts as the central controller of the workflow. It connects the different modules and manages the complete research process.

### Planner

`src/planner.py`

Creates a research plan containing exactly four research tasks for the given topic.

### Researcher

`src/researcher.py`

Processes each research task and generates a concise factual summary using the AI model.

### Report Generator

`src/report_generator.py`

Combines the research findings and generates a structured academic report containing:

1. Introduction
2. Key Findings
3. Benefits and Impacts
4. Challenges and Limitations
5. Conclusion

### Streamlit Application

`app.py`

Provides the user interface for entering a topic, generating the report, viewing the result, and downloading it.

## 🛠️ Technologies Used

| Technology          | Purpose                          |
| ------------------- | -------------------------------- |
| Python 3.12         | Core programming language        |
| Streamlit           | Web-based user interface         |
| Groq API            | AI model inference               |
| OpenAI GPT-OSS 120B | Language model used by the agent |
| python-dotenv       | Environment variable management  |
| Requests            | HTTP/API-related functionality   |

## 📁 Project Structure

```text
GenAI-Agentic-Research-Assistant/
│
├── src/
│   ├── agent.py
│   ├── planner.py
│   ├── researcher.py
│   ├── report_generator.py
│   └── tools.py
│
├── data/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── app.py
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ezhilarasipalani1428/GenAI-Agentic-Research-Assistant.git
cd GenAI-Agentic-Research-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

Use `.env.example` as a reference:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Replace `your_groq_api_key_here` with your own Groq API key.

**Never commit your real `.env` file or API key to GitHub.**

## ▶️ Running the Application

Start the Streamlit application with:

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

Enter a research topic such as:

```text
Impact of artificial intelligence on education
```

Then click **Generate Research Report**.

The system will create a research plan, process the research tasks, generate the final report, display it in the application, and provide a download option.

## 📄 Example Output

A generated report contains the following sections:

```text
1. Introduction
2. Key Findings
3. Benefits and Impacts
4. Challenges and Limitations
5. Conclusion
```

The generated report can also be downloaded as a `.txt` file.

## 🔐 Security

API credentials are stored using environment variables rather than directly inside the source code.

The `.env` file is excluded from Git using `.gitignore`.

Do not publish or share your actual API key.

## 🚀 Future Enhancements

Possible future improvements include:

* 🌐 Integration with real-time web search
* 🔗 Automatic source collection and citation
* 📚 Research using verified external sources
* 🧠 Improved multi-agent collaboration
* 💾 Persistent research history
* 📄 PDF report generation
* 📊 Research visualization and charts
* 🔄 Long-term research memory
* 🎯 More advanced task planning and tool usage

## 🎓 Project Purpose

This project was developed to demonstrate the concepts of **Agentic AI**, including task planning, modular agent execution, information processing, workflow orchestration, and automated report generation.

The project is intended as an educational and portfolio project for exploring practical applications of Generative AI and agent-based systems.

## 👨‍💻 Author

**Ezhilarasi Palani**

B.E. Computer Science and Engineering

Panimalar Engineering College
