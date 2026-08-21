from bs4 import BeautifulSoup
import requests
from langchain.tools import tool


def _ddg_search(query: str, max_results: int = 5) -> list:
    """Search using DuckDuckGo via ddgs library."""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [
                {"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", "")}
                for r in results
            ]
    except Exception:
        return []


def _wiki_summary(topic: str) -> str:
    """Get summary from Wikipedia."""
    try:
        headers = {"User-Agent": "ResearchAgent/1.0"}
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("extract", "")
    except Exception:
        pass
    return ""


def _wiki_search(query: str) -> list:
    """Search Wikipedia for related articles."""
    try:
        headers = {"User-Agent": "ResearchAgent/1.0"}
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": 5,
            "format": "json",
        }
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            results = []
            for item in data.get("query", {}).get("search", []):
                title = item.get("title", "")
                snippet = BeautifulSoup(item.get("snippet", ""), "html.parser").get_text()
                results.append({
                    "title": title,
                    "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                    "snippet": snippet,
                })
            return results
    except Exception:
        pass
    return []


@tool
def web_search(query: str) -> str:
    """Search the web for information on a given topic. Returns titles, URLs and snippets."""
    # Try DuckDuckGo first (most reliable)
    results = _ddg_search(query)
    if results:
        return "\n\n".join(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}"
            for r in results
        )
    # Fallback to Wikipedia
    wiki_results = _wiki_search(query)
    if wiki_results:
        lines = ["[Wikipedia Results]"]
        for r in wiki_results:
            lines.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}")
        summary = _wiki_summary(query.split()[0] + " " + query.split()[-1])
        if summary:
            lines.append(f"\n[Wikipedia Summary]\n{summary[:500]}")
        return "\n\n".join(lines)
    return f"No search results for: {query}. Try scraping a specific URL."


@tool
def web_scrape(url: str) -> str:
    """Extract text content from a webpage URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return "\n".join(chunk for chunk in chunks if chunk)[:3000]
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
