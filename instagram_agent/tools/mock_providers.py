"""
Mock Tool Implementations for Instagram Agent Standalone Execution & Testing.
Provides intelligent default responses without external API requirements.
"""

from typing import Dict, Any, List, Optional
from .base import TextGenerationTool, ImageGenerationTool, SearchTool, InstagramTool


class MockTextGenerationTool(TextGenerationTool):
    """Smart mock text generator simulating LLM outputs for Instagram strategy, writing, and critique."""

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        prompt_lower = prompt.lower()

        if "strategy" in prompt_lower or "plan" in prompt_lower:
            return """
TARGET AUDIENCE: B2B Decision Makers, Founders, Growth Leaders
CONTENT OBJECTIVE: Drive engagement and direct lead generation
ANGLE: Framework-driven educational content with clear visual identity
CONTENT PILLARS: Educational, Authority, Social Proof, Product, Engagement
FORMAT MIX: 50% Carousels, 20% Static Posts, 30% Stories
POSTING FREQUENCY: 3-4 posts per week
BEST TIMES: Tuesday 9AM, Thursday 12PM, Saturday 10AM
            """

        elif "critic" in prompt_lower or "evaluate" in prompt_lower:
            if "iteration_0" in prompt_lower or "first" in prompt_lower:
                return """
STATUS: needs_revision
OVERALL_SCORE: 7.8
ISSUES:
- Hook slide could be more visually arresting with a stronger pattern interrupt.
- CTA needs a clearer direct benefit statement.
REQUIRED_CHANGES:
- Strengthen Slide 1 hook with a bold, contrarian statistic.
- Make CTA more specific with a direct lead magnet reference.
                """
            else:
                return """
STATUS: passed
OVERALL_SCORE: 9.5
ISSUES: None
REQUIRED_CHANGES: None
                """

        elif "revise" in prompt_lower or "improve" in prompt_lower:
            return """
REVISED HOOK: The counterintuitive strategy top 1% brands use (that 90% ignore)
REVISED CTA: Save this post and DM us 'BLUEPRINT' for the free strategy guide
            """

        elif "carousel" in prompt_lower:
            return """
CAROUSEL TITLE: Framework-driven educational breakdown
SLIDE COUNT: 6
HOOK: Bold contrarian metric on Slide 1
STRUCTURE: Hook → Problem → Step 1 → Step 2 → Step 3 → CTA
            """

        elif "static" in prompt_lower or "single post" in prompt_lower:
            return """
CONCEPT: High-impact single graphic with bold headline and supporting stat
CATEGORY: Authority
HEADLINE: Bold contrarian statement positioning brand as thought leader
            """

        elif "story" in prompt_lower:
            return """
SEQUENCE: 4-part story walkthrough with interactive elements
FLOW: Hook Story → Educational Story → Poll/Question → CTA Story
            """

        else:
            return """
Instagram content strategy generated with brand-aligned visual direction,
audience-targeted hooks, and conversion-optimized CTAs.
            """


class MockImageGenerationTool(ImageGenerationTool):
    """Mock image generator returning simulated asset metadata."""

    def generate_image(self, prompt: str, style_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "asset_id": "img_ig_mock_001",
            "url": "https://assets.instagram.example.com/generated_asset.png",
            "prompt": prompt,
            "status": "generated",
            "dimensions": "1080x1080",
        }


class MockSearchTool(SearchTool):
    """Mock web search for Instagram research."""

    def browser_search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        return [
            {
                "title": f"Instagram Growth Insights: {query}",
                "snippet": "Top-performing Instagram accounts leverage carousel formats for 3x higher saves and shares. Educational content pillars drive 68% more profile visits.",
                "url": "https://insights.example.com/instagram-growth-2026",
            },
            {
                "title": "Instagram Algorithm & Content Strategy 2026",
                "snippet": "The Instagram algorithm rewards saves, shares, and extended view time. Carousels outperform single-image posts by 1.4x in reach. Stories with polls increase engagement by 40%.",
                "url": "https://content-strategy.example.com/instagram-2026",
            },
        ]

    def browse_url(self, url: str) -> str:
        return f"Scraped content from {url}: Instagram best practices emphasize visual consistency, educational value, strong hooks on Slide 1, and clear lead-generation CTAs."


class MockInstagramTool(InstagramTool):
    """Mock Instagram API for account data, publishing, and insights."""

    def instagram_fetch_account(self, account_id: str) -> Dict[str, Any]:
        return {
            "account_id": account_id,
            "username": "brandaccount",
            "followers_count": 15000,
            "media_count": 240,
            "biography": "Industry leader | Educational content | DM for collabs",
            "account_type": "BUSINESS",
        }

    def instagram_fetch_media(self, account_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        return [
            {
                "id": "media_001",
                "media_type": "CAROUSEL_ALBUM",
                "caption": "5 strategies that transformed our growth...",
                "like_count": 342,
                "comments_count": 58,
                "timestamp": "2026-09-15T10:00:00",
            },
            {
                "id": "media_002",
                "media_type": "IMAGE",
                "caption": "The truth about industry growth...",
                "like_count": 189,
                "comments_count": 24,
                "timestamp": "2026-09-12T14:00:00",
            },
        ]

    def instagram_publish(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "published_mock",
            "media_id": "ig_media_mock_12345",
            "permalink": "https://www.instagram.com/p/mock12345/",
        }

    def instagram_fetch_insights(self, media_id: str) -> Dict[str, Any]:
        return {
            "media_id": media_id,
            "reach": 4520,
            "impressions": 8900,
            "likes": 342,
            "comments": 58,
            "shares": 87,
            "saves": 215,
            "profile_visits": 156,
            "engagement_rate": 4.8,
        }
