"""
Instagram Platform Standards, Formatting Rules, and Best Practices.
Used by Strategy, Writer, Critic, and Creative sub-components.
"""

from typing import Dict, Any, List


INSTAGRAM_FORMAT_GUIDELINES: Dict[str, Any] = {
    "max_caption_length": 2200,
    "recommended_caption_length": {
        "short": 100,
        "medium": 300,
        "long": 800,
    },
    "max_hashtags": 30,
    "recommended_hashtags": 15,
    "content_types": {
        "carousel": {
            "max_slides": 20,
            "recommended_slides": 5,
            "dimensions": "1080x1080",
            "aspect_ratio": "1:1",
            "alt_aspect_ratios": ["4:5 (1080x1350)", "16:9 (1080x608)"],
            "requires_graphic": True,
            "engagement_notes": "Highest saves and shares. Best for educational/list content.",
        },
        "static_post": {
            "dimensions": "1080x1080",
            "aspect_ratio": "1:1",
            "alt_aspect_ratios": ["4:5 (1080x1350)"],
            "requires_graphic": True,
            "engagement_notes": "Good for bold statements, quotes, infographics.",
        },
        "story": {
            "dimensions": "1080x1920",
            "aspect_ratio": "9:16",
            "max_sequence": 10,
            "recommended_sequence": 4,
            "requires_graphic": True,
            "interactive_elements": [
                "poll_sticker", "question_sticker", "quiz_sticker",
                "link_sticker", "countdown_sticker", "emoji_slider",
            ],
            "engagement_notes": "Best for quick engagement, polls, and behind-the-scenes. Interactive elements increase completion rate by 40%.",
        },
        "reel": {
            "dimensions": "1080x1920",
            "aspect_ratio": "9:16",
            "max_duration_seconds": 90,
            "status": "COMING_SOON",
            "engagement_notes": "Highest reach potential. Algorithm-favoured format.",
        },
    },
    "formatting_rules": [
        "Use a high-impact hook in Slide 1 / first line (before fold).",
        "Keep carousel slide copy to 20-30 words max per slide for readability.",
        "Use bold typography hierarchy: Headline → Subhead → Body → CTA.",
        "Include brand colors and logo on every carousel slide for consistency.",
        "Use single-column layouts for mobile-first readability.",
        "Place a clear CTA on the final slide (carousel) or end of caption.",
        "Caption: Start with the hook, break into short paragraphs, end with CTA.",
        "Hashtags: Mix 5 broad + 5 niche + 5 branded for optimal discovery.",
        "Use line breaks and emojis strategically to improve caption scannability.",
        "Stories: Use interactive stickers on at least 1 in every 3 stories.",
    ],
    "hook_archetypes": [
        "Pattern Interrupt (Contrarian Statement)",
        "Bold Metric / Statistic",
        "Myth vs. Reality",
        "Step-by-Step Framework Teaser",
        "Before vs. After",
        "Direct Question / Problem Statement",
        "Social Proof / Testimonial",
    ],
    "content_pillar_templates": [
        "Educational (how-to, frameworks, tips)",
        "Authority (industry insights, thought leadership)",
        "Social Proof (testimonials, case studies, results)",
        "Product/Service (features, demos, offers)",
        "Engagement (polls, questions, memes, trends)",
    ],
    "carousel_structure_templates": {
        "educational_framework": [
            "Slide 1: Hook (Bold statement + visual pattern interrupt)",
            "Slide 2: Problem / Context",
            "Slide 3: Step 1 / Insight 1",
            "Slide 4: Step 2 / Insight 2",
            "Slide 5: Step 3 / Insight 3",
            "Slide 6: CTA (Save, Share, DM, Link in Bio)",
        ],
        "myth_busting": [
            "Slide 1: Hook (Common Myth statement)",
            "Slide 2: Why people believe the myth",
            "Slide 3: The reality / data",
            "Slide 4: What to do instead",
            "Slide 5: CTA",
        ],
        "listicle": [
            "Slide 1: Hook (X Things You Need to Know)",
            "Slide 2-5: One item per slide",
            "Slide 6: CTA",
        ],
    },
    "story_sequence_templates": {
        "educational_walkthrough": [
            "Story 1: Hook (text overlay on branded background)",
            "Story 2: Key insight or tip",
            "Story 3: Poll or question sticker for engagement",
            "Story 4: CTA with link sticker",
        ],
        "product_spotlight": [
            "Story 1: Teaser / Problem statement",
            "Story 2: Solution intro",
            "Story 3: Feature highlight",
            "Story 4: Social proof / testimonial",
            "Story 5: CTA / offer",
        ],
    },
}


def get_platform_checklist() -> List[str]:
    """Return Instagram formatting rules as a checklist for the critic."""
    return INSTAGRAM_FORMAT_GUIDELINES["formatting_rules"]


def get_carousel_template(template_name: str = "educational_framework") -> List[str]:
    """Return a carousel structure template by name."""
    templates = INSTAGRAM_FORMAT_GUIDELINES["carousel_structure_templates"]
    return templates.get(template_name, templates["educational_framework"])


def get_story_template(template_name: str = "educational_walkthrough") -> List[str]:
    """Return a story sequence template by name."""
    templates = INSTAGRAM_FORMAT_GUIDELINES["story_sequence_templates"]
    return templates.get(template_name, templates["educational_walkthrough"])


def get_content_type_spec(content_type: str) -> Dict[str, Any]:
    """Return specifications for a given content type."""
    return INSTAGRAM_FORMAT_GUIDELINES["content_types"].get(content_type, {})
