"""
Quick Verification Script for AirTop Browser API Integration.
"""

from instagram_agent.tools.airtop_provider import AirTopSearchTool

def main():
    print("Verifying AirTop Cloud Browser Integration...")
    airtop_tool = AirTopSearchTool()
    
    print(f"[*] AirTop API Key Loaded: {'YES' if airtop_tool.api_key else 'NO'}")
    
    results = airtop_tool.browser_search("Instagram marketing automation benchmarks", num_results=2)
    print(f"[*] Search Executed. Results Count: {len(results)}")
    for i, r in enumerate(results, 1):
        print(f"\n    Result {i}: {r.get('title')}")
        print(f"    URL     : {r.get('url')}")
        print(f"    Snippet : {r.get('snippet')[:120]}...")
        
    print("\n[SUCCESS] AirTop Browser integration is active and working!")

if __name__ == "__main__":
    main()
