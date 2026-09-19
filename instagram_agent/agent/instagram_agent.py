"""
Main Instagram Specialist Agent Controller.
Autonomous execution loop:
  Research → Strategy → Draft → Critique → Revision Loop → Polish → Output.

Supports: Carousels, Static Posts, Story Sequences, Content Calendars.
Reels: Coming Soon (returns notice, does not generate).
"""

from typing import Dict, Any, Optional
from ..schemas.input_contract import InstagramAgentInput
from ..schemas.output_contract import (
    InstagramAgentOutput,
    CreativeSummary,
    CreativeAsset,
    QualityMetrics,
    MissingContextRequirement,
    ApprovalState,
    ReelsNotice,
    HookVariant,
    CaptionDraft,
)
from ..state.agent_state import AgentState
from ..tools.registry import ToolRegistry
from .researcher import InstagramResearcher
from .strategy_planner import StrategyPlanner
from .writer import InstagramWriter
from .critic import InstagramCritic
from .reviser import InstagramReviser
from .polisher import InstagramPolisher
from .calendar_planner import CalendarPlanner


class InstagramSpecialistAgent:
    """Standalone Instagram Specialist Agent.

    Called by the Agent Orchestrator with structured input.
    Returns structured output. Never communicates directly with the user.
    """

    def __init__(self, tool_registry: Optional[ToolRegistry] = None):
        self.tools = tool_registry or ToolRegistry()
        self.researcher = InstagramResearcher(self.tools)
        self.strategy_planner = StrategyPlanner(self.tools)
        self.writer = InstagramWriter(self.tools)
        self.critic = InstagramCritic(self.tools)
        self.reviser = InstagramReviser(self.tools)
        self.polisher = InstagramPolisher(self.tools)
        self.calendar_planner = CalendarPlanner(self.tools)

    def run(self, input_data: InstagramAgentInput) -> InstagramAgentOutput:
        """
        Main entrypoint called by the external Agent Orchestrator.
        Takes structured input and returns structured output contract.
        """
        state = AgentState(
            input_data=input_data,
            max_iterations=input_data.constraints.max_iterations,
        )

        content_type = input_data.constraints.content_type
        task_format = input_data.task.target_format

        # ─── REELS: Coming Soon ───────────────────────────────────
        if content_type == "reel" or task_format == "reel":
            return InstagramAgentOutput(
                status="coming_soon",
                platform="instagram",
                task=input_data.task.type,
                content_type="reel",
                reels_notice=ReelsNotice(),
            )

        # ─── 1. Check for Missing Critical Context ────────────────
        missing_fields = []
        if not input_data.brand.brand_name:
            missing_fields.append("brand.brand_name")
        if not input_data.task.topic and not input_data.task.objective:
            missing_fields.append("task.topic or task.objective")

        if missing_fields:
            state.current_status = "missing_context"
            missing_req = MissingContextRequirement(
                missing_fields=missing_fields,
                why_needed="Required to ground Instagram content strategy and brand positioning accurately.",
                workaround_status="Cannot generate brand-aligned content without basic brand identity.",
            )
            state.missing_context = missing_req
            return InstagramAgentOutput(
                status="missing_context",
                platform="instagram",
                task=input_data.task.type,
                content_type=content_type,
                missing_context=missing_req,
            )

        # ─── 2. Research Phase ────────────────────────────────────
        state.current_status = "researching"
        research_summary = self.researcher.execute_research(state)

        # ─── 3. Strategy Phase ────────────────────────────────────
        state.current_status = "strategizing"
        strategy = self.strategy_planner.create_strategy(state)

        # ─── 4. Content Generation Phase ──────────────────────────
        state.current_status = "drafting"

        if content_type == "content_calendar" or task_format == "content_calendar":
            # Calendar generation (no critique loop needed)
            calendar = self.calendar_planner.create_calendar(state)
            state.current_status = "completed"
            return self._build_output(state, input_data, research_summary, strategy)

        # Generate content based on format
        if content_type == "carousel" or task_format == "carousel":
            self.writer.write_carousel(state)
        elif content_type == "static_post" or task_format == "static_post":
            self.writer.write_static_post(state)
        elif content_type == "story_sequence" or task_format == "story_sequence":
            self.writer.write_story_sequence(state)
        else:
            # Default to carousel
            self.writer.write_carousel(state)

        # Generate hooks and captions
        hooks = self.writer.generate_hooks(state)
        captions = self.writer.generate_captions(state, content_type)

        # ─── 5. Critique & Revision Loop ──────────────────────────
        state.current_status = "critiquing"
        content_summary = state.get_latest_content() or {"type": content_type}
        critique = self.critic.evaluate(content_summary, state)

        while critique.status == "needs_revision" and state.iteration_count < state.max_iterations - 1:
            state.iteration_count += 1
            state.current_status = "revising"
            self.reviser.revise(critique, state)

            state.current_status = "critiquing"
            content_summary = state.get_latest_content() or {"type": content_type}
            critique = self.critic.evaluate(content_summary, state)

        # ─── 6. Final Polish ──────────────────────────────────────
        state.current_status = "polishing"
        self.polisher.polish(state)

        state.current_status = "completed"

        # ─── 7. Build Output ──────────────────────────────────────
        output = self._build_output(state, input_data, research_summary, strategy)
        output.hooks = hooks
        output.captions = captions
        return output

    def _build_output(self, state, input_data, research_summary, strategy):
        """Assemble the final structured output contract."""
        content_type = input_data.constraints.content_type

        # Assemble creative assets list
        creative_assets = []
        if state.carousel:
            for slide in state.carousel.slides:
                creative_assets.append(CreativeAsset(
                    asset_id=f"carousel_slide_{slide.slide_number}",
                    format="carousel_slide",
                    prompt=slide.visual_direction,
                    description=f"Slide {slide.slide_number}: {slide.slide_title}",
                    status="generated",
                    dimensions="1080x1080",
                    url=slide.graphic_asset_url,
                    svg_content=slide.graphic_svg,
                ))
        if state.static_post:
            creative_assets.append(CreativeAsset(
                asset_id="static_post_graphic",
                format="static_post",
                prompt=state.static_post.visual_direction,
                description=state.static_post.headline,
                status="generated",
                dimensions="1080x1080",
                url=state.static_post.graphic_asset_url,
                svg_content=state.static_post.graphic_svg,
            ))
        if state.story_sequence:
            for story in state.story_sequence.stories:
                creative_assets.append(CreativeAsset(
                    asset_id=f"story_frame_{story.story_number}",
                    format="story_frame",
                    prompt=story.visual_direction,
                    description=f"Story {story.story_number}: {story.headline}",
                    status="generated",
                    dimensions="1080x1920",
                    url=story.graphic_asset_url,
                    svg_content=story.graphic_svg,
                ))

        # Quality metrics
        quality = QualityMetrics(
            status=state.latest_critique.status if state.latest_critique else "passed",
            overall_score=state.latest_critique.overall_score if state.latest_critique else 9.5,
            issues=state.latest_critique.issues if state.latest_critique else [],
            iterations=len(state.content_versions),
        )

        # Approval state
        approval = ApprovalState(
            current_status="REVIEW" if input_data.constraints.approval_required else "APPROVED",
            allowed_transitions=["APPROVE", "REJECT", "REGENERATE", "EDIT"],
            version_history=[{"version": k} for k in state.content_versions.keys()],
        )

        # Brand summary
        brand_summary = {
            "brand_name": input_data.brand.brand_name,
            "industry": input_data.brand.industry,
            "target_audience": input_data.brand.target_audience,
            "account_handle": input_data.brand.account_handle,
            "brand_voice": input_data.brand.brand_voice,
            "colors": input_data.brand.colors,
        }

        return InstagramAgentOutput(
            status="ready_for_review",
            platform="instagram",
            task=input_data.task.type,
            content_type=content_type,
            brand_summary=brand_summary,
            research=research_summary,
            strategy=strategy,
            carousel=state.carousel,
            static_post=state.static_post,
            story_sequence=state.story_sequence,
            calendar=state.calendar,
            creative=CreativeSummary(
                required=bool(creative_assets),
                assets=creative_assets,
            ),
            approval_state=approval,
            publishing_result=None,
            analytics_report=None,
            quality=quality,
            missing_context=None,
            reels_notice=None,
        )

    def run_raw(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Convenience method accepting raw JSON/dict input payload from Orchestrator."""
        input_data = InstagramAgentInput.from_dict(input_dict)
        output = self.run(input_data)
        return output.to_dict()
