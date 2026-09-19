# Connecting InstaAgent to Leno OS 🚀

This guide explains how to connect the **Instagram Specialist Agent (`instaagent`)** directly to **Leno OS (Digital Distribution OS)** and **Leno UI**.

---

## ⚡ Option 1: Live HTTP Microservice (Recommended)

Leno OS and Leno UI interact with specialist agents as distributed HTTP microservices.

### Step 1: Start the InstaAgent Server
In the `instaagent` directory:

```bash
# Install dependencies
pip install -r requirements.txt

# Launch server (runs on port 5002 by default, or supply custom port)
python server.py
# Or: PORT=5001 python server.py
```

You should see:
```text
======================================================================
  📸 INSTAGRAM SPECIALIST AGENT — LENO OS COMPATIBLE DAEMON
======================================================================
  🌐 Live Web Preview:   http://localhost:5002
  ⚡ Leno OS Connector:  http://localhost:5002/api/draft
  🚀 Leno UI Cockpit:    http://localhost:5002/api/generate-post
  📡 Agent Raw Contract: http://localhost:5002/api/run-instagram-agent
  🩺 Health & Overview:  http://localhost:5002/api/overview
----------------------------------------------------------------------
```

### Step 2: Configure Leno OS Environment
In your Leno OS project (`.env.local` or `.env`):

```bash
INSTAGRAM_AGENT_URL=http://localhost:5002
```

---

## 💻 Option 2: Drop-in Next.js / TypeScript Connector

We have included a production-ready connector `leno_connector.ts` in this repository.

### How to use it in Leno OS:
1. Copy `leno_connector.ts` from `instaagent/` into your Leno OS project:
   ```bash
   cp leno_connector.ts /path/to/Leno_OS/src/agents/platforms/instagram.ts
   ```

2. That's it! Leno OS's orchestrator can now import and call `generateDraft`:
   ```typescript
   import { generateDraft } from "@/agents/platforms/instagram";

   const draft = await generateDraft(brandProfile, campaignPlan, strategy);
   // Returns validated Leno OS Draft: { platform: "instagram", body: "...", hashtags: [...] }
   ```

### Features of the Connector:
- **Zod Schema Validated**: Output strictly satisfies Leno OS's `DraftSchema`.
- **Resilient Fallback**: If the Python daemon is temporarily restarting or offline, the connector falls back gracefully without breaking campaign runs.
- **Rich Visual Metadata**: Returns slide counts, SVG visual previews, and 10-point critique scores.

---

## 🐍 Option 3: Direct Python Package Import

If you are running a Python orchestrator or backend:

```bash
# Install package in editable mode
pip install -e .
```

Then in your Python code:
```python
from instagram_agent.adapter import run_for_leno_os

leno_payload = {
    "brand": {
        "name": "NexusAI Solutions",
        "positioning": "Enterprise AI Orchestration",
        "audience": "CTOs and Tech Leads",
        "tone_words": ["authoritative", "technical", "human"],
        "primary_color": "#0F172A",
        "secondary_color": "#3B82F6"
    },
    "plan": {
        "goal": "Authority",
        "key_message": "5 Microservices Anti-patterns",
        "platforms": ["instagram"]
    },
    "strategy": {
        "angle": "Architectural failure modes in high-scale systems",
        "hooks": ["Your cluster is fine until 2 AM."]
    }
}

draft = run_for_leno_os(leno_payload)
print(draft["platform"])    # 'instagram'
print(draft["body"])        # Platform-native humanized caption
print(draft["hashtags"])    # Curated hashtags
print(draft["slides"])      # Complete 4:5 SVG slide deck
print(draft["critique"])    # Leno OS 4-dimension critique scorecard
```

---

## 🌐 Connecting with Leno UI Cockpit

The Leno UI Creative Cockpit (`leno ui`) communicates directly with agent backends:

- **Healthcheck**: `GET /api/overview` confirms operational status and capabilities.
- **Post Generation**: `POST /api/generate-post` accepts `{ topic, core_message, format }` and returns Instagram carousel slides, hook, caption, and SVG preview.

To connect Leno UI to InstaAgent, point `API_BASE` in `leno ui/js/api.js` to `http://localhost:5002` (or run InstaAgent on port `5001`).

---

## 📋 API Reference Summary

| Endpoint | Method | Purpose | Input Payload | Output |
| :--- | :--- | :--- | :--- | :--- |
| `/api/overview` | `GET` | Healthcheck & Capabilities | None | `{ status: "operational", agent: "Instagram Specialist Agent", ... }` |
| `/api/draft` | `POST` | Leno OS Draft Connector | `{ brand, plan, strategy }` | `{ platform: "instagram", body, hashtags, visual_asset, critique }` |
| `/api/generate-post` | `POST` | Leno UI Creative Cockpit | `{ topic, core_message, format }` | `{ status: "success", instagram: { slides, svg_preview, ... } }` |
| `/api/run-instagram-agent` | `POST` | Raw Specialist Contract | `{ brand, task, constraints }` | `InstagramAgentOutput` |
