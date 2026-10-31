---
name: swiftui-expert
description: Use when writing, reviewing, or refactoring SwiftUI code for iOS or macOS
  — state, @Observable, view composition, performance, Liquid Glass, SDK 27, and Instruments
  trace analysis. Also use for iPhone Duo / foldable / large-display work, NavigationSplitView,
  ArrangementView, ReservedRegion, hinge effects, vertical bars, and the Xcode trace-driven
  improvement loop. Authored by Antoine van der Lee + Omar Elsayed; mirrored from
  AvdLee/SwiftUI-Agent-Skill on install.
trust: platform-product-manager
reviewed: true
source: shared/swiftui-expert-skill (mirror of https://github.com/AvdLee/SwiftUI-Agent-Skill
  @ 204dba7)
metadata:
  hermes:
    tags:
    - swiftui
    - ios
    - apple
    - avdlee
    - swiftlee
    - iphone-duo
    - performance
    - xctrace
    - instruments
    - foldable
    related_skills:
    - iphone-duo-apple-hig-kit
    - iphone-duo-form-factor-showcase
    - ios-prototype-scaffold
version: 2.0.0
---

# SwiftUI Expert Skill (AvdLee, mirrored)

> **This SKILL.md is the Hermes gate wrapper. The real triage file is at `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/SKILL.md` — load that one via `skill_view(name='swiftui-expert')`.**

This skill is the **canonical third-party SwiftUI correctness + performance reference** for Hermes (31.4k weekly installs, MIT, official `agentskills.io` open format, co-maintained by Antoine van der Lee — the SwiftLee blog).

## Why mirrored, not symlinked

AvdLee's repo updates ~2x/week. A symlink would mean our runtime copy drifts upstream without any Hermes-side review of the changes. The mirror pattern (Pitfall 5 fix path 1) gives us:

- A `ParzivalWins/SwiftUI-Agent-Skill` fork we control
- A gitlink + `.gitmodules` entry in the parent `HermesAgent` repo so fresh clones pull the right SHA
- Hermes-side review on every `git pull` from `AvdLee/SwiftUI-Agent-Skill` (the operator reviews the diff before flipping `reviewed: true` on a new commit)

## Update procedure

```bash
# 1. Pull latest from upstream AvdLee
cd ~/Desktop/HermesAgent/skills-registry/imported/SwiftUI-Agent-Skill
git fetch AvdLee
git log AvdLee/main..HEAD   # see what's diverged
# 2. Merge (or rebase) — operator reviews the diff before continuing
git merge AvdLee/main
# 3. Push to our ParzivalWins fork
git push ParzivalWins main
# 4. Update the gitlink in the parent repo to the new SHA
NEW_SHA=$(git rev-parse HEAD)
cd ~/Desktop/HermesAgent
git update-index --cacheinfo 160000,$NEW_SHA,skills-registry/imported/SwiftUI-Agent-Skill
# 5. Run the gate
make check-skills-gate
# 6. If clean, sync to runtime
make sync-skills
```

## What this skill does NOT cover (per the AvdLee AGENTS.md)

- Swift concurrency (use a separate Swift Concurrency skill)
- Architectural opinions (MVVM/VIPER/TCA mandates)
- Code formatting / linting rules
- Project structure mandates
- Build system configuration

The iPhone Duo HIG kit + Form Factor Showcase skills cover the iPhone Duo surface; this skill covers the general SwiftUI correctness layer underneath.

## Local content map

| Topic | Reference file in the AvdLee mirror |
|---|---|
| State management, @Observable, @Bindable, decision flowchart | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/state-management.md` |
| View composition, subview extraction, lazy containers, ZStack vs overlay, compositingGroup | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/view-structure.md` |
| Performance, hang analysis, hot paths, dependency granularity | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/performance-patterns.md` |
| **iPhone Duo, foldable, ArrangementView, ReservedRegion, hinge effects, vertical bars** | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/iphone-duo.md` |
| **Instruments .trace recording (xctrace wrapper scripts)** | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/trace-recording.md` + `references/trace-analysis.md` + `scripts/` |
| Layout best practices, safe areas, GeometryReader alternatives | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/layout-best-practices.md` |
| Lists + ForEach identity | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/list-patterns.md` |
| Navigation, sheets, NavigationSplitView, Inspector | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/sheet-navigation-patterns.md` |
| Toolbars, customization, overflow, vertical-bar APIs | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/toolbar-patterns.md` |
| Liquid Glass (iOS 26+) | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/liquid-glass.md` |
| Deprecated API lookup (latest-apis.md) | `imported/SwiftUI-Agent-Skill/skills/swiftui-expert-skill/references/latest-apis.md` |

