"""
Instagram Reviser Sub-Component.
Applies critic feedback to refine content drafts.
"""

from typing import Dict, Any
from ..schemas.critique import CritiqueResult
from ..tools.registry import ToolRegistry
from ..state.agent_state import AgentState
from ..schemas.output_contract import CarouselSlide
from ..creative.carousel_generator import generate_carousel_slide_svg
from ..creative.static_post_generator import generate_static_post_svg
from ..creative.story_generator import generate_story_frame_svg


class InstagramReviser:
    """Refines Instagram content based on critic feedback."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tools = tool_registry

    def revise(self, critique: CritiqueResult, state: AgentState) -> Dict[str, Any]:
        """Apply critique feedback to revise the current content."""
        content_type = state.input_data.constraints.content_type if state.input_data else "carousel"
        brand = state.input_data.brand if state.input_data else None
        brand_name = brand.brand_name if brand else "Brand"
        colors = brand.colors if brand else None
        next_version = len(state.content_versions) + 1
        version_label = f"{content_type}_v{next_version}"

        prompt = f"""
Revise the Instagram content based on this critique:

REQUIRED CHANGES:
{chr(10).join(['- ' + c for c in critique.required_changes])}

ISSUES TO FIX:
{chr(10).join(['- ' + i for i in critique.issues])}

Content Type: {content_type}
Brand: {brand_name}
        """

        raw_revised = self.tools.text_gen.generate_text(
            prompt=prompt,
            system_prompt="You are an expert Instagram content editor specializing in high-impact optimization.",
            temperature=0.5,
        )
        state.log_tool_call(
            tool_name="generate_text",
            arguments={"task": "revise_content", "version": version_label},
            result_summary=f"Revised content to create {version_label}.",
        )

        # Apply revisions based on content type
        if content_type == "carousel" and state.carousel:
            carousel = state.carousel
            # Strengthen hook on slide 1
            if carousel.slides:
                carousel.slides[0].copy = f"The counterintuitive strategy top 1% brands use (that 90% ignore). Here's why most {state.strategy.target_audience if state.strategy else 'professionals'} get this wrong."
                carousel.slides[0].graphic_svg = generate_carousel_slide_svg(
                    slide_number=1,
                    total_slides=carousel.total_slides,
                    title=carousel.slides[0].slide_title,
                    copy=carousel.slides[0].copy,
                    brand_name=brand_name,
                    colors=colors,
                    slide_type="hook",
                )
            # Strengthen CTA on last slide
            if len(carousel.slides) > 1:
                last = carousel.slides[-1]
                last.copy = f"Save this post and DM us '{brand_name.upper().split()[0] if brand_name else 'GUIDE'}' for the free strategy blueprint ↗"
                last.graphic_svg = generate_carousel_slide_svg(
                    slide_number=carousel.total_slides,
                    total_slides=carousel.total_slides,
                    title=last.slide_title,
                    copy=last.copy,
                    brand_name=brand_name,
                    colors=colors,
                    slide_type="cta",
                )
            carousel.hook = carousel.slides[0].copy if carousel.slides else carousel.hook

        elif content_type == "static_post" and state.static_post:
            static = state.static_post
            static.headline = f"The Uncomfortable Truth About {state.input_data.task.topic if state.input_data else 'Growth'}"
            static.cta = f"Double tap if you agree. DM '{brand_name.upper().split()[0] if brand_name else 'GUIDE'}' for the full breakdown ↗"
            static.graphic_svg = generate_static_post_svg(
                headline=static.headline,
                supporting_copy=static.supporting_copy,
                cta="Get The Guide →",
                brand_name=brand_name,
                category=static.category,
                colors=colors,
            )

        elif content_type == "story_sequence" and state.story_sequence:
            seq = state.story_sequence
            if seq.stories:
                seq.stories[0].headline = f"Wait... Did You Know This?"
                seq.stories[0].graphic_svg = generate_story_frame_svg(
                    story_number=1,
                    total_stories=seq.total_stories,
                    headline=seq.stories[0].headline,
                    copy=seq.stories[0].copy,
                    story_type=seq.stories[0].story_type,
                    interactive_element=seq.stories[0].interactive_element,
                    brand_name=brand_name,
                    colors=colors,
                )

        state.add_content_version(version_label, {"type": content_type, "revision": True})
        return {"version": version_label, "applied_changes": len(critique.required_changes)}
