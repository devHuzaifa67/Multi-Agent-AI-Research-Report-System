from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippits."""
    results = tavily.search(query=query, max_results=5)
    
    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return "\n---\n".join(out)

#print(web_search.invoke("What is the recent news of war?"))


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip = True)[:3000]
    
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
#print(scrape_url.invoke("https://www.bbc.com/news"))



# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup

# def scrape_url(url: str) -> str:
#     """Scrape and return clean text content from a given URL with JS support."""
#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=True)
#             page = browser.new_page()
#             page.goto(url, timeout=15000)

#             # Wait for main content to load
#             page.wait_for_load_state("networkidle")

#             html = page.content()
#             browser.close()

#         soup = BeautifulSoup(html, "html.parser")

#         # Remove unwanted tags
#         for tag in soup(["script", "style", "nav", "footer"]):
#             tag.decompose()

#         return soup.get_text(separator=" ", strip=True)[:3000]

#     except Exception as e:
#         return f"Could not scrape URL: {str(e)}"

# # Example usage
# print(scrape_url("https://www.dawn.com/news/2004941/bilawal-pledges-to-address-diamer-bhasha-dam-resettlement-issues-if-ppp-wins-g-b-polls"))
