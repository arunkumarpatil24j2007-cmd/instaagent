# Instagram Specialist Agent 📸

An autonomous, production-grade **Instagram Specialist Agent** engineered for multi-agent distribution operating systems. Transforms brand identity, strategic objectives, and audience insights into captivating Instagram content—including multi-slide educational carousels, bold static posts, interactive multi-frame story sequences, and multi-week balanced content calendars—complete with automated SVG visual mockup generation, 12 visual design archetypes, and a 10-point self-critic evaluation engine.

---

## 🌟 Key Architecture & Capabilities

### 1. Multi-Modality Content Generation
- **Multi-Slide Carousels (4:5 Portrait)**: Generates 5–10 slide sequences with hook slides, educational content cards, retention cues (*"Swipe to reveal"*, micro-breadcrumbs), and high-conversion call-to-action closing slides.
- **High-Impact Static Posts (1:1 / 4:5)**: Optimized for algorithmic feed discovery with punchy headlines, aesthetic background gradients, badge overlays, and structured captions.
- **Interactive Story Sequences (9:16 Vertical)**: Produces 3–7 frame narrative flows with native interactive sticker specifications (polls, emoji sliders, quizzes, question boxes, and countdowns).
- **Multi-Week Content Calendars**: Plans balanced distribution strategies across days of the week, alternating educational, community, promotional, and behind-the-scenes content archetypes.
- **Reels Notice Guardrail**: Gracefully intercepts video/Reels requests with an informative, contract-compliant `"coming_soon"` status payload.

### 2. 12 Visual Design Archetypes & Automated SVG Rendering
Built-in visual layout engine generates production-quality, responsive SVG creative previews matching 12 distinct aesthetic archetypes:
1. `bold_minimalist`: Clean negative space, typography-led hierarchy
2. `technical_schematic`: Blueprint grids, technical annotations, data callouts
3. `gradient_punch`: Vibrant modern multi-stop gradients with glassmorphism
4. `neo_editorial`: Sophisticated magazine typography and serif headlines
5. `dark_terminal`: Cyber/developer monospace styling with glowing accents
6. `retro_futuristic`: 80s/90s neon retro synth aesthetic
7. `warm_organic`: Earth tones, soft curves, and lifestyle palettes
8. `corporate_sleek`: Premium enterprise B2B precision
9. `creative_chaos`: Asymmetric stickers, overlapping textures, high energy
10. `data_viz`: Infographic charts, metrics, and bar comparisons
11. `quote_monument`: Monumental quotation marks and centered typography
12. `split_comparison`: Side-by-side Before/After or Do/Don't visual layouts

### 3. Aspect Ratio & Dimension Standards
Enforces strict platform-optimized dimensions across all generated assets:
- **Feed Carousels**: 1080 × 1350 px (4:5 portrait) for maximum screen real estate
- **Feed Static Posts**: 1080 × 1080 px (1:1 square) or 1080 × 1350 px (4:5 portrait)
- **Stories**: 1080 × 1920 px (9:16 vertical) with safe margins avoiding UI header/footer cutoffs

### 4. 10-Point Editorial & Visual Critic
Every generated piece of content passes through an autonomous critique and revision cycle:
- Hook punchiness & pattern interrupt score
- Retention pacing & swipe incentive
- Visual typography legibility & contrast ratio
- Brand palette adherence & tone consistency
- Call-to-action placement & conversion clarity
- Hashtag optimization (3–5 targeted niche tags, 0 spam tags)

### 5. Interactive Developer Preview Console
- Modern dark-mode web console running at `http://localhost:5002`.
- Interactive carousel slider with real-time slide navigation and live SVG previews.
- Story frame carousel with simulated mobile phone viewport.
- One-click sample test loader for Carousels, Static Posts, Stories, Calendars, and Reels.
- Copy-to-clipboard for Instagram captions, hashtags, and raw JSON payloads.

---

## 📂 Project Structure

