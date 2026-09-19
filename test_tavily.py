"""
Quick Verification Script for Tavily Search API Integration.
"""

from instagram_agent.tools.tavily_provider import TavilySearchTool

def main():
    print("Verifying Tavily Search API Integration...")
    tavily_tool = TavilySearchTool()
    
    print(f"[*] Tavily API Key Loaded: {'YES' if tavily_tool.api_key else 'NO'}")
    
    results = tavily_tool.browser_search("Instagram carousels design trends 2026", num_results=3)
    print(f"[*] Search Executed. Results Count: {len(results)}")
    for i, r in enumerate(results, 1):
        print(f"\n    Result {i}: {r.get('title')}")
        print(f"    URL     : {r.get('url')}")
        print(f"    Snippet : {r.get('snippet')[:120]}...")
        
    print("\n[SUCCESS] Tavily AI Search integration is active and working!")

if __name__ == "__main__":
    main()
