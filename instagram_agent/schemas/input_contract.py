"""
Input Contract Schemas for Instagram Specialist Agent.
Accepts brand context, task spec, and constraints from the Agent Orchestrator.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List


@dataclass
class BrandContext:
    """Complete brand identity and positioning context."""
    brand_name: str = ""
    industry: str = ""
    location: str = ""
    target_audience: str = ""
    buyer_persona: str = ""
    products_services: List[str] = field(default_factory=list)
    offers: List[str] = field(default_factory=list)
    positioning: str = ""
    brand_voice: str = ""
    tone: str = ""
    colors: List[str] = field(default_factory=list)
    typography: Dict[str, str] = field(default_factory=dict)
    competitors: List[str] = field(default_factory=list)
    content_pillars: List[str] = field(default_factory=list)
    business_goals: List[str] = field(default_factory=list)
    marketing_objectives: List[str] = field(default_factory=list)
    account_handle: str = ""
    website: str = ""
    existing_content_summary: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BrandContext":
        return cls(
            brand_name=data.get("brand_name", ""),
            industry=data.get("industry", ""),
            location=data.get("location", ""),
            target_audience=data.get("target_audience", ""),
            buyer_persona=data.get("buyer_persona", ""),
            products_services=data.get("products_services", []),
            offers=data.get("offers", []),
            positioning=data.get("positioning", ""),
            brand_voice=data.get("brand_voice", ""),
            tone=data.get("tone", ""),
            colors=data.get("colors", ["#0F172A", "#38BDF8", "#F43F5E"]),
            typography=data.get("typography", {"heading": "Outfit", "body": "Inter"}),
            competitors=data.get("competitors", []),
            content_pillars=data.get("content_pillars", []),
            business_goals=data.get("business_goals", []),
            marketing_objectives=data.get("marketing_objectives", []),
            account_handle=data.get("account_handle", ""),
            website=data.get("website", ""),
            existing_content_summary=data.get("existing_content_summary", ""),
        )


@dataclass
class TaskSpec:
    """Defines what the agent should do."""
    type: str = "create_content"
    # create_content | create_content_calendar | create_strategy | research
    # analytics | approval_action | reels_generate
    topic: str = ""
    objective: str = "lead_generation"
    # lead_generation | brand_awareness | authority | engagement | sales
    target_format: str = "carousel"
    # carousel | static_post | story_sequence | reel | content_calendar
    custom_params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskSpec":
        return cls(
            type=data.get("type", "create_content"),
            topic=data.get("topic", ""),
            objective=data.get("objective", "lead_generation"),
            target_format=data.get("target_format", "carousel"),
            custom_params=data.get("custom_params", {}),
        )


@dataclass
class Constraints:
    """Execution and content constraints."""
    content_type: str = "carousel"
    language: str = "English"
    max_slides: int = 6
    max_stories: int = 5
    approval_required: bool = True
    max_iterations: int = 3
    tone_override: Optional[str] = None
    calendar_duration: str = "1_week"  # 1_week | 2_weeks | 1_month
    posts_per_week: int = 4

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Constraints":
        return cls(
            content_type=data.get("content_type", "carousel"),
            language=data.get("language", "English"),
            max_slides=data.get("max_slides", 6),
            max_stories=data.get("max_stories", 5),
            approval_required=data.get("approval_required", True),
            max_iterations=data.get("max_iterations", 3),
            tone_override=data.get("tone_override"),
            calendar_duration=data.get("calendar_duration", "1_week"),
            posts_per_week=data.get("posts_per_week", 4),
        )


@dataclass
class InstagramAgentInput:
    """Root input contract for the Instagram Specialist Agent."""
    brand: BrandContext = field(default_factory=BrandContext)
    task: TaskSpec = field(default_factory=TaskSpec)
    constraints: Constraints = field(default_factory=Constraints)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstagramAgentInput":
        return cls(
            brand=BrandContext.from_dict(data.get("brand", {})),
            task=TaskSpec.from_dict(data.get("task", {})),
            constraints=Constraints.from_dict(data.get("constraints", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
