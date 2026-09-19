"""
Story SVG Generator for Instagram Agent.
Generates branded 1080×1920 (9:16) story frame graphics.
"""

from typing import Dict, Any, List, Optional
import html


def _escape(text: str) -> str:
    return html.escape(str(text), quote=True)


def _wrap_text(text: str, max_chars: int = 28) -> List[str]:
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def generate_story_frame_svg(
    story_number: int,
    total_stories: int,
    headline: str,
    copy: str = "",
    story_type: str = "educational",
    interactive_element: str = "",
    brand_name: str = "Brand",
    colors: Optional[List[str]] = None,
) -> str:
    """Generate a single 1080×1920 story frame as SVG."""

    c = colors or ["#0F172A", "#38BDF8", "#F43F5E"]
    bg = c[0] if len(c) > 0 else "#0F172A"
    accent = c[1] if len(c) > 1 else "#38BDF8"
    highlight = c[2] if len(c) > 2 else "#F43F5E"

    # Progress bar segments
    progress_bars = ""
    segment_width = (1080 - 40 - (total_stories - 1) * 6) / total_stories
    for i in range(total_stories):
        x = 20 + i * (segment_width + 6)
        fill = "white" if i < story_number else "rgba(255,255,255,0.3)"
        progress_bars += f'<rect x="{x:.0f}" y="30" width="{segment_width:.0f}" height="3" rx="1.5" fill="{fill}"/>'

    # Headline
    headline_lines = _wrap_text(headline, 22)
    headline_tspans = ""
    for i, line in enumerate(headline_lines[:3]):
        dy = 0 if i == 0 else 72
        headline_tspans += f'<tspan x="540" dy="{dy}">{_escape(line)}</tspan>'

    # Copy
    copy_lines = _wrap_text(copy, 36)
    copy_tspans = ""
    for i, line in enumerate(copy_lines[:4]):
        dy = 0 if i == 0 else 40
        copy_tspans += f'<tspan x="540" dy="{dy}">{_escape(line)}</tspan>'

    # Interactive element mock
    interactive_svg = ""
    if interactive_element == "poll_sticker":
        interactive_svg = f"""
    <rect x="200" y="1350" width="680" height="180" rx="20" fill="white" opacity="0.15"/>
    <text x="540" y="1400" font-family="Inter, Arial, sans-serif" font-size="22"
          fill="white" font-weight="700" text-anchor="middle">What do you think?</text>
    <rect x="240" y="1420" width="280" height="50" rx="25" fill="{accent}" opacity="0.8"/>
    <text x="380" y="1452" font-family="Inter, sans-serif" font-size="18" fill="white"
          text-anchor="middle" font-weight="600">Option A</text>
    <rect x="560" y="1420" width="280" height="50" rx="25" fill="{highlight}" opacity="0.8"/>
    <text x="700" y="1452" font-family="Inter, sans-serif" font-size="18" fill="white"
          text-anchor="middle" font-weight="600">Option B</text>
        """
    elif interactive_element == "question_sticker":
        interactive_svg = f"""
    <rect x="200" y="1350" width="680" height="120" rx="20" fill="white" opacity="0.15"/>
    <text x="540" y="1400" font-family="Inter, Arial, sans-serif" font-size="20"
          fill="white" font-weight="600" text-anchor="middle">Ask me anything...</text>
    <rect x="240" y="1420" width="600" height="40" rx="10" fill="white" opacity="0.1"/>
        """
    elif interactive_element == "link_sticker":
        interactive_svg = f"""
    <rect x="340" y="1400" width="400" height="56" rx="28" fill="{accent}"/>
    <text x="540" y="1435" font-family="Inter, Arial, sans-serif" font-size="18"
          fill="white" font-weight="700" text-anchor="middle">🔗 Tap to Learn More</text>
        """

    # Background gradient varies by story type
    if story_type == "cta":
        grad = f'<stop offset="0%" stop-color="{accent}44"/><stop offset="100%" stop-color="{bg}"/>'
    elif story_type == "promotional":
        grad = f'<stop offset="0%" stop-color="{highlight}33"/><stop offset="100%" stop-color="{bg}"/>'
    else:
        grad = f'<stop offset="0%" stop-color="{bg}"/><stop offset="100%" stop-color="{bg}ee"/>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <linearGradient id="story_bg_{story_number}" x1="0" y1="0" x2="0" y2="1">
      {grad}
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1920" fill="url(#story_bg_{story_number})"/>

  <!-- Progress bar -->
  {progress_bars}

  <!-- Brand name top -->
  <text x="540" y="90" font-family="Outfit, Arial, sans-serif" font-size="18"
        fill="white" opacity="0.7" font-weight="600" text-anchor="middle" letter-spacing="2">
    {_escape(brand_name)}
  </text>

  <!-- Headline -->
  <text x="540" y="700" font-family="Outfit, Arial, sans-serif" font-size="58"
        fill="white" font-weight="800" text-anchor="middle">
    {headline_tspans}
  </text>

  <!-- Copy -->
  <text x="540" y="950" font-family="Inter, Arial, sans-serif" font-size="26"
        fill="white" opacity="0.8" text-anchor="middle">
    {copy_tspans}
  </text>

  <!-- Interactive element -->
  {interactive_svg}

  <!-- Swipe up indicator -->
  <text x="540" y="1830" font-family="Inter, Arial, sans-serif" font-size="14"
        fill="white" opacity="0.4" text-anchor="middle" letter-spacing="2">
    SWIPE UP
  </text>
  <line x1="530" y1="1840" x2="540" y2="1850" stroke="white" stroke-opacity="0.4" stroke-width="2"/>
  <line x1="540" y1="1850" x2="550" y2="1840" stroke="white" stroke-opacity="0.4" stroke-width="2"/>
</svg>"""

    return svg


def generate_story_sequence_svgs(
    stories_data: List[Dict[str, str]],
    brand_name: str = "Brand",
    colors: Optional[List[str]] = None,
) -> List[str]:
    """Generate SVGs for all story frames in a sequence."""
    total = len(stories_data)
    svgs = []
    for i, story in enumerate(stories_data):
        svg = generate_story_frame_svg(
            story_number=i + 1,
            total_stories=total,
            headline=story.get("headline", ""),
            copy=story.get("copy", ""),
            story_type=story.get("story_type", "educational"),
            interactive_element=story.get("interactive_element", ""),
            brand_name=brand_name,
            colors=colors,
        )
        svgs.append(svg)
    return svgs
