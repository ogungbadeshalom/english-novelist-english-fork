# Phase 2: Planning + Second Confirmation

> **Prerequisite**: This phase uses the novel title the user confirmed in Phase 1 Layer 3. The title comes from the conversation context and is used to name the project directory, fill the outline file header, and populate the writing-plan JSON.

Execute the following steps:

1. **Create the project folder**: `./english-novelist/{YYYYMMDD-HHmmss}-{Layer 3 confirmed title}/` (relative to the current working directory, using the title the user selected in Layer 3)
2. **Generate character profiles**: create `00-character-profile.md` using the [character-template.md](../guides/character-template.md) template, referencing [character-building.md](../guides/character-building.md) to build profiles for the protagonist, antagonist, and supporting characters. **Character profiles must be detailed**: each character's core personality, fatal flaw, speech style/catchphrases, fears/weaknesses, and backstory must be specific enough to guide writing directly
3. **Generate the outline**: create `01-outline.md` using the [outline-template.md](../guides/outline-template.md) template, referencing [plot-structures.md](../guides/plot-structures.md) to fill in a complete chapter plan. **The outline must be character-driven**: reference `00-character-profile.md` to ensure the plot serves each character's growth arc
3.5. **Generate the style baseline**: create `03-style-baseline.md` with four parts:
   - **Style fingerprint**: dialogue-ratio target (default 35%-45%), sentence rhythm (mostly short sentences, action beats ≤10 words), paragraph breathing, narrative distance, and description tendency, generated from Layer 2's tone / style references / target readers
   - **Baseline passages**: 2 sample prose passages that show the target style (roughly 250-400 words each). If the user supplied a favorite passage during the Q&A, use it directly
   - **Negative checklist**: cite the "AI-flavor stripping" entry in [chapter-guide.md](../guides/chapter-guide.md)
   - **Book-calibration passages**: (initially empty; backfilled by Phase 3 once Chapter 1 is done)
3.7. **Create the chapter-summary file**: create an empty `99-chapter-summary.md` with the header `# Chapter Summary` plus one line stating "append a 150-250-word summary after each chapter for continuity reference". At the close of each chapter, append a summary here (see Phase D of [chapter-checklist.md](chapter-checklist.md)); the outline file stays a pure planning document and doesn't bloat as you progress
4. **Generate the writing plan**: create `02-writing-plan.json`, populated from the outline, with the following structure:
   ```json
   {
     "version": 1,
     "novelName": "[novel title]",
     "projectPath": "./english-novelist/{timestamp}-[novel title]",
     "totalChapters": [chapter count],
     "minWordsPerChapter": 1500,
     "createdAt": "[ISO time]",
     "updatedAt": "[ISO time]",
     "status": "planning",
     "writingMode": "[serial|subagent-parallel|agent-teams]",
     "chapters": [
       {
         "chapterNumber": 1,
         "title": "[chapter title]",
         "filePath": "Chapter-01-[chapter title].md",
         "status": "pending",
         "wordCount": null,
         "wordCountPass": null,
         "retryCount": 0
       }
     ]
   }
   ```

Once done, take the following two steps:

**1. Show the planning summary and request confirmation**

Show the user a planning summary (novel title, total chapter count, target word count, main characters, style-baseline sources) and request confirmation.

**2. Writing-mode selection** (after the user confirms the plan)

Use `AskUserQuestion`:

```
Question: Choose a writing mode
Options:
- Serial (the main Agent writes chapter by chapter itself, uninterrupted — best for short and medium works)
- Subagent-parallel (spawns subagents in batches to write in parallel, outline-driven coherence — best for medium and long works)
- Agent Teams (multi-agent collaboration; agents can communicate — must be enabled manually)
```

After the user chooses:
- update the `writingMode` field of `02-writing-plan.json`
- set `status` to `"in_progress"`
- enter Phase 3: Fast-Draft Writing → see [phase3-writing.md](phase3-writing.md)