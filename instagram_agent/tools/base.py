"""
Abstract Base Classes for Tool Providers.
Extends the core tool interfaces with Instagram-specific capabilities.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class TextGenerationTool(ABC):
    """Abstract interface for text generation LLM providers (e.g. Gemini, OpenAI, Claude)."""
    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        pass


class ImageGenerationTool(ABC):
    """Abstract interface for image generation providers (e.g. Imagen, DALL-E, Midjourney)."""
    @abstractmethod
    def generate_image(self, prompt: str, style_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass


class SearchTool(ABC):
    """Abstract interface for browser search & scraping capabilities."""
    @abstractmethod
    def browser_search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def browse_url(self, url: str) -> str:
        pass


class InstagramTool(ABC):
    """Abstract interface for Instagram API operations."""
    @abstractmethod
    def instagram_fetch_account(self, account_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def instagram_fetch_media(self, account_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def instagram_publish(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def instagram_fetch_insights(self, media_id: str) -> Dict[str, Any]:
        pass
