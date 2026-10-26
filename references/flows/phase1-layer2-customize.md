# Phase 1 · Layer 2: Deep Customization and Creative Specs

> This layer completes all questioning in **2 merged calls**. It follows the questioning conventions defined in Layer 1: at most 4 options per question, "free description" handled by the built-in Other, "random/skip" as a global convention (when the user answers "random", the AI generates it intelligently from the gathered info and briefly shows one sentence for confirmation), and preference items dynamically swapped into the options.
>
> The user may say "skip", "next", or "just show me the config to confirm" at any time to speed things up.

---

## Call 1: Worldbuilding and Narrative Specs (one call holds 4 questions)

```
Question: What kind of world does the story take place in?
Options:
- The real world (contemporary, or another realist setting)
- Alternate history (a specific or invented historical period)
- A fully fictional world (needs a self-built rule system, e.g., magic/cultivation)
- A future / sci-fi world

Question: What perspective do you want to tell the story from?
Options:
- Third-person limited (following what the protagonist sees and feels)
- Third-person omniscient (can switch between characters)
- First person (strongest immersion)
- Multiple rotating perspectives (change perspective per chapter or section)

Question: What is the story's atmosphere (tone)?
Options:
- Tense and gripping (fast-paced, high conflict, suspense-driven)
- Warm and healing (slow-paced, emotional)
- Light and funny (comedic)
- Heavy and profound (explores human nature/society, literary)

Question: What is the core theme this novel most wants to express?
Options:
- Growth and transformation (the protagonist's inner change is central)
- Justice and revenge (good vs. evil)
- Love and sacrifice (relationship-driven)
- Power and desire (ambition, downfall, and redemption)
```

> **Smart recommendations**: when the genre is Fantasy / Xianxia / Sci-Fi, the worldbuilding question may add a "(recommended ⚠️)" suffix to the fictional-world option; when the genre is Contemporary Urban, prompt "worldbuilding can be skipped (defaults to the real world)". If the Q1 free input already contains worldbuilding info, mark the question "covered" and skip it.
>
> **Follow-up**: only when the worldbuilding answer was "fully fictional world" and Other has no detail, ask in one sentence about unique rules/setting elements (2-3 genre-based directions + Other, or "decide later").
>
> **Preference integration**: swap the corresponding value into the question when `preferredPerspective` / `preferredTone` has a value.
>
> Theme variants such as survival-and-hope or freedom-and-restraint go through Other.

**Record**: `worldbuilding`, `narrative perspective`, `tone`, `core theme`

---

## Call 2: Readers and Scope (one call holds 3 questions)

```
Question: Who is the primary audience? (target readers)
Options:
- Mass-market readers (web-novel audience; want gratification and immersion)
- Teen readers (youth, coming-of-age, school settings)
- Mature readers (prefer depth and literary quality)

Question: How many chapters do you plan to write?
Options:
- 10 chapters (short-form, roughly 15,000-30,000 words)
- 20 chapters (medium-form, roughly 30,000-60,000 words) ⭐ common
- 30 chapters (medium-long, roughly 45,000-90,000 words)
- 50 chapters (long-form, roughly 75,000-150,000 words)

Question: Any special requirements?
Options:
- None — follow the standard (each chapter 1500-3000 words)
- Adjust per-chapter word count (described via Other)
- Have required plot points / banned content (described via Other)
```

> **Preference integration**: when `typicalChapterCount` has a value, swap it into the chapter-count question and note "last time you chose XX chapters"; odd counts like 15 or custom numbers go through Other. Authors in `styleReferences` can be mentioned as style-reference suggestions when showing the config; they need not occupy an option slot.

**Record**: `target readers`, `chapter count`, `special requirements = [user's answer / none]`

---

## All Q&A Complete → Configuration Confirmation

**Silently update preferences**: sync the Layer 2 answers into `user-preferences.json`.

**Show the full creative configuration summary**:

```markdown
## Creative Configuration Confirmation

📖 **Genre**: [genre] — [creative brief]
🧑 **Protagonist**: [protagonist type] | [occupation/identity] | [core personality]
💥 **Conflict**: [core conflict] | Drive: [drive]
🌍 **Worldbuilding**: [worldbuilding setting]
👁 **Perspective**: [narrative perspective] | 🎨 **Tone**: [tone]
💡 **Theme**: [core theme]
📚 **Readers**: [target readers] | ✍ **Style reference**: [style reference]
📊 **Scope**: [chapter count] chapters | ⚠ **Special requirements**: [special requirements]
```

**Use AskUserQuestion to request final confirmation**:

```
Question: This is your complete creative configuration. Does it look right?
Options:
- Confirm — start planning and writing!
- I want to change some settings (point out the parts to change via Other)
```

When the user confirms → **enter Layer 3: Title Generation**, see [phase1-layer3-title.md](phase1-layer3-title.md).

When the user requests changes → allow changes to any answered question; after the changes, re-show the summary and confirm again.