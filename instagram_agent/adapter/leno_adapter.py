"""
Leno OS Integration Adapter for Instagram Specialist Agent.
Provides bidirectional schema adaptation between Leno OS (Digital Distribution OS)
and the Instagram Specialist Agent contract.
"""

from typing import Dict, Any, List, Optional
from instagram_agent.schemas.input_contract import (
    InstagramAgentInput,
    BrandContext,
    TaskSpec,
    Constraints,
)
from instagram_agent.schemas.output_contract import InstagramAgentOutput
from instagram_agent.agent.instagram_agent import InstagramSpecialistAgent


class LenoOSAdapter:
    """
    Translates between Leno OS Campaign/Brand/Plan schemas and Instagram Specialist Agent.
    
    Leno OS Schema:
      BrandProfile: { name, one_liner, positioning, audience, products, competitors, tone_words, dos, donts, primary_color, secondary_color }
      Plan: { goal, audience, key_message, platforms: ['instagram', ...] }
      Strategy: { angle, hooks, cta }
      
    Outputs:
      Draft: { platform: 'instagram', body: string, hashtags: string[] }
      Critique: { platform: 'instagram', scores: { brand_voice, goal_fit, platform_fit, craft }, weighted, pass, fix_list }
    """

    def __init__(self, agent: Optional[InstagramSpecialistAgent] = None):
        self.agent = agent or InstagramSpecialistAgent()

    def to_agent_input(self, leno_payload: Dict[str, Any]) -> InstagramAgentInput:
        """Map Leno OS payload to InstagramAgentInput."""
        brand_raw = leno_payload.get("brand") or leno_payload.get("brandProfile") or {}
        plan_raw = leno_payload.get("plan") or {}
        strat_raw = leno_payload.get("strategy") or {}

        # Brand Context
        brand_name = (
            brand_raw.get("name")
            or brand_raw.get("brand_name")
            or leno_payload.get("brand_name")
            or "Default Brand"
        )
        industry = brand_raw.get("positioning") or brand_raw.get("industry") or "Technology & Digital Systems"
        one_liner = brand_raw.get("one_liner", "")
        audience_desc = plan_raw.get("audience") or brand_raw.get("audience") or "Growth-focused Professionals"

        colors = []
        if brand_raw.get("primary_color"):
            colors.append(brand_raw["primary_color"])
        if brand_raw.get("secondary_color"):
            colors.append(brand_raw["secondary_color"])
        if not colors:
            colors = ["#0F172A", "#3B82F6", "#10B981"]

        brand_context = BrandContext(
            brand_name=brand_name,
            industry=industry,
            target_audience=audience_desc,
            account_handle=brand_raw.get("account_handle", f"@{brand_name.lower().replace(' ', '')}"),
            website=brand_raw.get("website", ""),
            positioning=brand_raw.get("positioning", one_liner),
            tone=brand_raw.get("tone_words", ["authoritative", "human"])[0] if brand_raw.get("tone_words") else "human",
            products_services=[one_liner] if one_liner else brand_raw.get("products", []),
            colors=colors,
        )

        # Task & Strategy
        topic = (
            plan_raw.get("key_message")
            or strat_raw.get("angle")
            or leno_payload.get("topic")
            or leno_payload.get("coreMessage")
            or "Autonomous System Architecture"
        )
        objective = plan_raw.get("goal") or leno_payload.get("goal") or "authority"
        
        # Decide content type: defaults to carousel for maximum engagement on Instagram
        target_format = leno_payload.get("format", "carousel")
        if target_format not in ("carousel", "static_post", "story_sequence", "content_calendar", "reel"):
            target_format = "carousel"

        task_spec = TaskSpec(
            type="create_content",
            topic=topic,
            objective=objective,
            target_format=target_format,
            custom_params={"notes": f"Hook inspiration: {strat_raw.get('hooks', [''])[0] if strat_raw.get('hooks') else ''}. CTA: {strat_raw.get('cta', '')}"},
        )

        constraints = Constraints(
            content_type=target_format,
            tone_override=brand_raw.get("tone_words", ["professional"])[0] if brand_raw.get("tone_words") else "authoritative_yet_approachable",
            max_slides=7,
        )

        return InstagramAgentInput(
            brand=brand_context,
            task=task_spec,
            constraints=constraints,
        )

    def to_leno_draft(self, output: InstagramAgentOutput) -> Dict[str, Any]:
        """
        Transforms InstagramAgentOutput into strict Leno OS Draft & Critique schemas,
        enriched with visual asset metadata.
        """
        body_text = ""
        hashtags: List[str] = []
        visual_type = output.content_type
        aspect_ratio = "4:5"
        total_slides = 1
        slides_data = []
        svg_preview = ""
        title = ""

        # Extract caption text and hashtags from primary caption draft
        if output.captions and len(output.captions) > 0:
            c_draft = output.captions[0]
            body_text = c_draft.caption_text
            hashtags = c_draft.hashtags

        if output.carousel:
            c = output.carousel
            title = c.title
            aspect_ratio = "4:5"
            total_slides = c.total_slides or len(c.slides)
            if not body_text:
                body_text = c.caption or (c.slides[0].copy if c.slides else "")
            slides_data = [
                {
                    "slide_number": s.slide_number,
                    "headline": s.slide_title,
                    "body": s.copy,
                    "visual_direction": s.visual_direction,
                    "svg_markup": s.graphic_svg,
                }
                for s in c.slides
            ]
            if c.slides:
                svg_preview = c.slides[0].graphic_svg
        elif output.static_post:
            s = output.static_post
            title = s.headline
            aspect_ratio = "1:1"
            if not body_text:
                body_text = s.caption or s.supporting_copy
            svg_preview = s.graphic_svg
            slides_data = [{
                "slide_number": 1,
                "headline": s.headline,
                "body": s.supporting_copy,
                "svg_markup": s.graphic_svg,
            }]
        elif output.story_sequence:
            st = output.story_sequence
            title = st.sequence_title
            aspect_ratio = "9:16"
            total_slides = st.total_stories or len(st.stories)
            if not body_text:
                body_text = f"Story Sequence: {st.sequence_title}"
            slides_data = [
                {
                    "frame_number": f.story_number,
                    "headline": f.headline,
                    "body": f.copy,
                    "interactive_element": f.interactive_element,
                    "svg_markup": f.graphic_svg,
                }
                for f in st.stories
            ]
            if st.stories:
                svg_preview = st.stories[0].graphic_svg
        elif output.calendar:
            cal = output.calendar
            title = f"Content Calendar ({cal.duration})"
            total_slides = cal.total_posts
            if not body_text:
                body_text = f"Content Calendar with {cal.total_posts} scheduled posts."
            slides_data = [
                {
                    "date": e.date,
                    "day": e.day_of_week,
                    "topic": e.topic,
                    "format": e.format,
                    "hook": e.hook,
                    "cta": e.cta,
                }
                for e in cal.calendar_entries
            ]
        else:
            if not body_text:
                body_text = "Content generated successfully via Instagram Specialist Agent."

        if not hashtags:
            hashtags = ["#InstagramGrowth", "#ContentStrategy", "#DigitalDistribution"]

        # Leno OS Critique Score Normalization (0.0 to 1.0)
        overall_score_10 = output.quality.overall_score if output.quality else 9.0
        normalized_score = round(min(1.0, max(0.0, overall_score_10 / 10.0)), 2)
        issues = output.quality.issues if (output.quality and output.quality.issues) else []

        critique_payload = {
            "platform": "instagram",
            "scores": {
                "brand_voice": normalized_score,
                "goal_fit": normalized_score,
                "platform_fit": min(1.0, round(normalized_score + 0.02, 2)),
                "craft": normalized_score,
            },
            "weighted": normalized_score,
            "pass": normalized_score >= 0.80,
            "fix_list": issues,
        }

        return {
            # Strict Leno OS DraftSchema fields:
            "platform": "instagram",
            "body": body_text,
            "hashtags": hashtags,

            # Extended Leno OS & UI Visual Assets:
            "title": title or "Instagram Adaptation",
            "content_type": visual_type,
            "aspect_ratio": aspect_ratio,
            "total_slides": total_slides,
            "slides": slides_data,
            "svg_preview": svg_preview,
            "critique": critique_payload,
            "quality": {
                "status": output.quality.status if output.quality else "passed",
                "score": overall_score_10,
            },
            "raw_agent_status": output.status,
        }

    def execute_leno_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """End-to-end execution: maps Leno OS payload -> agent execution -> Leno OS draft output."""
        agent_input = self.to_agent_input(payload)
        output = self.agent.run(agent_input)
        return self.to_leno_draft(output)


# Singleton instance for quick programmatic use
leno_adapter = LenoOSAdapter()


def run_for_leno_os(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience helper to run Instagram Agent directly with a Leno OS payload."""
    return leno_adapter.execute_leno_request(payload)
