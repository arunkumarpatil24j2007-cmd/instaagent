"""
Internal Agent Context and Execution State for Instagram Specialist Agent.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
import time

from ..schemas.input_contract import InstagramAgentInput
from ..schemas.strategy import InstagramStrategy
from ..schemas.research import ResearchSummary, BrandUnderstanding
from ..schemas.critique import CritiqueResult
from ..schemas.output_contract import (
    CarouselContent, StaticPostContent, StorySequenceContent,
    ContentCalendar, MissingContextRequirement,
)


@dataclass
class ToolCallLog:
    tool_name: str
    arguments: Dict[str, Any]
    result_summary: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class AgentState:
    """Tracks all pipeline state across the Instagram Agent execution."""
    input_data: Optional[InstagramAgentInput] = None
    current_status: str = "initialized"
    # initialized | researching | strategizing | drafting | critiquing
    # revising | polishing | generating_creative | completed
    # missing_context | coming_soon | failed
    iteration_count: int = 0
    max_iterations: int = 3

    # Research state
    research_summary: Optional[ResearchSummary] = None
    brand_understanding: Optional[BrandUnderstanding] = None

    # Strategy state
    strategy: Optional[InstagramStrategy] = None

    # Content drafts (keyed by format + version, e.g. "carousel_v1")
    content_versions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    latest_version_key: Optional[str] = None

    # Generated content
    carousel: Optional[CarouselContent] = None
    static_post: Optional[StaticPostContent] = None
    story_sequence: Optional[StorySequenceContent] = None
    calendar: Optional[ContentCalendar] = None

    # Critique state
    critique_history: List[CritiqueResult] = field(default_factory=list)
    latest_critique: Optional[CritiqueResult] = None

    # Missing Context
    missing_context: Optional[MissingContextRequirement] = None

    # Audit & Tool execution history
    tool_call_history: List[ToolCallLog] = field(default_factory=list)

    def log_tool_call(self, tool_name: str, arguments: Dict[str, Any], result_summary: str):
        self.tool_call_history.append(
            ToolCallLog(tool_name=tool_name, arguments=arguments, result_summary=result_summary)
        )

    def add_content_version(self, version_label: str, content: Dict[str, Any]):
        self.content_versions[version_label] = content
        self.latest_version_key = version_label

    def get_latest_content(self) -> Optional[Dict[str, Any]]:
        if self.latest_version_key and self.latest_version_key in self.content_versions:
            return self.content_versions[self.latest_version_key]
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_status": self.current_status,
            "iteration_count": self.iteration_count,
            "max_iterations": self.max_iterations,
            "research_summary": self.research_summary.to_dict() if self.research_summary else None,
            "strategy": self.strategy.to_dict() if self.strategy else None,
            "content_versions": list(self.content_versions.keys()),
            "latest_version_key": self.latest_version_key,
            "latest_critique": self.latest_critique.to_dict() if self.latest_critique else None,
            "missing_context": asdict(self.missing_context) if self.missing_context else None,
            "tool_call_count": len(self.tool_call_history),
        }