```
instaagent/
├── instagram_agent/
│   ├── agent/                     # Specialist Agent orchestration & pipelines
│   │   ├── instagram_agent.py     # Main agent entrypoint & workflow
│   │   ├── strategy_planner.py    # Strategic goal & archetype planner
│   │   ├── writer.py              # Copywriting & caption engine
│   │   ├── calendar_planner.py    # Multi-day schedule generation
│   │   ├── polisher.py            # Formatting & hashtag polisher
│   │   ├── critic.py              # 10-point editorial self-critic
│   │   ├── researcher.py          # Trend & hashtag research adapter
│   │   └── reviser.py             # Autonomous revision loop
│   ├── creative/                  # Visual SVG generators
│   │   ├── carousel_generator.py  # 4:5 slide layout & visual flow
│   │   ├── static_post_generator.py # 1:1 and 4:5 feed card generator
│   │   └── story_generator.py     # 9:16 vertical story frame generator
│   ├── knowledge/                 # Instagram platform specifications & standards
│   │   └── instagram_standards.py
│   ├── schemas/                   # Pydantic input/output contracts
│   │   ├── input_contract.py      # InstagramAgentInput schema
│   │   ├── output_contract.py     # InstagramAgentOutput schema
│   │   ├── strategy.py            # Strategy & archetype specifications
│   │   ├── critique.py            # Editorial critique scores
│   │   └── research.py            # Trend & keyword models
│   ├── state/                     # Agent working state definitions
│   │   └── agent_state.py
│   ├── tests/                     # Unit and integration test suite
│   │   └── test_instagram_agent.py
│   └── tools/                     # Tool abstractions & provider adapters
│       ├── base.py                # Abstract tool interfaces
│       ├── mock_providers.py      # Zero-dependency local mock providers
│       ├── registry.py            # Dependency injection registry
│       ├── tavily_provider.py     # Tavily AI Search integration
│       └── airtop_provider.py     # AirTop cloud browser integration
├── instagram_test_inputs/         # Production test payloads
│   ├── 01_carousel_input.json
│   ├── 02_static_post_input.json
│   ├── 03_story_sequence_input.json
│   ├── 04_content_calendar_input.json
│   ├── 05_missing_context_input.json
│   └── 06_reels_input.json
├── instagram_outputs/             # Pre-generated sample output payloads
├── example_input.json             # Default sample input payload
├── output.json                    # Default sample output payload
├── preview.html                   # Interactive visual preview console
├── run_agent.py                   # Command-line test runner
├── server.py                      # Local development testbed server
├── test_airtop.py                 # AirTop provider test script
├── test_tavily.py                 # Tavily provider test script
├── requirements.txt               # Python package dependencies
├── .env.example                   # Environment variables template
└── .gitignore                     # Git ignore rules
```

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/arunkumarpatil24j2007-cmd/instaagent.git
cd instaagent
pip install -r requirements.txt
```

### 2. Environment Configuration (Optional)

Copy `.env.example` to `.env` to supply API keys for live web search:

```bash
cp .env.example .env
```

*(Note: The agent runs fully autonomously out-of-the-box using built-in mock providers if no API keys are supplied.)*

### 3. Run the Test Suite

Execute the unit and integration tests covering contract validation, carousel generation, static posts, stories, calendars, and Reels notices:

```bash
python -m unittest discover -s instagram_agent/tests
```

### 4. Run CLI Generation

Run all test inputs or execute against a single input file:

```bash
# Run all inputs in instagram_test_inputs/
python run_agent.py

# Run a specific input file
python run_agent.py instagram_test_inputs/01_carousel_input.json
```

### 5. Launch the Visual Preview Console

Start the built-in HTTP server to explore generated content interactively:

```bash
python server.py
```

Open [http://localhost:5002](http://localhost:5002) in your browser to test inputs, view live rendered SVGs, and inspect full JSON contracts.

---

## 📋 Input & Output Contract

### Sample Input Payload (`example_input.json`)
```json
{
  "brand": {
    "brand_name": "DevFlow",
    "industry": "Developer Tools & Cloud Infrastructure",
    "target_audience": "Senior Software Engineers, DevOps Leads, Engineering Managers",
    "account_handle": "@devflow_hq",
    "colors": ["#0F172A", "#3B82F6", "#10B981"]
  },
  "task": {
    "type": "create_content",
    "topic": "5 Microservices Anti-Patterns Every Tech Lead Should Know",
    "objective": "authority",
    "target_format": "carousel"
  },
  "constraints": {
    "content_type": "carousel",
    "tone": "authoritative_yet_approachable",
    "max_slides": 7
  }
}
```

### Sample Output Contract Structure
```json
{
  "status": "success",
  "content_type": "carousel",
  "strategy": {
    "core_angle": "Actionable technical breakdown of subtle architectural traps",
    "visual_archetype": "technical_schematic",
    "palette": ["#0F172A", "#3B82F6", "#10B981"]
  },
  "carousel": {
    "title": "5 Microservices Anti-Patterns",
    "aspect_ratio": "4:5",
    "total_slides": 7,
    "slides": [
      {
        "slide_number": 1,
        "role": "hook",
        "headline": "5 Microservices Anti-Patterns",
        "body": "That seem harmless until your cluster goes down at 2 AM.",
        "svg_markup": "<svg viewBox='0 0 1080 1350'>...</svg>"
      }
    ]
  },
  "quality": {
    "overall_score": 8.8,
    "status": "passed"
  }
}
```

---

## 📄 License

MIT License. Designed for modular multi-agent distribution systems.
