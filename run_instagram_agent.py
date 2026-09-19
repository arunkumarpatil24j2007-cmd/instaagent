"""
Executable Runner Script for Instagram Specialist Agent.
Provides human-friendly terminal output and saves complete JSON payload to instagram_outputs/.
"""

import json
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from instagram_agent.agent.instagram_agent import InstagramSpecialistAgent


def run_single_test(agent, input_path: Path, output_dir: Path):
    print(f"\n{'='*65}")
    print(f"  TEST: {input_path.stem}")
    print(f"{'='*65}")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_input = json.load(f)

    task_type = raw_input.get("task", {}).get("type", "create_content")
    brand_name = raw_input.get("brand", {}).get("brand_name", "Unknown Brand")
    print(f"  Task Type   : {task_type}")
    print(f"  Brand       : {brand_name}")

    print(f"\n  Running Instagram agent pipeline...")
    output_dict = agent.run_raw(raw_input)

    output_file = output_dir / f"{input_path.stem}_output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_dict, f, indent=2)

    status = output_dict.get("status", "unknown")
    print(f"  Status      : {status.upper()}")

    if status == "coming_soon":
        notice = output_dict.get("reels_notice", {})
        print(f"  Notice      : {notice.get('notice', 'Reels — Coming Soon')}")
    elif status == "missing_context":
        mc = output_dict.get("missing_context", {})
        print(f"  Missing     : {', '.join(mc.get('missing_fields', []))}")
    else:
        content_type = output_dict.get("content_type", "unknown")
        print(f"  Content Type: {content_type}")

        if content_type == "carousel" and output_dict.get("carousel"):
            c = output_dict["carousel"]
            print(f"  Carousel    : '{c.get('title')}' ({c.get('total_slides')} slides)")
        elif content_type == "static_post" and output_dict.get("static_post"):
            s = output_dict["static_post"]
            print(f"  Static Post : '{s.get('headline')}'")
        elif content_type == "story_sequence" and output_dict.get("story_sequence"):
            st = output_dict["story_sequence"]
            print(f"  Story Flow  : '{st.get('sequence_title')}' ({st.get('total_stories')} stories)")
        elif content_type == "content_calendar" and output_dict.get("calendar"):
            cal = output_dict["calendar"]
            print(f"  Calendar    : {cal.get('duration')} ({cal.get('total_posts')} scheduled posts)")

        quality = output_dict.get("quality")
        if quality:
            print(f"  Quality     : {quality.get('status')} (Score: {quality.get('overall_score')}/10)")

    print(f"\n  [OK] Output saved to: {output_file.name}")
    return output_dict


def main():
    print("=" * 65)
    print("  INSTAGRAM SPECIALIST AGENT — EXECUTION RUNNER")
    print("=" * 65)

    agent = InstagramSpecialistAgent()

    input_dir = Path(__file__).parent / "instagram_test_inputs"
    output_dir = Path(__file__).parent / "instagram_outputs"
    output_dir.mkdir(exist_ok=True)

    if not input_dir.exists():
        print(f"Error: Test inputs directory not found: {input_dir}")
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        custom_path = Path(sys.argv[1])
        if custom_path.exists():
            input_files = [custom_path]
        else:
            print(f"Error: Specified input file not found: {custom_path}")
            sys.exit(1)
    else:
        input_files = sorted(input_dir.glob("*.json"))

    if not input_files:
        print(f"Error: No JSON test inputs found in {input_dir}")
        sys.exit(1)

    print(f"\n  Processing {len(input_files)} input file(s)")

    results = []
    for input_path in input_files:
        result = run_single_test(agent, input_path, output_dir)
        results.append({"test": input_path.stem, "status": result.get("status", "unknown")})

    print(f"\n\n{'='*65}")
    print(f"  EXECUTION SUMMARY")
    print(f"{'='*65}")
    for r in results:
        print(f"  {r['test']:35s} → {r['status'].upper()}")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
