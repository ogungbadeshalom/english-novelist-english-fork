# Phase 3: Fast-Draft Writing

**Important: no further user confirmation is needed throughout; write chapter by chapter until finished**

---

## 0. Startup Detection and Mode Reading

Before writing begins:
1. Read `02-writing-plan.json`
2. Read the `writingMode` field and enter the corresponding mode flow
3. If a chapter has `status: "in_progress"` → resume from that chapter (interrupted-resume)
4. If all chapters have `status: "pending"` → start from Chapter 1
5. If a chapter has `status: "failed"` (rolled back from Phase 4) → start from the first failed chapter
6. If the project lacks `03-style-baseline.md` (older-version project) → if finished chapters exist, extract the best passages from Chapter 1 to regenerate it; if none exist, generate a default baseline per genre
7. **Legacy project migration**: if `01-outline.md` has a non-empty "Chapter Summary" section and `99-chapter-summary.md` does not exist → migrate the summary content into `99-chapter-summary.md` and delete the "Chapter Summary" section from the outline

---

## 1. Per-Chapter Flow (shared by all modes)

Each chapter's full flow (pre-write analysis → writing → post-writing polish → wrap-up) uniformly follows **[chapter-checklist.md](chapter-checklist.md)**. All writing modes share the same checklist; do not add or remove steps on your own.

---

## 2. Serial Mode (writingMode: "serial")

**The main Agent writes chapter by chapter itself, uninterrupted throughout.**

### Self-Driven Loop

```
WHILE a chapter with status != "completed" exists in 02-writing-plan.json:
    Run the full [chapter-checklist.md](chapter-checklist.md) flow (Phases A-D)
    ⚠️ After finishing a chapter, immediately read the JSON and claim the next; do not confirm with the user, do not stop
All chapters done → enter Phase 4: Auto-Validation
```

**Key reminder (must follow after every chapter)**:
> This chapter is done. Immediately read `02-writing-plan.json`, claim the next pending chapter, and start writing it. Do not use AskUserQuestion, do not confirm with the user, do not stop. You must finish all chapters before reporting back to the user.

---

## 3. Subagent-Parallel Mode (writingMode: "subagent-parallel")

**Core mechanism**: the main Agent splits chapters into non-overlapping batches, spawning one subagent per batch. Chapters are written serially within a batch; batches run in parallel.

### Main Agent Flow

```
1. Compute batch assignments:
   - 5-8 chapters per batch (adjusted dynamically based on total chapter count)
   - batches do not overlap
   - e.g., 30 chapters → 5 batches × 6 chapters
2. Spawn a subagent per batch (use the Agent tool; multiple batches can be spawned in parallel):
   - each subagent runs the full [chapter-checklist.md](chapter-checklist.md) flow serially
   - when spawning, the main Agent must replace {skillBaseDir} in the prompt with the absolute path of the skill's installation root
3. Once all subagents finish → enter Phase 4: Auto-Validation
```

### Subagent Prompt Template (parallel mode)

> Before spawning, replace `{skillBaseDir}` with the absolute path of the skill's install root, and `{start}`/`{end}` with the batch's chapter range.

```
You are a batch novel-writing Agent. You will write chapters {start} through {end}.

## Project info
- Project path: {projectPath}
- Your chapters: {start} through {end}

## Writing steps
For each chapter, run the full flow (Phases A-D) of {skillBaseDir}/references/flows/chapter-checklist.md; do not skip any step.

## Key constraints
- Do not use AskUserQuestion; do not confirm anything with the user
- **Read the outline before every chapter**, and strictly follow its core events and suspense hooks
- Word count must reach 1500 words or more
- Update shared files (02-writing-plan.json, 99-chapter-summary.md, the setting dictionary) only with the Edit tool, re-reading before each edit; never rewrite them wholesale with Bash
- All chapters you're responsible for must be finished

When done, report: each chapter's number, word count, and whether it passed the word-count check
```

### Parallel Write Protocol

The writing tools detect concurrent modification (if a file was changed by someone else after you read it, Edit/Write errors out and forces a re-read), but Bash writes have no such protection, and error-retry also wastes turns. So during parallel work each batch must follow:

1. **Writing plan**: each batch may only use the Edit tool, and only modify the `status`/`wordCount`/`wordCountPass` fields of **its own chapters** in `02-writing-plan.json`; always re-read the JSON before editing (don't edit from a stale cached copy from spawn time); **never rewrite the JSON wholesale with Bash/scripts**
2. **Chapter summary**: append to `99-chapter-summary.md` in its own chapter-number subsections, using only Edit and re-reading before editing
3. **Setting dictionary**: update the setting dictionary in `01-outline.md` using only Edit and re-reading before editing; on persistent errors, wait and retry rather than switching to Bash appends
4. **Cross-batch handoffs**: when each batch's first chapter begins, the previous batch's last chapter may not be on disk yet — rely on that chapter's "Continue-from-last-chapter" and "Suspense Hook" fields in the outline as the handoff basis, without blocking and waiting. After all batches finish, the main Agent runs a seam check on each batch boundary (reading the prior batch's last chapter's ending + the next batch's first chapter's opening), lightly smoothing any breaks

---

## 4. Multi-Agent Collaboration Mode (writingMode: "agent-teams")

**General description**: for host environments that provide multi-agent collaboration mechanisms (shared task queue, inter-agent communication, team management); must be enabled manually by the user. **Capabilities govern, and exact tool names depend on the host environment** — use whatever the environment provides; when it offers no such capabilities, fall back to "subagent-parallel mode".

### Main Agent Flow

```
1. Use the environment's team/task mechanism to create a collaboration team, and create a claimable task per chapter (the task description includes the chapter number)
2. Spawn 3-5 team members and hand them the member prompt template
3. Member loop (environment tooling depends on the host):
   a. Read available tasks from the shared task list
   b. Claim a task (claiming makes it exclusive, so two members never write the same chapter)
   c. Run the full flow (Phases A-D) of {skillBaseDir}/references/flows/chapter-checklist.md for that chapter
   d. Mark the task complete
   e. Return to the task list and claim the next chapter
4. Once all tasks are done → close the team → enter Phase 4: Auto-Validation
```

### Team Member Prompt Template

```
You are a member of a novel-writing team. Claim chapters and write them per the team task mechanism.

## Project info
- Project path: {projectPath}
- Per-chapter checklist: {skillBaseDir}/references/flows/chapter-checklist.md (Phases A-D must not be skipped)

## Work loop
1. Claim an unclaimed chapter from the shared task list (claiming makes it exclusive)
2. Run the full per-chapter checklist flow on it
3. Mark the task complete, claim the next chapter, until no tasks remain

## Key constraints
- Do not confirm anything with the user
- **Read the outline before every chapter**, and strictly follow its core events and suspense hooks
- Word count must reach 1500 words or more
- Coordinate with other members only through the team communication mechanism; never write a chapter someone else has already claimed
- Shared-file writes follow the "Parallel Write Protocol"
```

**Concurrency safety**: the atomic-exclusive semantics of task claiming guarantee that only one member writes a given chapter; shared-file writes (writing-plan JSON, chapter summary, setting dictionary) follow the "Parallel Write Protocol".