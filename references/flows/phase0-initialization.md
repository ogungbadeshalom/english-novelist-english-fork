# Phase 0: Initialization and Preference Loading

**Run first every time the skill is triggered:**

## 1. Load User Preferences

Check whether `user-preferences.json` exists.
- If it exists → load the preference data; use it for option ordering, recommendation marking, and a personalized welcome.
- If it does not exist → use defaults; the file is created automatically after the first interaction.

See → [shared-infrastructure.md](shared-infrastructure.md) for the preference data structure and update rules.

## 2. Quick-Start Detection

Analyze whether the user's first input already contains rich creation details (genre, protagonist, core conflict, and other key elements).

- If the information is sufficient → show the extracted details and offer three options:
  - "Yes, start planning directly" → skip the Q&A and go to Phase 2
  - "Show the extracted info so I can confirm/edit first" → show the configuration for confirmation, then proceed to planning
  - "No, I still want to go through the Q&A" → enter the Layer 1 Q&A
- If the information is insufficient → go straight into the Layer 1 Q&A

## 3. Personalized Welcome

(When preference data exists:)

> "Welcome back! Based on your previous writing habits, I've made some recommendations for you (options marked with ⭐)."

## 4. Interrupted-Resume Detection

Scan the project folders under `./english-novelist/`:

- Look for projects that contain a `02-writing-plan.json` whose `status` is `"in_progress"` or `"validating"`
- If an unfinished project is found:
  - Show the project details: novel title, completion progress (X/Y chapters done)
  - Offer options:
    - "Resume last work" → go straight to Phase 3 and continue from the interrupted chapter
    - "Start a new work" → enter the Layer 1 Q&A
- If none is found → proceed normally to quick-start detection or the Layer 1 Q&A