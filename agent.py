from langgraph.prebuilt import create_react_agent
from llm import get_llm
from tools import web_search, web_scrape
from prompts import RESEARCH_SYSTEM_PROMPT


def create_research_agent():
    llm = get_llm()
    tools = [web_search, web_scrape]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=RESEARCH_SYSTEM_PROMPT,
    )
    return agent
