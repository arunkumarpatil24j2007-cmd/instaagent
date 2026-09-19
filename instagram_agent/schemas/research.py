"""
Research Schemas for Instagram Specialist Agent.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional


@dataclass
class BrandUnderstanding:
    """Synthesized understanding of the brand from research."""
    positioning: str = ""
    products_services: List[str] = field(default_factory=list)
    target_audience: str = ""
    industry: str = ""
    differentiators: List[str] = field(default_factory=list)
    brand_personality: str = ""
    tone_of_voice: str = ""
    visual_style: str = ""
    common_content_themes: List[str] = field(default_factory=list)
    cta_patterns: List[str] = field(default_factory=list)
    hashtag_strategy: List[str] = field(default_factory=list)
    posting_frequency: str = ""
    top_performing_formats: List[str] = field(default_factory=list)
    existing_content_analysis: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BrandUnderstanding":
        return cls(
            positioning=data.get("positioning", ""),
            products_services=data.get("products_services", []),
            target_audience=data.get("target_audience", ""),
            industry=data.get("industry", ""),
            differentiators=data.get("differentiators", []),
            brand_personality=data.get("brand_personality", ""),
            tone_of_voice=data.get("tone_of_voice", ""),
            visual_style=data.get("visual_style", ""),
            common_content_themes=data.get("common_content_themes", []),
            cta_patterns=data.get("cta_patterns", []),
            hashtag_strategy=data.get("hashtag_strategy", []),
            posting_frequency=data.get("posting_frequency", ""),
            top_performing_formats=data.get("top_performing_formats", []),
            existing_content_analysis=data.get("existing_content_analysis", ""),
        )


@dataclass
class CompetitorInsight:
    """Analysis of a competitor's Instagram presence."""
    name: str = ""
    handle: str = ""
    strengths: List[str] = field(default_factory=list)
    content_themes: List[str] = field(default_factory=list)
    formats_used: List[str] = field(default_factory=list)
    hook_patterns: List[str] = field(default_factory=list)
    cta_patterns: List[str] = field(default_factory=list)
    posting_frequency: str = ""
    visual_patterns: List[str] = field(default_factory=list)
    content_gaps: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompetitorInsight":
        return cls(
            name=data.get("name", ""),
            handle=data.get("handle", ""),
            strengths=data.get("strengths", []),
            content_themes=data.get("content_themes", []),
            formats_used=data.get("formats_used", []),
            hook_patterns=data.get("hook_patterns", []),
            cta_patterns=data.get("cta_patterns", []),
            posting_frequency=data.get("posting_frequency", ""),
            visual_patterns=data.get("visual_patterns", []),
            content_gaps=data.get("content_gaps", []),
        )


@dataclass
class IndustryTrend:
    """A trending topic or conversation in the industry."""
    topic: str = ""
    relevance_score: float = 0.0
    key_takeaway: str = ""
    content_opportunity: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IndustryTrend":
        return cls(
            topic=data.get("topic", ""),
            relevance_score=data.get("relevance_score", 0.0),
            key_takeaway=data.get("key_takeaway", ""),
            content_opportunity=data.get("content_opportunity", ""),
        )


@dataclass
class ResearchSummary:
    """Complete research output for the Instagram Agent."""
    brand: BrandUnderstanding = field(default_factory=BrandUnderstanding)
    competitors: List[CompetitorInsight] = field(default_factory=list)
    industry_trends: List[IndustryTrend] = field(default_factory=list)
    audience_pain_points: List[str] = field(default_factory=list)
    content_opportunities: List[str] = field(default_factory=list)
    platform_standards_applied: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResearchSummary":
        return cls(
            brand=BrandUnderstanding.from_dict(data.get("brand", {})),
            competitors=[CompetitorInsight.from_dict(c) for c in data.get("competitors", [])],
            industry_trends=[IndustryTrend.from_dict(i) for i in data.get("industry_trends", [])],
            audience_pain_points=data.get("audience_pain_points", []),
            content_opportunities=data.get("content_opportunities", []),
            platform_standards_applied=data.get("platform_standards_applied", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
