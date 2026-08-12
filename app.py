from agent import create_research_agent
from utils.report import display_report


def main():
    agent = create_research_agent()

    print("=" * 80)
    print("  RESEARCH AGENT")
    print("  Powered by Groq + Qwen")
    print("=" * 80)
    print("\nEnter a research topic (or 'quit' to exit):\n")

    while True:
        query = input("> ").strip()
        if query.lower() in ["quit", "exit", "q"]:
            break

        if not query:
            continue

        print(f"\nResearching: {query}...\n")
        try:
            result = agent.invoke({"messages": [("user", query)]})
            output = result["messages"][-1].content
            display_report(query, output)
        except Exception as e:
            print(f"Error: {str(e)}")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
