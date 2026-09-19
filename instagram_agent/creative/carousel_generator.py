"""
Carousel SVG Generator for Instagram Agent.
Generates branded 1080×1080 carousel slide SVG graphics.
"""

from typing import Dict, Any, List, Optional
import html


def _escape(text: str) -> str:
    """Safely escape text for SVG embedding."""
    return html.escape(str(text), quote=True)


def _wrap_text(text: str, max_chars: int = 35) -> List[str]:
    """Wrap text into lines for SVG rendering."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        if len(test) <= max_chars:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines or [""]


def generate_carousel_slide_svg(
    slide_number: int,
    total_slides: int,
    title: str,
    copy: str,
    brand_name: str = "Brand",
    colors: Optional[List[str]] = None,
    slide_type: str = "content",
) -> str:
    """Generate a single 1080×1080 carousel slide as SVG."""

    c = colors or ["#0F172A", "#38BDF8", "#F43F5E"]
    bg_primary = c[0] if len(c) > 0 else "#0F172A"
    accent = c[1] if len(c) > 1 else "#38BDF8"
    highlight = c[2] if len(c) > 2 else "#F43F5E"

    safe_title = _escape(title)
    safe_brand = _escape(brand_name)

    # Wrap copy text
    copy_lines = _wrap_text(copy, max_chars=40)
    copy_tspans = ""
    for i, line in enumerate(copy_lines[:6]):
        y_offset = 580 + (i * 42)
        copy_tspans += f'<tspan x="540" dy="{42 if i > 0 else 0}">{_escape(line)}</tspan>'

    # Progress dots
    dots = ""
    for i in range(total_slides):
        cx = 540 - ((total_slides - 1) * 12) + (i * 24)
        fill = accent if i == slide_number - 1 else f"{accent}44"
        dots += f'<circle cx="{cx}" cy="1020" r="6" fill="{fill}"/>'

    # Determine gradient based on slide type
    if slide_type == "hook":
        gradient_stops = f"""
            <stop offset="0%" stop-color="{highlight}22"/>
            <stop offset="100%" stop-color="{bg_primary}"/>
        """
    elif slide_type == "cta":
        gradient_stops = f"""
            <stop offset="0%" stop-color="{accent}33"/>
            <stop offset="100%" stop-color="{bg_primary}"/>
        """
    else:
        gradient_stops = f"""
            <stop offset="0%" stop-color="{bg_primary}"/>
            <stop offset="100%" stop-color="{bg_primary}ee"/>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <linearGradient id="bg_{slide_number}" x1="0" y1="0" x2="1" y2="1">
      {gradient_stops}
    </linearGradient>
    <filter id="glow_{slide_number}">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1080" fill="url(#bg_{slide_number})" rx="0"/>
  <rect x="0" y="0" width="1080" height="1080" fill="{bg_primary}" rx="0"/>

  <!-- Decorative accent line -->
  <rect x="80" y="120" width="60" height="4" rx="2" fill="{accent}"/>

  <!-- Slide number badge -->
  <text x="80" y="170" font-family="Inter, Arial, sans-serif" font-size="18"
        fill="{accent}88" font-weight="500" letter-spacing="2">
    {_escape(f'{slide_number:02d} / {total_slides:02d}')}
  </text>

  <!-- Title -->
  <text x="540" y="380" font-family="Outfit, Arial, sans-serif" font-size="52"
        fill="white" font-weight="700" text-anchor="middle" filter="url(#glow_{slide_number})">
    {safe_title}
  </text>

  <!-- Copy -->
  <text x="540" y="560" font-family="Inter, Arial, sans-serif" font-size="28"
        fill="white" opacity="0.85" text-anchor="middle" line-height="42">
    {copy_tspans}
  </text>

  <!-- Brand watermark -->
  <text x="540" y="960" font-family="Outfit, Arial, sans-serif" font-size="16"
        fill="{accent}66" font-weight="600" text-anchor="middle" letter-spacing="3">
    {safe_brand}
  </text>

  <!-- Progress dots -->
  {dots}

  <!-- Accent corner decoration -->
  <rect x="920" y="80" width="80" height="3" rx="1.5" fill="{highlight}44"/>
  <rect x="997" y="80" width="3" height="80" rx="1.5" fill="{highlight}44"/>
</svg>"""

    return svg


def generate_carousel_svgs(
    slides_data: List[Dict[str, str]],
    brand_name: str = "Brand",
    colors: Optional[List[str]] = None,
) -> List[str]:
    """Generate SVGs for all carousel slides."""
    total = len(slides_data)
    svgs = []
    for i, slide in enumerate(slides_data):
        slide_type = "hook" if i == 0 else ("cta" if i == total - 1 else "content")
        svg = generate_carousel_slide_svg(
            slide_number=i + 1,
            total_slides=total,
            title=slide.get("title", ""),
            copy=slide.get("copy", ""),
            brand_name=brand_name,
            colors=colors,
            slide_type=slide_type,
        )
        svgs.append(svg)
    return svgs
