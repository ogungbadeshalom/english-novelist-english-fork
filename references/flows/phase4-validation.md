# Phase 4: Auto-Validation and Repair

**Goal**: ensure all chapters are complete and meet the word-count target, with no user involvement.

---

## Validation Flow

### 1. Initialize Validation

Read `02-writing-plan.json` and set the project `status` to `"validating"`.

> For subagent-parallel / Teams mode, first confirm each batch's status and chapter summaries have been merged back into `02-writing-plan.json` and `99-chapter-summary.md` (merge them first if not), then run a seam check on each batch boundary.

### 2. Check Chapter by Chapter

For each chapter, run these checks:

1. **File existence**: check that the file at `filePath` exists
2. **Word count**: batch-check using the script (`{skillBaseDir}` is the skill's installation root; see [shared-infrastructure.md](shared-infrastructure.md)):
   ```bash
   python {skillBaseDir}/scripts/check_chapter_wordcount.py --all <project-folder-path> --json
   ```
   Exit codes: 0=all pass, 1=some fail, 2=error. Read each chapter's `word_count` and `status` from the `results[]` of the `--json` output
3. **Update JSON**: write `wordCount` and `wordCountPass` into the corresponding chapter records

### 3. Summarize Results

- **All pass** (all chapter files exist and `wordCountPass == true`) → set the project `status` to `"completed"` and go to step 5
- **Some fail** → go to step 4

### 4. Auto-Repair (up to 3 rounds)

For each failing chapter:

1. Set `status` to `"failed"`, increment `retryCount` by 1
2. Return to Phase 3 and run the per-chapter flow on it (pre-write analysis → writing → polish → wrap-up)
3. After rewriting, re-check the word count
4. Update `02-writing-plan.json`

Loop rules:
- run at most **3** validation-repair cycles
- chapters that still fail after 3 tries keep their record but don't block the flow
- set the project `status` to `"completed"` once all repairs are done

### 5. Completion Report

Show the user the writing-completion summary:

```
📊 [novel title] writing complete

Total chapters: [X]
Total words: [X]
Completion rate: [X]%

Per-chapter status:
✅ Chapter 1: [title] ([X] words)
✅ Chapter 2: [title] ([X] words)
...

Project folder: ./english-novelist/[timestamp]-[title]/
```

If any chapter failed (still failing after 3 rewrites), flag it in the report:
```
⚠️ Chapter X: word count short ([actual]/1500), retried 3 times
```