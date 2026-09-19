"""
Instagram Writer Sub-Component.
Generates content drafts for Carousels, Static Posts, and Story Sequences
with branded SVG graphics.
"""

from typing import Dict, Any, List, Optional
from ..schemas.strategy import InstagramStrategy, ContentIdea
from ..schemas.output_contract import (
    CarouselContent, CarouselSlide,
    StaticPostContent,
    StorySequenceContent, StoryFrame,
    HookVariant, CaptionDraft,
    CreativeAsset,
)
from ..tools.registry import ToolRegistry
from ..state.agent_state import AgentState
from ..creative.carousel_generator import generate_carousel_slide_svg
from ..creative.static_post_generator import generate_static_post_svg
from ..creative.story_generator import generate_story_frame_svg


class InstagramWriter:
    """Generates Instagram content drafts with copy, hooks, captions, and SVG graphics."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tools = tool_registry

    def write_carousel(self, state: AgentState, version_label: str = "carousel_v1") -> CarouselContent:
        """Generate a carousel with slide copy and branded SVG graphics."""
        strategy = state.strategy or InstagramStrategy()
        brand = state.input_data.brand if state.input_data else None
        brand_name = brand.brand_name if brand else "Brand"
        colors = brand.colors if brand else None
        topic = state.input_data.task.topic if state.input_data else "industry insights"
        max_slides = state.input_data.constraints.max_slides if state.input_data else 6

        # LLM prompt for carousel content
        prompt = f"""
Write a {max_slides}-slide Instagram carousel about: {topic}
Brand: {brand_name}
Target Audience: {strategy.target_audience}
Objective: {strategy.objective}
Tone: {strategy.tone_and_style}

For each slide provide:
- Slide title (5-8 words, bold)
- Slide copy (15-25 words, crisp)
- Visual direction

Structure: Hook → Problem → Step 1 → Step 2 → Step 3 → CTA
        """

        raw_text = self.tools.text_gen.generate_text(
            prompt=prompt,
            system_prompt="You are an expert Instagram carousel copywriter.",
            temperature=0.7,
        )
        state.log_tool_call(
            tool_name="generate_text",
            arguments={"task": "write_carousel", "version": version_label},
            result_summary=f"Generated carousel content for {version_label}.",
        )

        # Build slides
        slide_data = [
            {
                "title": f"Stop Doing This Wrong",
                "copy": f"90% of {strategy.target_audience or 'professionals'} waste time on outdated approaches. Here's what actually works.",
                "visual": "Bold hook with contrarian stat, gradient background",
            },
            {
                "title": "The Real Problem",
                "copy": f"Most {brand.industry or 'industry'} strategies fail because they focus on volume over value. Quality beats quantity.",
                "visual": "Problem illustration with red accent highlights",
            },
            {
                "title": "Step 1: Foundation",
                "copy": f"Start with a clear framework. Define your core pillars before creating any content.",
                "visual": "Clean step graphic with numbered badge",
            },
            {
                "title": "Step 2: Consistency",
                "copy": f"Build a repeatable system. Batch create, schedule ahead, and maintain visual consistency.",
                "visual": "System/process illustration with blue accents",
            },
            {
                "title": "Step 3: Optimize",
                "copy": f"Track what works. Double down on your top-performing formats and topics weekly.",
                "visual": "Growth chart with upward trend line",
            },
            {
                "title": "Get The Full Guide",
                "copy": f"DM us '{brand_name.upper().split()[0] if brand_name else 'GUIDE'}' for the free strategy blueprint. Save this post ↗",
                "visual": "CTA slide with branded button and link prompt",
            },
        ]

        slides = []
        for i, sd in enumerate(slide_data[:max_slides]):
            slide_type = "hook" if i == 0 else ("cta" if i == len(slide_data[:max_slides]) - 1 else "content")
            svg = generate_carousel_slide_svg(
                slide_number=i + 1,
                total_slides=min(max_slides, len(slide_data)),
                title=sd["title"],
                copy=sd["copy"],
                brand_name=brand_name,
                colors=colors,
                slide_type=slide_type,
            )
            slides.append(CarouselSlide(
                slide_number=i + 1,
                slide_title=sd["title"],
                copy=sd["copy"],
                visual_direction=sd["visual"],
                visual_element=sd["visual"],
                graphic_asset_url=f"https://assets.instagram.example.com/{brand_name.lower().replace(' ', '_')}/carousel/slide_{i+1}.svg",
                graphic_svg=svg,
            ))

        hook_text = slides[0].copy if slides else ""
        cta_text = slides[-1].copy if slides else ""

        carousel = CarouselContent(
            title=f"{topic} — Complete Framework",
            objective=strategy.objective,
            audience=strategy.target_audience,
            hook=hook_text,
            total_slides=len(slides),
            slides=slides,
            cta=cta_text,
            caption=self._generate_caption(strategy, topic, brand_name, "carousel"),
            brand_styling={
                "colors": colors or ["#0F172A", "#38BDF8", "#F43F5E"],
                "typography": {"heading": "Outfit", "body": "Inter"},
                "brand_name": brand_name,
            },
            design_instructions="1080×1080, dark theme, bold typography, brand color accents, progress dots",
        )

        state.carousel = carousel
        state.add_content_version(version_label, {"type": "carousel", "title": carousel.title})
        return carousel

    def write_static_post(self, state: AgentState, version_label: str = "static_v1") -> StaticPostContent:
        """Generate a static post with copy and branded SVG graphic."""
        strategy = state.strategy or InstagramStrategy()
        brand = state.input_data.brand if state.input_data else None
        brand_name = brand.brand_name if brand else "Brand"
        colors = brand.colors if brand else None
        topic = state.input_data.task.topic if state.input_data else "industry insights"

        prompt = f"""
