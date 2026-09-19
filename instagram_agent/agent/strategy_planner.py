"""
Strategy Planner Sub-Component for Instagram Agent.
Translates brand context and research into a structured Instagram Content Strategy.
"""

from ..schemas.input_contract import InstagramAgentInput
from ..schemas.strategy import InstagramStrategy, ContentIdea
from ..schemas.research import ResearchSummary
from ..tools.registry import ToolRegistry
from ..state.agent_state import AgentState


class StrategyPlanner:
    """Develops a structured content strategy for Instagram."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tools = tool_registry

    def create_strategy(self, state: AgentState) -> InstagramStrategy:
        inp = state.input_data or InstagramAgentInput()
        research = state.research_summary or ResearchSummary()
        brand = inp.brand

        # Ask LLM to synthesize strategy
        prompt = f"""
Synthesize an Instagram Content Strategy for:
Brand: {brand.brand_name} ({research.brand.positioning})
Industry: {brand.industry}
Objective: {inp.task.objective}
Topic: {inp.task.topic}
Target Audience: {brand.target_audience or research.brand.target_audience}
Target Format: {inp.task.target_format}
Content Pillars: {', '.join(brand.content_pillars or ['Educational', 'Authority', 'Social Proof'])}
Brand Voice: {brand.brand_voice or research.brand.tone_of_voice}
        """

        raw = self.tools.text_gen.generate_text(
            prompt=prompt,
            system_prompt="You are an expert Instagram Content Strategist for B2B and D2C brands.",
        )
        state.log_tool_call(
            tool_name="generate_text",
            arguments={"task": "create_strategy"},
            result_summary="Generated Instagram content strategy.",
        )

        # Build content pillars
        pillars = brand.content_pillars or [
            "Educational", "Authority", "Social Proof", "Product/Service", "Engagement"
        ]

        # Generate content ideas
        ideas = []
        topic = inp.task.topic or f"{brand.industry or 'Industry'} best practices"

        if inp.task.target_format in ("carousel", "content_calendar"):
            ideas.append(ContentIdea(
                title=f"The Framework for {topic}",
                format="carousel",
                content_pillar="Educational",
                objective=inp.task.objective,
                hook=f"90% of {brand.target_audience or 'leaders'} get this wrong.",
                core_idea=f"Step-by-step breakdown of {topic}",
                cta="Save this post and DM us 'GUIDE' for the free resource.",
                visual_direction="Bold slide 1 hook, clean steps, branded CTA slide",
                caption_direction="Expand on the framework, add personal insight, hashtags",
            ))

        if inp.task.target_format in ("static_post", "content_calendar"):
            ideas.append(ContentIdea(
                title=f"The Truth About {topic}",
                format="static_post",
                content_pillar="Authority",
                objective=inp.task.objective,
                hook=f"Unpopular opinion about {topic}",
                core_idea="Bold contrarian statement with supporting data",
                cta="Agree or disagree? Drop your take below 👇",
                visual_direction="Single bold graphic with headline and stat",
                caption_direction="Expand on the contrarian take, invite discussion",
            ))

        if inp.task.target_format in ("story_sequence", "content_calendar"):
            ideas.append(ContentIdea(
                title=f"Quick Guide: {topic}",
                format="story_sequence",
                content_pillar="Educational",
                objective=inp.task.objective,
                hook="Swipe through for the fastest way to...",
                core_idea="4-part interactive walkthrough",
                cta="Tap the link to get the full guide",
                visual_direction="Progressive story with poll and CTA stickers",
                caption_direction="N/A (stories don't have external captions)",
            ))

        strategy = InstagramStrategy(
            brand_name=brand.brand_name,
            objective=inp.task.objective,
            content_pillars=pillars,
            format_mix_percentage={
                "carousel": 50, "static_post": 20, "story_sequence": 30
            },
            content_ideas=ideas,
            strategic_recommendations=[
                "Lead with educational carousels — highest saves and shares on IG.",
                "Use interactive story stickers (polls, questions) at least 2x per week.",
                "Maintain visual consistency with brand colors across all formats.",
                f"Post 3-4 times per week for optimal algorithm performance.",
                f"Use a mix of {len(pillars)} content pillars to avoid content fatigue.",
            ],
            target_audience=brand.target_audience or research.brand.target_audience,
            content_angle=f"Framework-driven educational content about {topic}",
            tone_and_style=brand.brand_voice or research.brand.tone_of_voice,
            posting_frequency=f"{inp.constraints.posts_per_week} posts per week",
            best_posting_times=["Tuesday 9AM", "Thursday 12PM", "Saturday 10AM"],
        )

        state.strategy = strategy
        return strategy
