"""
Tool Registry for Instagram Agent Dependency Injection.
Automatically detects Tavily Search and AirTop Browser API keys when present.
Reuses the same tool providers as the LinkedIn Agent.
"""

import os
from typing import Optional
from .base import TextGenerationTool, ImageGenerationTool, SearchTool, InstagramTool
from .mock_providers import (
    MockTextGenerationTool,
    MockImageGenerationTool,
    MockSearchTool,
    MockInstagramTool,
)

# Reuse Tavily and AirTop providers from the LinkedIn Agent
import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

try:
    from .tavily_provider import TavilySearchTool
except ImportError:
    try:
        from linkedin_agent.tools.tavily_provider import TavilySearchTool
    except ImportError:
        TavilySearchTool = None

try:
    from .airtop_provider import AirTopSearchTool
except ImportError:
    try:
        from linkedin_agent.tools.airtop_provider import AirTopSearchTool
    except ImportError:
        AirTopSearchTool = None


class ToolRegistry:
    """Central container managing tool bindings for the Instagram Agent."""

    def __init__(
        self,
        text_gen: Optional[TextGenerationTool] = None,
        image_gen: Optional[ImageGenerationTool] = None,
        search: Optional[SearchTool] = None,
        instagram: Optional[InstagramTool] = None,
    ):
        self.text_gen = text_gen or MockTextGenerationTool()
        self.image_gen = image_gen or MockImageGenerationTool()

        # Detect Tavily or AirTop API Keys automatically
        tavily_key = os.getenv("TAVILY_API_KEY", "")
        airtop_key = os.getenv("AIRTOP_API_KEY", "")

        if search:
            self.search = search
        elif tavily_key and TavilySearchTool:
            self.search = TavilySearchTool(api_key=tavily_key)
        elif airtop_key and AirTopSearchTool:
            self.search = AirTopSearchTool(api_key=airtop_key)
        else:
            self.search = MockSearchTool()

        self.instagram = instagram or MockInstagramTool()

    def set_text_gen_provider(self, provider: TextGenerationTool):
        self.text_gen = provider

    def set_image_gen_provider(self, provider: ImageGenerationTool):
        self.image_gen = provider

    def set_search_provider(self, provider: SearchTool):
        self.search = provider

    def set_instagram_provider(self, provider: InstagramTool):
        self.instagram = provider
