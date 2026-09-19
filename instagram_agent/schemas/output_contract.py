"""
Output Contract Schemas for Instagram Specialist Agent.
Covers: Carousels, Static Posts, Stories, Calendars, Hooks, Captions,
        Creative Assets, Approval Workflow, Publishing, Analytics, Quality.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from .strategy import InstagramStrategy
from .research import ResearchSummary


# ─── Hooks & Captions ───────────────────────────────────────────────

@dataclass
class HookVariant:
    style: str = "Curiosity"
    hook_text: str = ""
    rationale: str = ""
    angle: str = ""


@dataclass
class CaptionDraft:
    version: str = "v1"
    caption_text: str = ""
    hashtags: List[str] = field(default_factory=list)


# ─── Carousel ────────────────────────────────────────────────────────

@dataclass
class CarouselSlide:
    slide_number: int = 1
    slide_title: str = ""
    copy: str = ""
    visual_direction: str = ""
    visual_element: str = ""
    graphic_asset_url: str = ""
    graphic_svg: str = ""


@dataclass
class CarouselContent:
    title: str = ""
    objective: str = ""
    audience: str = ""
    hook: str = ""
    total_slides: int = 0
    slides: List[CarouselSlide] = field(default_factory=list)
    cta: str = ""
    caption: str = ""
    brand_styling: Dict[str, Any] = field(default_factory=dict)
    design_instructions: str = ""


# ─── Static Post ──────────────────────────────────────────────────────

@dataclass
class StaticPostContent:
    concept: str = ""
    category: str = "Educational"
    headline: str = ""
    supporting_copy: str = ""
    cta: str = ""
    caption: str = ""
    visual_direction: str = ""
    graphic_asset_url: str = ""
    graphic_svg: str = ""


# ─── Story Sequence ───────────────────────────────────────────────────

@dataclass
class StoryFrame:
    story_number: int = 1
    story_type: str = "educational"
    # educational | promotional | poll | question | cta | lead_generation
    headline: str = ""
    copy: str = ""
    visual_direction: str = ""
    interactive_element: str = ""  # poll, question_sticker, link_sticker, etc.
    graphic_asset_url: str = ""
    graphic_svg: str = ""


@dataclass
class StorySequenceContent:
    sequence_title: str = ""
    objective: str = ""
    total_stories: int = 0
    stories: List[StoryFrame] = field(default_factory=list)
    cta: str = ""


# ─── Content Calendar ─────────────────────────────────────────────────

@dataclass
class CalendarEntry:
    date: str = ""
    day_of_week: str = ""
    topic: str = ""
    format: str = "carousel"
    content_pillar: str = ""
    hook: str = ""
    cta: str = ""
    status: str = "Draft"
    # IDEA | DRAFT | GENERATED | REVIEW | APPROVED | SCHEDULED | PUBLISHED | FAILED
    objective: str = ""
    notes: str = ""


@dataclass
class ContentCalendar:
    duration: str = "1 Week"
    total_posts: int = 0
    calendar_entries: List[CalendarEntry] = field(default_factory=list)
    format_distribution: Dict[str, int] = field(default_factory=dict)


# ─── Creative Assets ──────────────────────────────────────────────────

@dataclass
class CreativeAsset:
    asset_id: str = ""
    format: str = "carousel_slide"
    # carousel_slide | static_post | story_frame
    prompt: str = ""
    description: str = ""
    status: str = "generated"
    dimensions: str = "1080x1080"
    url: str = ""
    svg_content: str = ""


@dataclass
class CreativeSummary:
    required: bool = False
    assets: List[CreativeAsset] = field(default_factory=list)


# ─── Approval Workflow ────────────────────────────────────────────────

@dataclass
class ApprovalState:
    current_status: str = "REVIEW"
    # DRAFT | GENERATED | REVIEW | APPROVED | SCHEDULED | PUBLISHED | FAILED
    allowed_transitions: List[str] = field(default_factory=lambda: [
        "APPROVE", "REJECT", "REGENERATE", "EDIT"
    ])
    version_history: List[Dict[str, str]] = field(default_factory=list)
    feedback_history: List[Dict[str, str]] = field(default_factory=list)


# ─── Quality Metrics ──────────────────────────────────────────────────

@dataclass
class QualityMetrics:
    status: str = "passed"
    overall_score: float = 10.0
    issues: List[str] = field(default_factory=list)
    iterations: int = 1


# ─── Missing Context ──────────────────────────────────────────────────

@dataclass
class MissingContextRequirement:
    missing_fields: List[str] = field(default_factory=list)
    why_needed: str = ""
    workaround_status: str = ""


# ─── Reels Notice ─────────────────────────────────────────────────────

@dataclass
class ReelsNotice:
    notice: str = "Reels — Coming Soon"
    coming_soon: bool = True
    future_architecture: List[str] = field(default_factory=lambda: [
        "Reel Strategy Engine",
        "Script Generator",
        "Scene Breakdown Planner",
        "Motion Graphics Generator",
        "Voiceover Integration",
        "Caption/Subtitle Generator",
        "Video Rendering Pipeline",
        "Reel Publishing via Meta API",
    ])


# ─── Root Output Contract ─────────────────────────────────────────────

@dataclass
class InstagramAgentOutput:
    """Root output returned to Agent Orchestrator."""
    status: str = "ready_for_review"
    # ready_for_review | coming_soon | missing_context | error
    platform: str = "instagram"
    task: str = "create_content"
    content_type: str = "carousel"
    # carousel | static_post | story_sequence | content_calendar

    brand_summary: Optional[Dict[str, Any]] = None
    research: Optional[ResearchSummary] = None
    strategy: Optional[InstagramStrategy] = None

    hooks: List[HookVariant] = field(default_factory=list)
    captions: List[CaptionDraft] = field(default_factory=list)

    carousel: Optional[CarouselContent] = None
    static_post: Optional[StaticPostContent] = None
    story_sequence: Optional[StorySequenceContent] = None
    calendar: Optional[ContentCalendar] = None

    creative: CreativeSummary = field(default_factory=CreativeSummary)
    approval_state: Optional[ApprovalState] = None

    publishing_result: Optional[Dict[str, Any]] = None
    analytics_report: Optional[Dict[str, Any]] = None

    quality: QualityMetrics = field(default_factory=QualityMetrics)

    missing_context: Optional[MissingContextRequirement] = None
    reels_notice: Optional[ReelsNotice] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "platform": self.platform,
            "task": self.task,
            "content_type": self.content_type,
            "brand_summary": self.brand_summary,
            "research": self.research.to_dict() if self.research else None,
            "strategy": self.strategy.to_dict() if self.strategy else None,
            "hooks": [asdict(h) for h in self.hooks],
            "captions": [asdict(c) for c in self.captions],
            "carousel": asdict(self.carousel) if self.carousel else None,
            "static_post": asdict(self.static_post) if self.static_post else None,
            "story_sequence": asdict(self.story_sequence) if self.story_sequence else None,
            "calendar": asdict(self.calendar) if self.calendar else None,
            "creative": {
                "required": self.creative.required,
                "assets": [asdict(a) for a in self.creative.assets],
            },
            "approval_state": asdict(self.approval_state) if self.approval_state else None,
            "publishing_result": self.publishing_result,
            "analytics_report": self.analytics_report,
            "quality": asdict(self.quality),
            "missing_context": asdict(self.missing_context) if self.missing_context else None,
            "reels_notice": asdict(self.reels_notice) if self.reels_notice else None,
        }