Write a bold Instagram static post about: {topic}
Brand: {brand_name}
Target Audience: {strategy.target_audience}
Tone: {strategy.tone_and_style}
        """

        raw_text = self.tools.text_gen.generate_text(
            prompt=prompt,
            system_prompt="You are an expert Instagram single-post copywriter.",
        )
        state.log_tool_call(
            tool_name="generate_text",
            arguments={"task": "write_static_post", "version": version_label},
            result_summary=f"Generated static post for {version_label}.",
        )

        headline = f"The {topic.title()} Framework That Changes Everything"
        supporting = f"Most {strategy.target_audience or 'professionals'} overcomplicate this. Here's the simple truth that top performers already know."
        cta = "Agree? Double tap and share with someone who needs this ↗"

        svg = generate_static_post_svg(
            headline=headline,
            supporting_copy=supporting,
            cta="Learn More →",
            brand_name=brand_name,
            category="Authority",
            colors=colors,
        )

        static = StaticPostContent(
            concept=f"Bold authority statement about {topic}",
            category="Authority",
            headline=headline,
            supporting_copy=supporting,
            cta=cta,
            caption=self._generate_caption(strategy, topic, brand_name, "static_post"),
            visual_direction="Bold single graphic with headline and CTA",
            graphic_asset_url=f"https://assets.instagram.example.com/{brand_name.lower().replace(' ', '_')}/static_post.svg",
            graphic_svg=svg,
        )

        state.static_post = static
        state.add_content_version(version_label, {"type": "static_post", "headline": headline})
        return static

    def write_story_sequence(self, state: AgentState, version_label: str = "story_v1") -> StorySequenceContent:
        """Generate a story sequence with copy, interactive elements, and branded SVG graphics."""
        strategy = state.strategy or InstagramStrategy()
        brand = state.input_data.brand if state.input_data else None
        brand_name = brand.brand_name if brand else "Brand"
        colors = brand.colors if brand else None
        topic = state.input_data.task.topic if state.input_data else "industry insights"
        max_stories = state.input_data.constraints.max_stories if state.input_data else 4

        prompt = f"""
