#!/usr/bin/env python3
"""
Test module mapping logic to debug CTX video selection.
"""

import json
from pathlib import Path

# Read the manifest
manifest_path = Path(__file__).parent.parent.parent / "kb" / "demoforge_manifest.json"
with open(manifest_path) as f:
    manifest = json.load(f)

module_to_demos = manifest["module_to_demos"]
demos_by_id = manifest["demos_by_id"]

print("=" * 80)
print("MODULE-TO-DEMO MAPPING TEST")
print("=" * 80)

# Test cases: (module_name_from_source, intent, expected_demo_name)
test_cases = [
    ("CTX", "how_to", "CTWA Demo"),
    ("CTX", "setup", "CTWA Demo"),
    ("CTX", "overview", "CTWA Demo"),
    ("Bot Studio", "how_to", "Bot Studio"),
    ("Bot Studio", "setup", "Bot Studio"),
    ("AI Admin", "overview", "AI Admin Demo"),
    ("Campaign Manager", "task", "Campaign Manager Demo"),
]

print("\nTest Cases:")
print("-" * 80)

for module_name, intent, expected_demo_name in test_cases:
    # Simulate _module_from_source -> select_demoforge_demo logic
    module_key = str(module_name).lower().replace("-", "_").replace(" ", "_")
    intent_key = str(intent).lower().replace("-", "_")

    module_demos = module_to_demos.get(module_key, {})
    demo_id = module_demos.get(intent_key)

    if demo_id:
        demo = demos_by_id.get(demo_id, {})
        actual_demo_name = demo.get("name", "UNKNOWN")
        status = "✓" if actual_demo_name == expected_demo_name else "✗"
        print(f"{status} module='{module_name}' intent='{intent}'")
        print(f"   module_key='{module_key}', intent_key='{intent_key}'")
        print(f"   demo_id={demo_id}")
        print(f"   expected='{expected_demo_name}', got='{actual_demo_name}'")
    else:
        print(f"✗ module='{module_name}' intent='{intent}'")
        print(f"   module_key='{module_key}', intent_key='{intent_key}'")
        print(f"   NO DEMO FOUND - available modules: {list(module_to_demos.keys())}")

    print()

print("=" * 80)
print("AVAILABLE MODULES IN MANIFEST:")
print(list(module_to_demos.keys()))
print("=" * 80)
