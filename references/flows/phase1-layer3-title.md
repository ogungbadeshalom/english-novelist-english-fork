# Phase 1 · Layer 3: Title Generation

> This layer runs after Layer 1 (core positioning) and Layer 2 (deep customization) are complete.
> The AI generates candidate titles from the collected creative elements, per [title-guide.md](../guides/title-guide.md); once the user selects or customizes a title, we move on to Phase 2.

---

## Step 1: Analyze the Creative Elements

On entering this layer, first extract the following key elements from the information gathered in Layer 1 and Layer 2:

- **Genre**: taken from the Q1 record (Mystery, Romance, Fantasy, Sci-Fi, Historical, Urban, Thriller, etc.)
- **Core conflict**: taken from the Q3 record
- **Protagonist traits**: taken from the Q2 record (identity, personality, goal)
- **Core theme**: taken from the "core theme" record in Layer 2
- **Atmosphere / tone**: taken from the "tone" record in Layer 2

Based on the genre, match the "genre-to-style mapping" table in [title-guide.md](../guides/title-guide.md) to decide the title-style direction.

---

## Step 2: Generate Candidate Titles

Following the matched style rules, apply the "title-crafting techniques" in [title-guide.md](../guides/title-guide.md) to generate candidate titles:

- **Simple / single-genre stories**: generate **3** candidates
- **Complex / cross-genre stories**: generate **5** candidates
- Each candidate must use a **different** technique to avoid stylistic sameness

Each title carries a one-line note:
- which technique it uses
- why it fits this story

---

## Step 3: Present and Select

Use `AskUserQuestion` to present the candidate titles:

```
Question: Based on your story's elements, here are the candidate titles I generated. Please choose:
Options:
- [Title 1] — [technique name], [one-line note]
- [Title 2] — [technique name], [one-line note]
- [Title 3] — [technique name], [one-line note]
- Regenerate a fresh set of candidate titles
multiSelect: false
```

> The user can also type a title directly via "Other".
> When the user picks "regenerate", return to Step 2 and generate a fresh set.

### Iteration Strategy

Maintain an internal counter to track regeneration rounds. When regeneration exceeds **5 rounds**, prepend a hint before showing the candidates:

> "You've tried several rounds of selection — you can also simply type the title you have in mind below."

---

## Step 4: Confirmed the Title and Transition

Once the user confirms the final title:

### 1. Show the Confirmation

```
✅ Novel title confirmed: [title]
Next, we move into the planning phase to generate your outline and character profiles.
```

### 2. Pass the Title Along

The title is stored in the current conversation context. When the Phase 2 planning starts, read it from context and use it to:

- **Name the project directory**: `./english-novelist/{timestamp}-{title}/`
- **Write to the `novelName` field** of `02-writing-plan.json`
- **Write to the file header** of `01-outline.md`

### 3. Interrupted-Resume

The title only travels through the conversation context; it isn't persisted on its own. If the user interrupts the session after this layer but before Phase 2 starts, Phase 0 will find no project directory (because Phase 2 hasn't run), and the user will redo the Phase 1 Q&A, ultimately re-selecting the title in this layer.

---

→ Enter **Phase 2: Planning and Confirmation**, see [phase2-planning.md](phase2-planning.md)