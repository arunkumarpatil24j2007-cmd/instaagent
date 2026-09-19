"""
Static Post SVG Generator for Instagram Agent.
Generates branded 1080×1080 static post graphics.
"""

from typing import Dict, Any, List, Optional
import html


def _escape(text: str) -> str:
    return html.escape(str(text), quote=True)


def _wrap_text(text: str, max_chars: int = 30) -> List[str]:
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


def generate_static_post_svg(
    headline: str,
    supporting_copy: str = "",
    cta: str = "",
    brand_name: str = "Brand",
    category: str = "Educational",
    colors: Optional[List[str]] = None,
) -> str:
    """Generate a single 1080×1080 static post as SVG."""

    c = colors or ["#0F172A", "#38BDF8", "#F43F5E"]
    bg = c[0] if len(c) > 0 else "#0F172A"
    accent = c[1] if len(c) > 1 else "#38BDF8"
    highlight = c[2] if len(c) > 2 else "#F43F5E"

    # Headline wrapped
    headline_lines = _wrap_text(headline, 25)
    headline_tspans = ""
    for i, line in enumerate(headline_lines[:3]):
        dy = 0 if i == 0 else 64
        headline_tspans += f'<tspan x="540" dy="{dy}">{_escape(line)}</tspan>'

    # Supporting copy
    copy_lines = _wrap_text(supporting_copy, 42)
    copy_tspans = ""
    for i, line in enumerate(copy_lines[:4]):
        dy = 0 if i == 0 else 38
        copy_tspans += f'<tspan x="540" dy="{dy}">{_escape(line)}</tspan>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <linearGradient id="static_bg" x1="0" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="50%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{highlight}15"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1080" fill="url(#static_bg)" rx="0"/>

  <!-- Category badge -->
  <rect x="420" y="200" width="{len(category) * 14 + 40}" height="36" rx="18"
        fill="{accent}22" stroke="{accent}44" stroke-width="1"/>
  <text x="{420 + (len(category) * 7 + 20)}" y="224" font-family="Inter, Arial, sans-serif"
        font-size="14" fill="{accent}" font-weight="600" text-anchor="middle"
        letter-spacing="1.5">{_escape(category.upper())}</text>

  <!-- Decorative accent -->
  <rect x="490" y="290" width="100" height="4" rx="2" fill="{accent}"/>

  <!-- Headline -->
  <text x="540" y="400" font-family="Outfit, Arial, sans-serif" font-size="54"
        fill="white" font-weight="800" text-anchor="middle">
    {headline_tspans}
  </text>

  <!-- Supporting copy -->
  <text x="540" y="620" font-family="Inter, Arial, sans-serif" font-size="24"
        fill="white" opacity="0.75" text-anchor="middle">
    {copy_tspans}
  </text>

  <!-- CTA -->
  <rect x="340" y="830" width="400" height="56" rx="28"
        fill="{accent}" opacity="0.9"/>
  <text x="540" y="865" font-family="Inter, Arial, sans-serif" font-size="20"
        fill="white" font-weight="700" text-anchor="middle">
    {_escape(cta or "Learn More →")}
  </text>

  <!-- Brand -->
  <text x="540" y="980" font-family="Outfit, Arial, sans-serif" font-size="16"
        fill="{accent}55" font-weight="600" text-anchor="middle" letter-spacing="3">
    {_escape(brand_name)}
  </text>

  <!-- Corner accents -->
  <rect x="60" y="60" width="40" height="3" rx="1.5" fill="{highlight}33"/>
  <rect x="60" y="60" width="3" height="40" rx="1.5" fill="{highlight}33"/>
  <rect x="980" y="1017" width="40" height="3" rx="1.5" fill="{highlight}33"/>
  <rect x="1017" y="980" width="3" height="40" rx="1.5" fill="{highlight}33"/>
</svg>"""

    return svg
