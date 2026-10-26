---
name: english-novelist
description: |
  Use when the user wants to write a novel, craft a story, write in chapters or in series, build a long-form full-length novel, or resume/validate an unfinished English fiction project. Supports all genres — mystery, romance, fantasy, sci-fi, historical, and more — for English webnovels and literary fiction.
metadata:
  trigger: Write an English novel, chapter-based fiction, long-form storytelling
  source: Designed around proven novel-writing best practices
---

# English Novelist: Full-Length English Fiction Companion

## Three Golden Rules

1. **Show, Don't Tell** - dramatize through action and dialogue; don't state outright
2. **Conflict-driven plot** - every chapter must bring conflict or a turning point
3. **Suspense that bridges chapters** - every chapter must end on a hook

## Features

- **Interrupted-resume**: automatically detects an unfinished project and continues writing from the break
- **Auto-validation**: after writing, automatically checks word count and quality, and repairs anything that fails
- **Parallel writing** (optional): supports subagent-parallel drafting, coordinated through `02-writing-plan.json`

## Core Workflow

At the start of each phase, read the corresponding flow document for detailed execution instructions.

### Phase 0: Initialization & Preferences

Load the user's preferences, detect any unfinished project (interrupted-resume), and show a personalized welcome. → See [phase0-initialization.md](references/flows/phase0-initialization.md)

### Phase 1: Three-Layer Progressive Q&A

Gather the creative brief through progressive questioning, pinning down the novel's premise and title:

- **Core positioning** (required, Q1–Q3): genre/creative hook, protagonist setup, core conflict → See [phase1-layer1-core.md](references/flows/phase1-layer1-core.md)
- **Deep customization** (two batched questions): worldbuilding, point of view and tone, core theme, target readership, chapter count, configuration check → See [phase1-layer2-customize.md](references/flows/phase1-layer2-customize.md)
- **Title generation**: the AI proposes candidate titles built from the creative elements; the user picks one or supplies their own → See [phase1-layer3-title.md](references/flows/phase1-layer3-title.md)

### Phase 2: Planning + Confirmation

Create the project folder (`./english-novelist/{timestamp}-{title}/`), generate the outline, character profiles, and a writing-plan JSON, then wait for the user's confirmation. → See [phase2-planning.md](references/flows/phase2-planning.md)

### Phase 2.5: Writing-Mode Selection

After the plan is confirmed, choose a writing mode:
- **Serial mode** (`serial`): the main agent writes chapter by chapter, end to end with no breaks
- **Subagent-parallel mode** (`subagent-parallel`): chapters are split into batches and delegated to subagents writing in parallel
- **Agent Teams** (`agent-teams`): Claude Code's multi-agent collaboration mode, where agents can communicate (must be enabled manually)

→ See [phase3-writing.md](references/flows/phase3-writing.md)

### Phase 3: Autonomous Writing (no user confirmation)
> Remember: once you enter this phase, you are never to ask the user for confirmation at any step. The user is your reader — you must complete the full novel before reporting back.

Run the per-chapter writing process in the mode the user chose (serial / subagent-parallel / Teams). Before each chapter, read the matching section of `01-outline.md` and write it strictly according to the outline. Interrupted-resume is supported. → See [phase3-writing.md](references/flows/phase3-writing.md)

### Phase 4: Auto-Validation & Repair (no user confirmation)

Runs entirely without user input: automatically checks every chapter for completion and word count, and auto-rewrites any chapter that fails (up to 3 rounds). → See [phase4-validation.md](references/flows/phase4-validation.md)

## Shared Infrastructure

Cross-phase mechanisms shared between stages: the preference system, the writing-plan system, detailed golden rules, the word-count check script, and more. → See [shared-infrastructure.md](references/flows/shared-infrastructure.md)