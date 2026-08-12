import streamlit as st
from agent import create_research_agent
from utils.report import display_report
import os
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }

    /* ── Color Palette ──
        #344E41 - Brunswick green (darkest)
        #3A5A40 - Hunter green
        #5C7650 - Roseda green
        #A3B18A - Sage
        #DAD7CD - Timberwolf (lightest)
    */

    /* ── Background ── */
    .stApp {
        background-color: #000000;
        color: #DAD7CD;
    }
    section[data-testid="stSidebar"] {
        background-color: #050505;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
        color: #A3B18A;
        font-size: 1.6rem;
        font-weight: 700;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #5C7650;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
        color: #A3B18A;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* ── Header ── */
    .main-header {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        border-bottom: 1px solid #344E41;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        color: #DAD7CD;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: #A3B18A;
        font-size: 1.15rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* ── Chat Input ── */
    .stChatInput textarea {
        background-color: #0a0a0a !important;
        color: #DAD7CD !important;
        border: 1px solid #344E41 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }
    .stChatInput textarea:focus {
        border-color: #A3B18A !important;
        box-shadow: 0 0 0 2px rgba(163, 177, 138, 0.15) !important;
    }

    /* ── Chat Messages ── */
    [data-testid="stChatMessage"] {
        background-color: #0a0a0a;
        border: 1px solid #344E41;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin: 0.5rem 0;
    }
    [data-testid="stChatMessage"]:hover {
        border-color: #3A5A40;
    }
    [data-testid="stChatMessage"][aria-label="User"] {
        background: #080c09;
        border-left: 3px solid #A3B18A;
    }
    [data-testid="stChatMessage"][aria-label="Assistant"] {
        background: #060a07;
        border-left: 3px solid #5C7650;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        color: #DAD7CD;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    /* ── Status Widget ── */
    .stStatus {
        border: 1px solid #344E41;
        border-radius: 12px;
        background-color: #0a0a0a;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: #0a0a0a;
        color: #A3B18A;
        border: 1px solid #344E41;
        border-radius: 10px;
        padding: 0.55rem 1.4rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        border-color: #A3B18A;
        color: #DAD7CD;
        background: #0f1410;
    }

    /* ── Sidebar Example Buttons ── */
    [data-testid="stSidebar"] .stButton > button {
        background: #0a0a0a;
        color: #A3B18A;
        border: 1px solid #344E41;
        border-radius: 8px;
        text-align: left;
        font-size: 0.9rem;
        padding: 0.6rem 0.85rem;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #A3B18A;
        color: #DAD7CD;
        background: #0f1410;
    }

    /* ── Expandable ── */
    .streamlit-expanderHeader {
        background-color: #0a0a0a !important;
        border: 1px solid #344E41 !important;
        border-radius: 10px !important;
        color: #A3B18A !important;
        font-size: 0.95rem !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: #A3B18A !important;
        color: #DAD7CD !important;
    }

    /* ── Download Button ── */
    .stDownloadButton > button {
        background: transparent;
        color: #A3B18A;
        border: 1px solid #3A5A40;
        border-radius: 10px;
        font-size: 0.9rem;
    }
    .stDownloadButton > button:hover {
        background: rgba(163, 177, 138, 0.1);
        border-color: #A3B18A;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #000000; }
    ::-webkit-scrollbar-thumb { background: #344E41; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3A5A40; }

    /* ── Markdown Content ── */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #DAD7CD !important;
        font-weight: 700;
    }
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #A3B18A !important;
    }
    .stMarkdown a { color: #A3B18A; }
    .stMarkdown a:hover { color: #DAD7CD; }
    .stMarkdown li { color: #DAD7CD; font-size: 1.05rem; }
    .stMarkdown p { color: #DAD7CD; line-height: 1.8; font-size: 1.05rem; }
    .stMarkdown strong { color: #A3B18A; font-weight: 700; }
    .stMarkdown em { color: #5C7650; }
    .stMarkdown code {
        background: #0a0a0a;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        border: 1px solid #344E41;
        color: #A3B18A;
        font-size: 0.9em;
    }

    /* ── Divider ── */
    hr {
        border-color: #344E41;
        opacity: 0.6;
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "agent" not in st.session_state:
    st.session_state.agent = None


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🔬 Research Agent")
    st.markdown("AI-powered research assistant that searches the web and synthesizes structured reports.")

    st.markdown("---")
    st.markdown("### ⚡ How it works")
    st.markdown("""
    1. 🔍 Search the web
    2. 📖 Read key sources
    3. 🧠 Generate report
    """)

    st.markdown("---")
    st.markdown("### 💡 Try these examples")

    example_queries = [
        "Latest breakthroughs in solid-state batteries",
        "Compare React vs Vue.js for web dev in 2026",
        "Rust vs C++ for systems programming",
        "Quantum computing recent advances",
        "Best practices for deploying AI models",
    ]

    for query in example_queries:
        if st.button(query, key=f"ex_{query[:30]}"):
            st.session_state.user_input = query

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    show_sources = st.checkbox("Show sources", value=True)
    detail_level = st.selectbox("Detail level", ["Concise", "Detailed", "Comprehensive"], index=1)

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center; color:#5C7650; font-size:0.85rem; padding:0.5rem 0;">'
        '🔗 <a href="https://github.com/ayaan-2008" target="_blank" style="color:#A3B18A; text-decoration:none;">GitHub</a> &nbsp;|&nbsp; '
        'Built by <strong style="color:#DAD7CD;">Ayaan</strong>'
        '</div>',
        unsafe_allow_html=True,
    )


# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🔬 Research Agent</h1>
    <p>Search the web. Read sources. Get structured reports.</p>
</div>
""", unsafe_allow_html=True)


# ─── Helper: Run Research Agent ────────────────────────────────────────────────
def run_research(query: str, detail: str) -> tuple[str, list]:
    """Run the research agent and return (report, sources)."""
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

    agent = create_research_agent()
    result = agent.invoke({"messages": [("user", query)]})

    messages = result.get("messages", [])

    # Find the LAST AIMessage that has substantial content (the final report)
    report = ""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content and len(msg.content) > 100:
            report = msg.content
            break

    # If no good AI report found, try the last message with content
    if not report:
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content and len(msg.content) > 50:
                report = msg.content
                break

    if not report:
        report = "No report was generated. Please try rephrasing your query."

    # Extract URLs from report (sources)
    sources = []
    import re
    urls = re.findall(r'https?://[^\s\)\]>"]+', report)
    sources = list(dict.fromkeys(urls))  # deduplicate while preserving order

    return report, sources


# ─── Chat History Display ──────────────────────────────────────────────────────
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    sources = message.get("sources", [])

    with st.chat_message(role, avatar="🧑" if role == "user" else "🔬"):
        st.markdown(content)
        if role == "assistant" and sources and show_sources:
            with st.expander("📎 Sources"):
                for src in sources:
                    st.markdown(f"- [{src}]({src})")


# ─── Chat Input ────────────────────────────────────────────────────────────────
# Check if an example button was clicked
user_input = st.chat_input("Ask me anything to research...")
if "user_input" in st.session_state:
    user_input = st.session_state.pop("user_input")

if user_input:
    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "sources": [],
    })

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Run agent with status
    with st.chat_message("assistant", avatar="🔬"):
        report_text = ""
        sources = []

        with st.status("🔬 Researching...", expanded=True) as status:
            st.write("🔍 Searching the web for relevant sources...")
            try:
                report_text, sources = run_research(user_input, detail_level)
                st.write(f"📖 Found {len(sources)} sources")
                st.write("🧠 Generating structured report...")
                status.update(label="✅ Research complete!", state="complete")
            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                report_text = f"Sorry, an error occurred while researching: {str(e)}"
                st.error(str(e))

        # Always show report if we have one
        if report_text and report_text.strip():
            st.markdown("---")
            st.markdown(report_text)

            if sources and show_sources:
                with st.expander("📎 Sources"):
                    for src in sources:
                        st.markdown(f"- [{src}]({src})")

            # Download button
            report_md = f"# Research: {user_input}\n\n{report_text}"
            st.download_button(
                label="📥 Download Report",
                data=report_md,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
            )
        else:
            st.warning("No report was generated. Please try again.")

        # Save to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": report_text,
            "sources": sources,
        })
