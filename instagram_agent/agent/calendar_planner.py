"""
Content Calendar Planner Sub-Component for Instagram Agent.
Generates multi-day content calendars with format distribution.
"""

from typing import Dict, Any, List
from ..schemas.input_contract import InstagramAgentInput
from ..schemas.strategy import InstagramStrategy
from ..schemas.output_contract import ContentCalendar, CalendarEntry
from ..tools.registry import ToolRegistry
from ..state.agent_state import AgentState


# Default weekly calendar templates
WEEKLY_TEMPLATES = {
    4: [  # 4 posts per week
        {"day": "Monday", "format": "carousel", "pillar": "Educational"},
        {"day": "Wednesday", "format": "static_post", "pillar": "Authority"},
        {"day": "Friday", "format": "story_sequence", "pillar": "Engagement"},
        {"day": "Saturday", "format": "carousel", "pillar": "Social Proof"},
    ],
    3: [  # 3 posts per week
        {"day": "Tuesday", "format": "carousel", "pillar": "Educational"},
        {"day": "Thursday", "format": "static_post", "pillar": "Authority"},
        {"day": "Saturday", "format": "story_sequence", "pillar": "Engagement"},
    ],
    5: [  # 5 posts per week
        {"day": "Monday", "format": "carousel", "pillar": "Educational"},
        {"day": "Tuesday", "format": "story_sequence", "pillar": "Engagement"},
        {"day": "Wednesday", "format": "static_post", "pillar": "Authority"},
        {"day": "Friday", "format": "carousel", "pillar": "Product/Service"},
        {"day": "Saturday", "format": "story_sequence", "pillar": "Social Proof"},
    ],
}


class CalendarPlanner:
    """Generates structured Instagram content calendars."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tools = tool_registry

    def create_calendar(self, state: AgentState) -> ContentCalendar:
        inp = state.input_data or InstagramAgentInput()
        strategy = state.strategy or InstagramStrategy()
        brand = inp.brand
        topic = inp.task.topic or f"{brand.industry or 'Industry'} insights"

        posts_per_week = inp.constraints.posts_per_week
        duration = inp.constraints.calendar_duration

        # Determine number of weeks
        weeks = {"1_week": 1, "2_weeks": 2, "1_month": 4}.get(duration, 1)
        total_posts = posts_per_week * weeks

        # LLM-assisted content ideation
        prompt = f"""
Generate {total_posts} Instagram content ideas for a {weeks}-week calendar:
Brand: {brand.brand_name}
Industry: {brand.industry}
Topic Focus: {topic}
Target Audience: {strategy.target_audience}
Content Pillars: {', '.join(strategy.content_pillars)}
Posts per week: {posts_per_week}
        """

        raw = self.tools.text_gen.generate_text(
            prompt=prompt,
            system_prompt="You are an expert Instagram content calendar planner.",
        )
        state.log_tool_call(
            tool_name="generate_text",
            arguments={"task": "create_calendar", "weeks": weeks},
            result_summary=f"Generated {total_posts} content ideas for calendar.",
        )

        # Build calendar entries
        template = WEEKLY_TEMPLATES.get(posts_per_week, WEEKLY_TEMPLATES[4])
        entries = []
        format_counts = {}

        day_dates = {
            "Monday": "Day 1", "Tuesday": "Day 2", "Wednesday": "Day 3",
            "Thursday": "Day 4", "Friday": "Day 5", "Saturday": "Day 6", "Sunday": "Day 7",
        }

        for week in range(weeks):
            for i, slot in enumerate(template):
                entry_num = week * len(template) + i + 1
                day = slot["day"]
                fmt = slot["format"]
                pillar = slot["pillar"]

                # Generate unique topic per slot
                topic_variants = [
                    f"{topic} Framework Breakdown",
                    f"The Truth About {topic}",
                    f"{topic} Quick Tips",
                    f"{topic} Case Study",
                    f"Common {topic} Mistakes",
                    f"{topic} vs Traditional Approaches",
                    f"Behind The Scenes: {topic}",
                    f"{topic} Results Showcase",
                ]
                slot_topic = topic_variants[entry_num % len(topic_variants)]

                # Hook variants per pillar
                hook_map = {
                    "Educational": f"90% of {strategy.target_audience or 'professionals'} get this wrong about {topic}",
                    "Authority": f"Unpopular opinion: {topic} is broken. Here's why.",
                    "Social Proof": f"How our client achieved 3x growth using {topic}",
                    "Product/Service": f"Introducing the easiest way to master {topic}",
                    "Engagement": f"Quick question: What's your biggest challenge with {topic}?",
                }

                cta_map = {
                    "Educational": f"Save this and DM '{brand.brand_name.upper().split()[0] if brand.brand_name else 'GUIDE'}' for the free guide",
                    "Authority": "Agree or disagree? Drop your take below 👇",
                    "Social Proof": "Want results like this? Link in bio ↗",
                    "Product/Service": "Tap the link to learn more →",
                    "Engagement": "Vote in the poll / Share your answer below",
                }

                entries.append(CalendarEntry(
                    date=f"Week {week + 1}, {day}",
                    day_of_week=day,
                    topic=slot_topic,
                    format=fmt,
                    content_pillar=pillar,
                    hook=hook_map.get(pillar, f"Discover the truth about {topic}"),
                    cta=cta_map.get(pillar, "Save this post for later"),
                    status="Draft",
                    objective=strategy.objective,
                    notes=f"Content pillar: {pillar} | Format: {fmt}",
                ))

                format_counts[fmt] = format_counts.get(fmt, 0) + 1

        calendar = ContentCalendar(
            duration=f"{weeks} Week{'s' if weeks > 1 else ''}",
            total_posts=len(entries),
            calendar_entries=entries,
            format_distribution=format_counts,
        )

        state.calendar = calendar
        state.add_content_version("calendar_v1", {"type": "content_calendar", "total": len(entries)})
        return calendar
