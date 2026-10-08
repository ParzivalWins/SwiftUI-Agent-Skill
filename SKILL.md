---
name: swiftui-expert
description: Use when writing, reviewing, or refactoring SwiftUI code for iOS or macOS — state, @Observable, view composition, performance, Liquid Glass, SDK 27, and Instruments trace analysis. Also use for iPhone Duo / foldable / large-display work, NavigationSplitView, ArrangementView, ReservedRegion, hinge effects, vertical bars, and the Xcode trace-driven improvement loop. Authored by Antoine van der Lee + Omar Elsayed; mirrored from AvdLee/SwiftUI-Agent-Skill on install.
trust: platform-product-manager
reviewed: true
source: shared/swiftui-expert-skill (mirror of https://github.com/AvdLee/SwiftUI-Agent-Skill @ 204dba7)
metadata:
  hermes:
    tags: [swiftui, ios, apple, avdlee, swiftlee, iphone-duo, performance, xctrace, instruments, foldable]
    related_skills: [iphone-duo-apple-hig-kit, iphone-duo-form-factor-showcase, ios-prototype-scaffold]
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