**Today (2026-10-08), 4 of these directly informed the Duo Cast build:**
- `state-management.md` → revealed SpotlightStore is still pre-iOS-17 (items 1 in analysis)
- `view-structure.md` → confirmed 5/5 poses use the right extract-subviews pattern
- `performance-patterns.md` → informed the trace analysis step
- `iphone-duo.md` → revealed the 5-bullet technique picker that should replace HIG kit's "design for two size classes" rule (item 3 in analysis)

---

## Core Principle & Mental Model (HSR-8 Contract)

- **Overview & Objective**: Mirrored AvdLee SwiftUI Agent Skill wrapper governing `@Observable` state management, view composition, Instruments `xctrace` profiling, and iPhone Duo foldable APIs.
- **Mental Model**: Sweep memory first, enforce deterministic pre-flight validation gates before mutating state, preserve all source provenance, and verify every output artifact on disk.

## When to Use & Trigger Conditions

- Trigger `swiftui-expert` whenever the operator request matches the scenarios above or when an upstream orchestrator delegates this domain step.

## When NOT to Use (Counter-Triggers & Anti-Patterns)

- **When NOT to use**: Never invoke `swiftui-expert` outside its documented scope, never bypass pre-flight safety/authentication gates, and never fabricate unverified outputs (**red flag / anti-pattern**).

## Stage 0: Memory-First Pre-Flight

1. Run `memory_search(query="swiftui-expert rules pitfalls conventions")` and `memory_recall(query="swiftui-expert")`.
2. Check `MEMORY.md` pointers and `~/Documents/LLM-Knowledge/` context before executing.

## Decision Matrix & Branching Logic

| Condition / Signal (`If ...`) | Decision Branch / Tier (`Then ...`) | Deterministic Rubric & Action |
|---|---|---|
| Pre-flight prerequisites & env vars verified | **Tier 1: Standard Execution** | Execute Stage 1 → Stage 2 → Stage 3 workflow deterministically |
| Missing prerequisite, expired auth, or failed gate | **Tier 2: Safe Abort & Recovery** | Halt mutation, emit structured diagnostic error, and run recovery steps |
| Dry-run flag enabled or exploratory check requested | **Tier 3: Read-Only Inspection** | Produce plan/preview artifact only with zero external side effects |

## Hypothesis, Rationale & Diagnostic Analysis

- Formulate an explicit operational **hypothesis** and execution **plan** before running commands, **analyze** intermediate outputs against the expected schema, and document the **rationale** when evaluating edge cases.

## Hard Gates & Non-Negotiable Invariants

1. **Deterministic Gate Rule**: Never mark work complete without passing the verification checklist and deterministic validation script.
2. **Service & Gateway Safety Invariant**: Never spawn standalone per-profile gateways (`ai.hermes.gateway-<profile>`); only use `launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway` or `hermes -p <profile> gateway restart`.

### Stage 1: Pre-Flight & Environment Check
Confirm all input parameters, paths, and prerequisites documented above.

### Stage 2: Core Domain Execution
Execute the primary procedure of `swiftui-expert` and capture structured outputs.

### Stage 3: Verification, Common Pitfalls & Self-Healing Recovery
Run the deterministic contract validator and smoke check:

```bash
python3 skills-registry/shared/swiftui-expert-skill/scripts/validate_output.py --json
```

- **Common Pitfalls & Troubleshooting**: If a step fails due to missing env vars, stale locks, or transient tool errors, **recover** via the fallback/retry/rollback procedures documented in this skill (`references/guide.md`) rather than ignoring the failure.
- [ ] Stage 0 pre-flight, deterministic execution, and post-run verification completed.

## Multi-Agent Handoff & Composability

- **Upstream / Downstream Handoff**: Composes via `delegate_task`, `subagent`, `kanban`, or `linear` handoffs using the `related_skills` declared in YAML frontmatter.
- **Input Prerequisite & Output Deliverable Contract**: Accepts typed prerequisites and emits a verified `.md` / `.json` deliverable artifact with full provenance.

## Worked Example & Evaluation Harness

- **Worked Example & Benchmark Eval**: Execute the verification command above and run `pytest` / `unittest` alongside `python3 scripts/skills_registry_gate.py` to benchmark contract compliance. See [`references/guide.md`](references/guide.md) for detailed reference tables.
