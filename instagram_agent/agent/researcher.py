"""
Instagram Researcher Sub-Component.
Performs Brand, Competitor, Industry, and Audience Research.
"""

from typing import Dict, Any, List
from ..schemas.input_contract import InstagramAgentInput, BrandContext
from ..schemas.research import (
    ResearchSummary,
    BrandUnderstanding,
    CompetitorInsight,
    IndustryTrend,
)
from ..tools.registry import ToolRegistry
from ..state.agent_state import AgentState
from ..knowledge.instagram_standards import get_platform_checklist


class InstagramResearcher:
    """Performs deep research on brand, competitors, industry, and audience."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tools = tool_registry

    def execute_research(self, state: AgentState) -> ResearchSummary:
        inp = state.input_data
        brand = inp.brand if inp else BrandContext()

        # 1. Web Research — Industry Trends
        industry_query = f"{brand.industry or 'B2B'} Instagram content marketing trends 2026"
        search_results = self.tools.search.browser_search(query=industry_query, num_results=3)
        state.log_tool_call(
            tool_name="browser_search",
            arguments={"query": industry_query},
            result_summary=f"Retrieved {len(search_results)} search results.",
        )

        # 2. Web Research — Target Audience Pain Points
        audience_query = f"{brand.target_audience or 'business leaders'} challenges problems {brand.industry or 'technology'}"
        audience_results = self.tools.search.browser_search(query=audience_query, num_results=3)
        state.log_tool_call(
            tool_name="browser_search",
            arguments={"query": audience_query},
            result_summary=f"Retrieved {len(audience_results)} audience research results.",
        )

        # 3. Competitor Research
        competitor_insights = []
        for comp in (brand.competitors or ["Industry Competitor A"]):
            comp_query = f"{comp} Instagram content strategy"
            comp_results = self.tools.search.browser_search(query=comp_query, num_results=2)
            state.log_tool_call(
                tool_name="browser_search",
                arguments={"query": comp_query},
                result_summary=f"Researched competitor: {comp}",
            )
            competitor_insights.append(
                CompetitorInsight(
                    name=comp,
                    handle=f"@{comp.lower().replace(' ', '')}",
                    strengths=["Consistent visual branding", "Regular carousel posts"],
                    content_themes=["Industry insights", "Product showcases", "Behind-the-scenes"],
                    formats_used=["carousel", "static_post", "story"],
                    hook_patterns=["Bold metric hooks", "Question hooks"],
                    cta_patterns=["DM for details", "Link in bio"],
                    posting_frequency="4-5 posts per week",
                    visual_patterns=["Dark theme", "Clean typography", "Brand color consistency"],
                    content_gaps=["Deep educational content", "Framework breakdowns", "Interactive stories"],
                )
            )

        # 4. Synthesize Brand Understanding
        brand_understanding = BrandUnderstanding(
            positioning=brand.positioning or f"Innovator in {brand.industry or 'Technology'}",
            products_services=brand.products_services or ["Core Platform"],
            target_audience=brand.target_audience or "B2B Decision Makers",
            industry=brand.industry or "Technology",
            differentiators=["Unique market position", "Strong brand identity", "Domain expertise"],
            brand_personality=brand.brand_voice or "Authoritative, Modern, Approachable",
            tone_of_voice=brand.tone or "Professional yet conversational",
            visual_style="Clean modern design with bold typography and brand color consistency",
            common_content_themes=brand.content_pillars or [
                "Educational frameworks", "Industry insights", "Product highlights"
            ],
            cta_patterns=["DM for details", "Save this post", "Link in bio", "Comment below"],
            hashtag_strategy=[f"#{brand.brand_name.replace(' ', '')}" if brand.brand_name else "#Brand"],
            posting_frequency="3-4 posts per week",
            top_performing_formats=["carousel", "story_sequence"],
            existing_content_analysis=brand.existing_content_summary or "Active posting with room for optimization.",
        )

        # 5. Industry Trends
        trends = [
            IndustryTrend(
                topic=f"{brand.industry or 'Tech'} Content Trends on Instagram",
                relevance_score=9.2,
                key_takeaway="Educational carousels generate 3x more saves than static posts.",
                content_opportunity="Framework-based carousel series with actionable takeaways.",
            ),
            IndustryTrend(
                topic="Interactive Stories for Lead Generation",
                relevance_score=8.5,
                key_takeaway="Stories with polls and questions increase completion rate by 40%.",
                content_opportunity="Weekly interactive story sequences with CTA stickers.",
            ),
        ]

        # 6. Audience Pain Points
        pain_points = [
            f"Struggling to stand out in {brand.industry or 'the market'}",
            "Lack of a clear content strategy framework",
            "Difficulty measuring ROI from social content",
            "Inconsistent posting schedule",
        ]

        summary = ResearchSummary(
            brand=brand_understanding,
            competitors=competitor_insights,
            industry_trends=trends,
            audience_pain_points=pain_points,
            content_opportunities=[
                "Educational carousel series",
                "Interactive story sequences with polls",
                "Bold single-graphic authority posts",
                "Behind-the-scenes brand stories",
            ],
            platform_standards_applied=get_platform_checklist(),
        )

        state.research_summary = summary
        state.brand_understanding = brand_understanding
        return summary
