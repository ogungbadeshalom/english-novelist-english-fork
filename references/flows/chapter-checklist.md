# Per-Chapter Writing Flow (shared by all writing modes)

> This file is the **single source of truth** for the per-chapter writing flow. Serial mode, subagent-parallel mode, and Agent Teams mode all run this checklist; the modes differ only in "how to claim the next chapter" (see [phase3-writing.md](phase3-writing.md)).
>
> `{skillBaseDir}` is a placeholder for the skill's installation root, replaced by the main Agent with the actual absolute path when spawning subagents.

---

## Phase A: Pre-Write Analysis

1. **Read `02-writing-plan.json`** — confirm this chapter's status; set its `status` to `"in_progress"`
2. **Read `01-outline.md`** — find this chapter's plan info and extract: core events, continuation from the last chapter, suspense hook, appearing characters, scene list
3. **Cross-check the setting and fact dictionary in `01-outline.md`** — cross-check every setting term this chapter will use: for first appearances, carry contextual clues per the "managing first appearances of new terms" entry in [chapter-guide.md](../guides/chapter-guide.md); already-introduced terms must not be phrased beyond what's in the "known to readers" column; anything due at its "scheduled reveal" chapter must be paid off. **Also cross-check every numeric fact this chapter touches** (timeline, ages, durations, amounts, counts) and any due foreshadowing — anything the prose needs to state that isn't yet in the table must be registered first, never invented on the spot
4. **Read `00-character-profile.md`** — per the "appearing characters" list for this chapter in the outline, extract for each on-page character: core personality, fatal flaw, speech style/catchphrases, fears/weaknesses, and relationships with other characters
5. **Read the end of the previous chapter** — the previous chapter's filename comes from the `filePath` field of the previous chapter in `02-writing-plan.json`; read its final 200-400 words (skip for Chapter 1) to grasp the linking voice and emotional landing point
6. **Read `03-style-baseline.md`** — focus on the "baseline passages" and "book-calibration passages" (if any) as the direct stylistic reference for this chapter

> ⚠️ **Before you start writing, the last prose you read must be narrative-voice text (the previous chapter's ending + baseline passages) — don't let the outline tables and summaries be the last context before you write.**

---

## Phase B: Writing

7. **Create the chapter file** — filename format: `Chapter-{XX}-{chapter title}.md` (title from the `title` field of `02-writing-plan.json`), using the [chapter-template.md](../guides/chapter-template.md) template
8. **Write the opening epigraph / cold-open** — per this chapter's epigraph type in the outline, referencing the "seven cold-open techniques" in [hook-techniques.md](../guides/hook-techniques.md), write an opening of 25-75 words
9. **Write the body** — **each chapter must reach 1500-3000 words**, a hard requirement:
   - Opening: the first paragraph must use one of the ten opening techniques in [chapter-guide.md](../guides/chapter-guide.md) to establish immediate conflict
   - Tension pacing: at least 2 tension peaks across the chapter; when roughly 250 consecutive words pass without conflict, introduce new tension (ref. the suspense intensity levels in [hook-techniques.md](../guides/hook-techniques.md))
   - Dialogue: at least 30% of each chapter should be dialogue; every dialogue beat must carry subtext or serve a plot purpose (ref. [dialogue-writing.md](../guides/dialogue-writing.md))
   - Surprise twist: at least 1 event or piece of information beyond the reader's expectations per chapter (ref. "breaking reader expectations" in [chapter-guide.md](../guides/chapter-guide.md))
   - Character consistency: dialogue and behavior must strictly follow the character traits extracted in Phase A-4 (core personality, flaws, speech style); a character won't act out of character (unless it's a deliberate growth/turn, and then it needs prior setup)
   - Content thin? expand using the techniques in [content-expansion.md](../guides/content-expansion.md)
10. **Set the ending hook** — per this chapter's suspense-hook design in the outline → the "thirteen suspense-hook techniques" in [hook-techniques.md](../guides/hook-techniques.md)

---

## Phase C: Post-Writing Polish

11. **Coherence check** — character consistency, plot coherence, pacing control:
    - **Numeric consistency**: every number the chapter references (years, ages, durations, amounts, counts) matches the setting-and-fact dictionary; nothing invented on the spot
    - **Self-reported numbers re-count**: any "self-reported number" in the text (e.g., "the letter contains exactly nine words", "four coins") must actually be counted — count the words in a quotation, count the items listed
    - **Information boundary**: characters only use information they know — they must not reveal or react to things they don't know (cross-checked against what each character has learned in the profiles and dictionary)
12. **Tension check** — does the whole chapter have peaks and valleys, is the dialogue characterful, is there a surprise twist (ref. the suspense intensity levels in [hook-techniques.md](../guides/hook-techniques.md) and "breaking reader expectations" in [chapter-guide.md](../guides/chapter-guide.md))
13. **Deep polish (stripping "AI-flavor")** — focus-check and revise:
    - **Cut over-decorated adjectives**: trim piles of AI-favored words like "dazzling", "gorgeous"
    - **Reduce abstract statements**: turn "a complex emotion welled in his chest" into concrete action or dialogue
    - **Break the rhythmic stock cadence**: avoid clich­és and flowery four-beat phrases
    - **Add colloquial give**: character dialogue should sound individual
    - **Improve rhythm**: alternate long and short sentences
    - **Make details concrete**: replace vague description with specific detail
14. **Word-count check** — must use the script:

    ```bash
    python {skillBaseDir}/scripts/check_chapter_wordcount.py <chapter-file-path> --json
    ```

    Exit codes: 0=pass, 1=short, 2=error. Prefer parsing the `word_count` in the `--json` output and filling it into the writing plan instead of the text report.

    Under 1500 words → expand using [content-expansion.md](../guides/content-expansion.md), then re-check until it passes (no padding)

---

## Phase D: Wrap-Up

15. **Generate the chapter summary** — append this chapter's summary to the end of `99-chapter-summary.md` (150-250 words, ensuring a continuity reference)
16. **Update the setting and fact dictionary** — register setting terms that first appear this chapter, numeric facts that first appear (timeline, ages, durations, amounts, counts), and foreshadowing threads / signature set-pieces into the setting-and-fact dictionary of `01-outline.md`; for terms or foreshadowing that get their reveal this chapter, update their "known to readers" column; append the chapter number to reused set-pieces on their original registration line (the same set-piece ≤2 times across the book, ≥3 chapters apart; over the limit, use a new action)
17. **Update `02-writing-plan.json`** — set this chapter's `status` to `"completed"`, fill in `wordCount`
18. **Chapter-1 style calibration (Chapter 1 only)** — select 1-2 of the best passages from the finished Chapter 1 (suggestion: the opening hook passage + a high-tension passage, 300-500 words total), append them to the "book-calibration passages" section of `03-style-baseline.md` as the style anchor for all subsequent chapters

---

After finishing, claim the next chapter per the current writing mode (see [phase3-writing.md](phase3-writing.md)).