#!/usr/bin/env python3
"""Deterministic contract validator for the `swiftui-expert` Hermes skill."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Core Principle & Mental Model",
    "When to Use & Trigger Conditions",
    "When NOT to Use",
    "Stage 0: Memory-First Pre-Flight",
    "Decision Matrix & Branching Logic",
    "Hypothesis, Rationale & Diagnostic Analysis",
    "Hard Gates & Non-Negotiable Invariants",
    "Multi-Agent Handoff & Composability",
    "Verification, Common Pitfalls & Self-Healing Recovery",
    "Worked Example & Evaluation Harness",
]


def validate_skill_md(skill_md: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not skill_md.is_file():
        return False, [f"Missing SKILL.md at {skill_md}"]
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not (50 <= len(lines) <= 500):
        errors.append(f"Line count {len(lines)} outside 50..500 bounds")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append("Missing valid YAML frontmatter block")
    if "reviewed: true" not in text:
        errors.append("Frontmatter must declare reviewed: true")
    for sec in REQUIRED_SECTIONS:
        if sec.lower() not in text.lower():
            errors.append(f"Missing required section: {sec}")
    if "- [ ]" not in text:
        errors.append("Missing interactive verification checklist (- [ ])")
    return len(errors) == 0, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate swiftui-expert SKILL.md contract")
    parser.add_argument(
        "--skill-md",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "SKILL.md",
        help="Path to SKILL.md",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()
    ok, errors = validate_skill_md(args.skill_md)
    payload = {"skill": "swiftui-expert", "valid": ok, "errors": errors}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] swiftui-expert: {len(errors)} error(s)")
        for err in errors:
            print(f"  - {err}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
