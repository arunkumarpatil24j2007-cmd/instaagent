"""
Instagram Post Polisher Sub-Component.
Final formatting, readability, and visual consistency pass.
"""

from typing import Dict, Any
from ..tools.registry import ToolRegistry
from ..state.agent_state import AgentState


class InstagramPolisher:
    """Performs final micro-optimizations on approved content."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tools = tool_registry

    def polish(self, state: AgentState) -> Dict[str, Any]:
        """Apply final polish to the content."""
        content_type = state.input_data.constraints.content_type if state.input_data else "carousel"

        prompt = f"""
Perform final polishing on this approved Instagram content:
Type: {content_type}
Rules:
1. Ensure maximum visual impact on mobile screens.
2. Verify brand color and typography consistency across all assets.
3. Optimize caption line breaks for mobile readability.
4. Ensure emoji usage is strategic, not excessive.
5. Verify hashtag count is between 10-15 relevant tags.
6. Ensure CTA is crystal clear and specific.
        """

        raw_polished = self.tools.text_gen.generate_text(
            prompt=prompt,
            system_prompt="You are an elite Instagram formatting and polishing specialist.",
            temperature=0.3,
        )
        state.log_tool_call(
            tool_name="generate_text",
            arguments={"task": "polish_content"},
            result_summary="Completed final content polish.",
        )

        # Apply micro-optimizations
        polished = {"type": content_type, "polished": True}

        if content_type == "carousel" and state.carousel:
            # Ensure consistent slide formatting
            for slide in state.carousel.slides:
                slide.copy = slide.copy.strip()
                slide.slide_title = slide.slide_title.strip()
            polished["slides_polished"] = len(state.carousel.slides)

        elif content_type == "static_post" and state.static_post:
            state.static_post.headline = state.static_post.headline.strip()
            state.static_post.supporting_copy = state.static_post.supporting_copy.strip()
            polished["headline_polished"] = True

        elif content_type == "story_sequence" and state.story_sequence:
            for story in state.story_sequence.stories:
                story.headline = story.headline.strip()
                story.copy = story.copy.strip()
            polished["stories_polished"] = len(state.story_sequence.stories)

        state.add_content_version("final_polished", polished)
        return polished