Write a {max_stories}-part Instagram Story Sequence about: {topic}
Brand: {brand_name}
Target Audience: {strategy.target_audience}
Include: 1 poll sticker, 1 CTA with link sticker
        """

        raw_text = self.tools.text_gen.generate_text(
            prompt=prompt,
            system_prompt="You are an expert Instagram Story sequence creator.",
        )
        state.log_tool_call(
            tool_name="generate_text",
            arguments={"task": "write_story_sequence", "version": version_label},
            result_summary=f"Generated story sequence for {version_label}.",
        )

        story_data = [
            {
                "headline": f"Did You Know This About {topic.title()}?",
                "copy": f"Most {strategy.target_audience or 'people'} miss this completely...",
                "story_type": "educational",
                "interactive_element": "",
            },
            {
                "headline": "Here's The Key Insight",
                "copy": "The top performers focus on systems, not just tactics.",
                "story_type": "educational",
                "interactive_element": "",
            },
            {
                "headline": "Quick Poll",
                "copy": "Which matters more for growth?",
                "story_type": "engagement",
                "interactive_element": "poll_sticker",
            },
            {
                "headline": "Get The Full Guide",
                "copy": f"Tap below to grab our free {topic} blueprint",
                "story_type": "cta",
                "interactive_element": "link_sticker",
            },
        ]

        stories = []
        for i, sd in enumerate(story_data[:max_stories]):
            svg = generate_story_frame_svg(
                story_number=i + 1,
                total_stories=min(max_stories, len(story_data)),
                headline=sd["headline"],
                copy=sd["copy"],
                story_type=sd["story_type"],
                interactive_element=sd["interactive_element"],
                brand_name=brand_name,
                colors=colors,
            )
            stories.append(StoryFrame(
                story_number=i + 1,
                story_type=sd["story_type"],
                headline=sd["headline"],
                copy=sd["copy"],
                visual_direction=f"Branded {sd['story_type']} story with {sd.get('interactive_element', 'no')} sticker",
                interactive_element=sd["interactive_element"],
                graphic_asset_url=f"https://assets.instagram.example.com/{brand_name.lower().replace(' ', '_')}/story/frame_{i+1}.svg",
                graphic_svg=svg,
            ))

        sequence = StorySequenceContent(
            sequence_title=f"{topic} — Quick Guide",
            objective=strategy.objective,
            total_stories=len(stories),
            stories=stories,
            cta="Tap the link sticker on the final story",
        )

        state.story_sequence = sequence
        state.add_content_version(version_label, {"type": "story_sequence", "title": sequence.sequence_title})
        return sequence

    def generate_hooks(self, state: AgentState) -> List[HookVariant]:
        """Generate multiple hook variants for the content."""
        topic = state.input_data.task.topic if state.input_data else "topic"
        audience = state.strategy.target_audience if state.strategy else "audience"

        return [
            HookVariant(
                style="Curiosity",
                hook_text=f"What top 1% {audience} know about {topic} (that nobody talks about)",
                rationale="Curiosity gap + exclusivity drives saves and shares",
                angle="Mystery / insider knowledge",
            ),
            HookVariant(
                style="Contrarian",
                hook_text=f"Stop following {topic} advice from people who've never done it",
                rationale="Pattern interrupt challenges conventional wisdom",
                angle="Bold contrarian statement",
            ),
            HookVariant(
                style="Metric",
                hook_text=f"We tested {topic} for 90 days. Here are the real numbers.",
                rationale="Specific data and timeframes build credibility",
                angle="Data-backed proof",
            ),
        ]

    def generate_captions(self, state: AgentState, format_type: str = "carousel") -> List[CaptionDraft]:
        """Generate caption drafts for the content."""
        return [CaptionDraft(
            version="v1",
            caption_text=self._generate_caption(
                state.strategy or InstagramStrategy(),
                state.input_data.task.topic if state.input_data else "topic",
                state.input_data.brand.brand_name if state.input_data else "Brand",
                format_type,
            ),
            hashtags=self._generate_hashtags(state),
        )]

    def _generate_caption(self, strategy: InstagramStrategy, topic: str, brand_name: str, format_type: str) -> str:
        """Generate a caption for the given format."""
        hook = f"90% of {strategy.target_audience or 'professionals'} get {topic} completely wrong."
        body = (
            f"\n\nHere's what actually works:\n\n"
            f"We've spent months analyzing what top performers do differently.\n\n"
            f"The answer? They focus on frameworks, not tactics.\n\n"
            f"Swipe through to see the exact 3-step approach ➡️\n\n"
            if format_type == "carousel" else
            f"\n\nMost people overcomplicate {topic}.\n\n"
            f"The truth is simpler than you think.\n\n"
            f"The top performers share one thing in common: they build repeatable systems.\n\n"
        )
        cta = (
            f"💡 Save this post for later\n"
            f"🔁 Share with someone who needs this\n"
            f"💬 DM us '{brand_name.upper().split()[0] if brand_name else 'GUIDE'}' for the free guide"
        )
        hashtags = " ".join(self._generate_hashtags_list(strategy, topic, brand_name))
        return f"{hook}{body}{cta}\n\n.\n.\n.\n{hashtags}"

    def _generate_hashtags(self, state: AgentState) -> List[str]:
        topic = state.input_data.task.topic if state.input_data else "business"
        brand_name = state.input_data.brand.brand_name if state.input_data else "brand"
        strategy = state.strategy or InstagramStrategy()
        return self._generate_hashtags_list(strategy, topic, brand_name)

    def _generate_hashtags_list(self, strategy: InstagramStrategy, topic: str, brand_name: str) -> List[str]:
        base_tags = [
            f"#{brand_name.replace(' ', '')}" if brand_name else "#Brand",
            f"#{topic.replace(' ', '')}" if topic else "#Content",
        ]
        industry_tags = [
            "#ContentStrategy", "#SocialMediaMarketing", "#InstagramGrowth",
            "#DigitalMarketing", "#ContentCreation",
        ]
        niche_tags = [
            "#BusinessTips", "#MarketingStrategy", "#GrowthHacking",
            "#Entrepreneurship", "#LeadershipDevelopment",
        ]
        return base_tags + industry_tags[:5] + niche_tags[:5]
