# Shared Infrastructure

This file defines the mechanisms and rules shared across phases.

---

## The Three Golden Rules

1. **Show Don't Tell** — render through action and dialogue; don't state things directly
2. **Conflict-Driven Plot** — every chapter must contain conflict or a turning point
3. **End-of-Chapter Hook** — every chapter must end on a hook that bridges to the next

---

## User Preference System

### Storage File

`user-preferences.json` (at the repository root; auto-created on first use)

### Data Structure

```json
{
  "version": 1,
  "updatedAt": "2026-04-12",
  "preferences": {
    "favoriteGenres": [],
    "preferredProtagonist": "",
    "preferredPerspective": "",
    "preferredTone": "",
    "typicalChapterCount": null,
    "styleReferences": [],
    "dislikes": [],
    "creationHistory": []
  }
}
```

### Preference Update Rules

| Timing | Behavior |
|------|------|
| Every Q&A layer completed | Silently sync that layer's answers into the preference file (add/update, don't delete history) |
| User says "remember my preferences" | Save all current configuration into preferences |
| User says "forget XX preference" | Clear the preference for the specified dimension |
| User says "reset preferences" | Clear all preference data |
| A long-form work is completed | Append the work's info to `creationHistory` |

### How Preferences Affect Interaction

1. **Startup welcome**: when preferences exist, show "Welcome back!" + a personalized prompt
2. **Option ordering**: in Q1, rank `favoriteGenres` matches ahead of others
3. **Usage marking**: in the tone question (Layer 2, call 1) and the chapter-count question (Layer 2, call 2), mark the matching option with ⭐ ("your usual" / "last selection")
4. **Needs reporting**: give personalized suggestions informed by preferences (e.g., "you've liked Mystery + third-person limited; want to try rotating perspectives this time?")
5. **Random generation**: where possible, randomize from within the preference range to keep consistency
6. **Style-reference follow-up**: prioritize recommending authors from `styleReferences`

### Error Recovery

- **Roll back changes**: the user can say "ask XX again" or "change XX" at any time; the AI rolls back to the given question and asks anew
- **Mid-way checkpoint**: auto-save via `02-writing-plan.json`; the next time the skill triggers, Phase 0 auto-detects unfinished projects and asks "Continue [Title]?"
- **Corrupt preference file**: on JSON parse failure, ignore preferences and use defaults, and repair the file in the background

---

## Title Passing Mechanism

### How It's Passed

The title travels across phases **through the conversation context**; it isn't persisted to a file on its own.

**Passing chain**:
1. Phase 1 Layer 3: user selects/confirms the title → title is stored in the conversation context
2. Phase 2: read the title from context → write it into the project directory name, `02-writing-plan.json`, and `01-outline.md`

### Interrupted-Resume

If the session is interrupted after Layer 3 but before Phase 2 starts:
- Phase 0 finds no project directory (because Phase 2 hasn't run)
- the user re-enters Layer 3 to re-select the title (title selection is quick, so the re-selection cost is acceptable)

## Writing-Plan System

### Storage File

`02-writing-plan.json` (inside the project folder, created in Phase 2)

### Purpose

- **Progress tracking**: records each chapter's writing status (pending/in_progress/completed/failed)
- **Writing mode**: records the user's chosen writing mode (serial/subagent-parallel/agent-teams)
- **Interrupted-resume**: Phase 0 reads the JSON to detect unfinished projects and resume from the break point
- **Validation basis**: Phase 4 validates chapter completion and word counts against the JSON
- **Parallel coordination** (optional): during multi-agent parallel writing, JSON status avoids conflicts

### Relationship with the Outline

- `01-outline.md`: chapter plan (core events, suspense hooks, continuation from the last chapter, appearing characters, scene lists) + setting dictionary (tracking first appearances and reveals of setting terms); a pure planning document that doesn't bloat as you progress
- `99-chapter-summary.md`: the 150-250-word summary appended per chapter (continuity reference), written at each chapter's close
- `02-writing-plan.json`: chapter status, word count, retry count, writing mode (machine-readable progress tracking)
- Phase 3 must read the corresponding chapter's plan info from `01-outline.md` before writing each chapter, as the writing basis
- The two correspond strictly: the JSON's `chapterNumber` and `title` must match the chapter plan in the outline

### JSON Corruption Handling

- On JSON parse failure: prompt the user, try to infer completion progress from `99-chapter-summary.md`
- On lost chapter status: rebuild status from file existence and the word-count script

---

## Word-Count Check Script

Use `{skillBaseDir}/scripts/check_chapter_wordcount.py` to check chapter word counts. `{skillBaseDir}` refers to the skill's installation root where SKILL.md lives (e.g., `~/.claude/skills/english-novelist`) — the script isn't inside the user's project, so **it must be called with the absolute path to the skill install directory**; never use a relative path like `scripts/...` (that only exists in the skill's source tree, and the user's project can't resolve it).

```bash
# Check a single chapter (--json outputs machine-readable results, incl. word_count and pass status)
python {skillBaseDir}/scripts/check_chapter_wordcount.py ./english-novelist/<project-folder>/Chapter-01.md --json

# Check all chapters (sorted numerically by chapter number, so Chapter 10 won't precede Chapter 2)
python {skillBaseDir}/scripts/check_chapter_wordcount.py --all ./english-novelist/<project-folder>/ --json

# Custom minimum word count
python {skillBaseDir}/scripts/check_chapter_wordcount.py ./english-novelist/<project-folder>/Chapter-01.md 2000 --json
```

### Exit Codes

| Exit code | Meaning |
|-------|------|
| 0 | All pass |
| 1 | Some chapters fail |
| 2 | File/directory error |

The Agent should prefer `--json` + exit code to judge the result: `results[].word_count` can go straight into the `wordCount` field of `02-writing-plan.json`, with no need to parse the text report.

### Use Cases

| Phase | Purpose |
|------|------|
| Phase 3 (per-chapter writing) | after writing, check a single chapter's word count; any chapter under 1500 words must be expanded |
| Phase 4 (auto-validation) | batch-check all chapters' word counts; failing chapters are auto-rewritten |

Chapters under 1500 words must be expanded using the techniques in [content-expansion.md](../guides/content-expansion.md).