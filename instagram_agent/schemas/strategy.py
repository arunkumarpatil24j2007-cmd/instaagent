"""
Strategy Schema for Instagram Specialist Agent.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional


@dataclass
class ContentIdea:
    """A single content idea with format, pillar, and creative direction."""
    title: str = ""
    format: str = "carousel"  # carousel | static_post | story_sequence
    content_pillar: str = "Educational"
    objective: str = "lead_generation"
    hook: str = ""
    core_idea: str = ""
    cta: str = ""
    visual_direction: str = ""
    caption_direction: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContentIdea":
        return cls(**{k: data.get(k, v) for k, v in cls.__dataclass_fields__.items()})


@dataclass
class InstagramStrategy:
    """Complete content strategy for Instagram."""
    brand_name: str = ""
    objective: str = "lead_generation"
    content_pillars: List[str] = field(default_factory=lambda: [
        "Educational", "Authority", "Social Proof", "Product/Service", "Engagement"
    ])
    format_mix_percentage: Dict[str, int] = field(default_factory=lambda: {
        "carousel": 50, "static_post": 20, "story_sequence": 30
    })
    content_ideas: List[ContentIdea] = field(default_factory=list)
    strategic_recommendations: List[str] = field(default_factory=list)
    target_audience: str = ""
    content_angle: str = ""
    tone_and_style: str = ""
    posting_frequency: str = "3-4 posts per week"
    best_posting_times: List[str] = field(default_factory=lambda: [
        "Tuesday 9AM", "Thursday 12PM", "Saturday 10AM"
    ])

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstagramStrategy":
        ideas = [ContentIdea.from_dict(i) for i in data.get("content_ideas", [])]
        return cls(
            brand_name=data.get("brand_name", ""),
            objective=data.get("objective", "lead_generation"),
            content_pillars=data.get("content_pillars", [
                "Educational", "Authority", "Social Proof", "Product/Service", "Engagement"
            ]),
            format_mix_percentage=data.get("format_mix_percentage", {
                "carousel": 50, "static_post": 20, "story_sequence": 30
            }),
            content_ideas=ideas,
            strategic_recommendations=data.get("strategic_recommendations", []),
            target_audience=data.get("target_audience", ""),
            content_angle=data.get("content_angle", ""),
            tone_and_style=data.get("tone_and_style", ""),
            posting_frequency=data.get("posting_frequency", "3-4 posts per week"),
            best_posting_times=data.get("best_posting_times", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
