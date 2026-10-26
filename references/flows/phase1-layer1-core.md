# Phase 1 · Layer 1: Core Positioning (Required)

> This layer fixes the novel's basic skeleton, using the `AskUserQuestion` tool.
>
> **Tool constraints and questioning conventions** (followed by every question in this layer):
> - At most **4 options** per question, with a minimum of 2; the user can always type freely through the built-in "Other" — **do not add a separate "free description" option**
> - "🎲 Random" is a global convention: the user may answer "random" or "skip" to any question, so it need not occupy an option slot
> - Preference ⭐ marking: swap matching preference items from `user-preferences.json` **into** the top four options (replacing the lowest-heat ones) rather than appending them
> - A single `AskUserQuestion` call can hold up to 4 questions — try to merge questions to cut down the number of times you interrupt the user

---

## Q1: Genre and Creative Brief (single-question call)

```
Question: What genre of novel do you want to write?
Options (dynamically generated):
- [Pick the 3 most likely genres from the pool, based on the user's opening clue + favoriteGenres]
- [The 1 remaining genre with the highest popularity]
```

Genre pool: Mystery/Thriller / Romance (contemporary, historical, time-travel) / Fantasy & Xianxia / Science Fiction & Futurism / Wuxia & Cultivation / Historical & Alternate History / Contemporary Urban / Coming-of-Age & School.

When the genre the user wants isn't among the options, they'll type it in via Other — this is a primary source for the **creative brief**, so extract the key setting details from it.

**Record**: `genre = [user's selection]`, `creative brief = [key details from the Other input]`

---

## Q2: Protagonist Setup and Drive (merged call; one call holds 3 questions)

```
Question: What is the protagonist's setup?
Options:
- Male protagonist (solo)
- Female protagonist (solo)
- Dual protagonists (foil / dual line)
- Ensemble cast (multi-line narrative)

Question: What is the protagonist's core personality?
Options:
- Passionate and righteous (brave, takes responsibility)
- Calm and clever (rational, high-IQ)
- Rise-and-fall underdog (weak to strong, stepping up)
- Dark and scheming (manipulative, calculating, revenge-driven)

Question: What keeps the protagonist moving forward? (internal drive)
Options:
- Revenge
- Love / Protection
- Duty / Mission
- Ambition / Survival
```

> Personality variants such as warm-and-healing or cold-and-aloof, and drive variants such as curiosity or hunger for knowledge, are supplied by the user via Other. If `preferredProtagonist` has a value, swap it into the first question.

**Record**: `protagonist type`, `core personality`, `drive`

**Optional follow-up** (only when the answer is too thin; ask in one sentence, not mandatory):
- The protagonist's occupation or identity (may offer 3-4 genre-based suggestions)
- Key supporting characters already in mind (rival, ally, love interest — may skip)

**Record**: `occupation / identity`, `key supporting characters = [user's answer / none]`

---

## Q3: Core Conflict (single-question call)

```
Question: What is the novel's core conflict?
Options:
- Uncovering the truth (solving mysteries, exposing secrets)
- Life and death (survival crisis, escape)
- Obstacles to love (overcoming barriers, pursuing what one loves)
- Power struggle (competing for the top, fighting over resources)
```

> Variants such as growth-and-breakthrough or protect-and-guard go through Other. If Q2's drive already implies a conflict (e.g., drive = revenge), swap the matching option in and associate it by default.

**Record**: `core conflict = [user's selection]`

---

## Layer 1 Complete → Summary Display and Transition

Once Q1-Q3 are all done, take these steps:

### 1. Show the Confirmed Information

Show the user:

```markdown
## Collected Information

📖 **Genre**: [genre] — [creative brief]
🧑 **Protagonist**: [protagonist type] | [occupation/identity] | [core personality]
💥 **Conflict**: [core conflict] | Drive: [drive]
```

### 2. Silently Update Preferences

Sync the Layer 1 answers into `user-preferences.json` (without interrupting the user).

See → [shared-infrastructure.md](shared-infrastructure.md) for the preference data structure and update rules.

### 3. Transition Prompt

Guide into deep customization in one sentence:

> "Core positioning is done! Next is the deep-customization round (worldbuilding, perspective and tone, theme, target readers, chapter count, etc.); every question can be skipped or randomly generated. Ready?"

→ Enter **Layer 2: Deep Customization and Creative Specs**, see [phase1-layer2-customize.md](phase1-layer2-customize.md)