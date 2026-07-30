#!/usr/bin/env python3
"""Simple DemoForge integration test - shows manifest structure and mapping."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Load manifest
manifest_path = ROOT / "kb" / "demoforge_manifest.json"
manifest = json.loads(manifest_path.read_text())

print("=" * 70)
print("DemoForge Manifest Structure Analysis")
print("=" * 70)

# Check structure
if "module_to_demos" in manifest:
    print("\n✓ Found 'module_to_demos' mapping (new indexed format)")
    print(f"  Modules available: {list(manifest['module_to_demos'].keys())[:5]}...")
elif "projects" in manifest:
    print("\n✓ Found 'projects' structure (raw DemoForge export)")
    projects = manifest.get("projects", [])
    print(f"  Total projects: {len(projects)}")

    # Build demo lookup
    all_demos = {}
    module_mapping = {}

    for project in projects:
        project_name = project.get("name")
        for demo in project.get("demos", []):
            demo_id = demo.get("id")
            demo_name = demo.get("name")
            use_case = demo.get("use_case", "")

            all_demos[demo_id] = {
                "id": demo_id,
                "name": demo_name,
                "project": project_name,
                "use_case": use_case,
                "industry": demo.get("industry"),
                "persona": demo.get("persona"),
            }

            print(f"\n  Demo: {demo_name}")
            print(f"    ID: {demo_id}")
            print(f"    Project: {project_name}")
            print(f"    Use Case: {use_case[:80]}...")

print("\n" + "=" * 70)
print("Test Case Mapping Strategy")
print("=" * 70)

test_cases = [
    {
        "query": "How do I create a campaign?",
        "intent": "how_to",
        "module": "campaigns",
        "expect_demo": "Campaign Manager Demo",
    },
    {
        "query": "What is Bot Studio?",
        "intent": "overview",
        "module": "bot_studio",
        "expect_demo": None,  # overview typically → YouTube
    },
    {
        "query": "Show me a demo of Gupshup for retail",
        "intent": "overview",
        "module": None,
        "expect_demo": "General Demo",  # broad fallback
    },
]

print("\nTest Case Expectations:")
for i, tc in enumerate(test_cases, 1):
    print(f"\n{i}. Query: {tc['query']}")
    print(f"   Intent: {tc['intent']}")
    print(f"   Module: {tc['module']}")
    print(f"   Expected: {tc['expect_demo']}")

print("\n" + "=" * 70)
print("DemoForge Integration Points")
print("=" * 70)

print("""
1. Query Processing:
   - Extract intent (how_to, overview, setup, etc.)
   - Extract module (campaigns, bot_studio, rcs, whatsapp, etc.)

2. Demo Selection:
   - Use kb_video.select_demoforge_demo(query, intent, module, context)
   - Returns: demo_id, name, industry, persona, (share_token=None)

3. API Integration:
   - Call DemoForge API to create_share_token(demo_id)
   - Construct share URL: demoforge-ui.gupshup.io/s/{share_token}
   - Return to user

4. Fallback Strategy:
   - If no module→demo mapping: fall back to YouTube
   - If no video available: plain text answer
   - If API timeout: fallback to YouTube

5. Success Metrics:
   - Query → Demo selection accuracy
   - API response latency
   - Share token generation success rate
   - User click-through on demo link
""")

print("=" * 70)
