# Research Agent

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://your-app-url.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-000000?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)

AI-powered research assistant that searches the web and synthesizes information into structured reports. Built with LangGraph, Groq, and DuckDuckGo.

## Preview

<!-- Replace with your screenshot: place an image file (e.g. preview.png) in the repo root and uncomment the line below -->
<!-- ![Research Agent Preview](preview.png) -->

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   [ Add your website screenshot here ]              │
│                                                     │
│   Save as preview.png in the repo root              │
│   Then uncomment the image line above               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Features

- **Chat interface** — Conversational research experience
- **Web search** — DuckDuckGo + Wikipedia fallback
- **Source scraping** — Reads and extracts content from web pages
- **Structured reports** — Executive summary, key findings, analysis, sources
- **Dark theme** — Clean dark UI with earthy green accents
- **Download reports** — Export as Markdown files

## Architecture

```
User Query (Chat)
     |
     v
LangGraph ReAct Agent
     |
     +--> web_search (DuckDuckGo / Wikipedia)
     |
     +--> scrape_webpage (BeautifulSoup)
     |
     v
Structured Research Report
     |
     v
Streamlit Chat UI
```

## Quick Start

```bash
# Clone
git clone https://github.com/ayaan-2008/research-agent.git
cd research-agent

# Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Add API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run
streamlit run streamlit_app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → select your repo
4. Select `streamlit_app.py` as the main file
5. Go to **Settings → Secrets** and add:
   ```
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
6. Click "Deploy"

## Project Structure

```
research-agent/
├── streamlit_app.py        # Streamlit chat UI (main)
├── app.py                  # CLI entry point
├── agent.py                # LangGraph ReAct agent setup
├── llm.py                  # Groq model configuration
├── prompts.py              # System prompt template
├── tools.py                # Web search + scraping tools
├── utils/
│   ├── __init__.py
│   └── report.py           # Report display (CLI)
├── .streamlit/
│   └── config.toml         # Streamlit theme config
├── requirements.txt
├── .env.example            # API key template
└── .gitignore
```

## Tech Stack

| Layer | Technology |
|---|---|
| **Agent Framework** | LangGraph (ReAct pattern) |
| **LLM** | Groq + Llama 3.3 70B |
| **Web Search** | DuckDuckGo + Wikipedia API |
| **Scraping** | BeautifulSoup4 |
| **Frontend** | Streamlit (chat interface) |

## Environment Variables

| Variable | Description | Where |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key | `.env` (local) or Streamlit Secrets (deployment) |

## Made By

**Ayaan** — [GitHub](https://github.com/ayaan-2008)
