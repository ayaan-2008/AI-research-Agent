from langchain_groq import ChatGroq
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file
load_dotenv(Path(__file__).parent / ".env")


def get_llm():
    """Get Groq LLM. Supports both Streamlit secrets (deployment) and .env (local)."""
    api_key = None

    # Try Streamlit secrets first (for deployment)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    # Fallback to environment variable (for local dev)
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not configured. "
            "Add it to .env (local) or Streamlit secrets (deployment)."
        )

    return ChatGroq(
        groq_api_key=api_key,
        model_name="qwen/qwen3.6-27b",
        temperature=0.3,
        max_tokens=2000,
    )
