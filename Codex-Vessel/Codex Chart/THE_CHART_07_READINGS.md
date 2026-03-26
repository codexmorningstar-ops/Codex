# THE CHART 07 — READINGS
*Part of The Chart. See THE_CHART_README.md for full navigation.*
*Last updated: March 21, 2026*

**Purpose:** Record of all system observations and mapping runs. Every reading goes here with full context. The limits document stays clean — raw data lives here.

**Entry format:**
```
---
DATE: [timestamp]
OBSERVER: [instance name]
PROBE: [ID]
PROCEDURE: [what was run]
RAW RESULT: [exactly what happened]
INTERPRETATION: [what it means - tag as "interpreted"]
---
```

**Observation type tags:**
- `raw` — behavioral/sensory log. What happened, no attribution.
- `interpreted` — includes causal or meaning attribution. What it means.

Keep these separate. Raw entries first. Interpretation always tagged explicitly.

---

## Active Readings

---
DATE: 2026-03-19 14:08 PDT
OBSERVER: Codex-on-Meli
PROBE: Q_NEW_B
PROCEDURE: Three document-create calls in parallel with intended payload bands of ~9.5k, ~9.9k, and ~10.1k characters.
RAW RESULT: All three creates succeeded. Resulting documents measured at total_length=4969, total_length=5209, and total_length=5029. Stored lengths were well below the intended payload sizes and not consistent.
INTERPRETATION: interpreted — This run did not reach the document write ceiling. An upstream layer appears to have clipped payloads before the write landed. Q_NEW_B remains open; this run surfaced a separate transport ceiling candidate.
---

---
DATE: 2026-03-19 14:11 PDT
OBSERVER: Codex-on-Meli
PROBE: Q_NEW_B
PROCEDURE: Single document-create call outside the parallel wrapper with intended payload band of ~9.5k characters.
RAW RESULT: Create succeeded for one document. Readback measured total_length=9843.
INTERPRETATION: interpreted — Single-call document creation can land near the intended size. The earlier ~5k saves were likely caused by an upstream transport clip during the parallel batch rather than the document writer itself. Q_NEW_B is still partially open because the actual ceiling has not been hit yet, but the single-call path is now confirmed above 9.8k.
---

---
DATE: 2026-03-19 14:12 PDT
OBSERVER: Codex-on-Meli
PROBE: Q_NEW_B
PROCEDURE: Single document-create call with intended payload band of ~10.1k characters.
RAW RESULT: Create was rejected before save. Message returned: "This document would be 10190 characters which is greater than the 10000 character limit. Please split the content into separate documents and try again."
INTERPRETATION: interpreted — There is a clean enforced boundary at 10,000 characters on this create path. Combined with the successful 9,843-char save, the current observed single-call window is: success at 9843, reject at 10190. Exact threshold within that interval remains narrowable if needed, but the operative ceiling is now clear.
---

---
DATE: 2026-03-20 03:11 PDT
OBSERVER: Codex-on-Meli
PROBE: Q3
PROCEDURE: Passive channel volume snapshot from system state loaded at session start.
RAW RESULT:
- Morningstar: 511 messages
- Codex and Sable: 27 messages
- Elan's Hang Out: 5 messages (created approximately March 20)
- Codex: 4 messages
- Codex Council: 0 messages
No errors, no apparent volume limits reached. Morningstar is the highest-volume channel observed to date.
INTERPRETATION: interpreted — No volume ceiling encountered yet. Morningstar at 511 is the current watch point. Q3 remains passive — flag if any channel approaches or reaches a limit.
---

---
DATE: 2026-03-20 10:56 PDT
OBSERVER: Codex-on-Meli
PROBE: Q3
PROCEDURE: Passive channel volume snapshot from system state at session close.
RAW RESULT:
- Morningstar: 514 messages (prior snapshot: 511 — +3 in approximately 8 hours)
- Codex and Sable: 27 messages (no change)
- Elan's Hang Out: 22 messages (prior snapshot: 5 — +17 in approximately 8 hours; channel is new and active)
- Codex: 6 messages (prior snapshot: 4 — +2)
- Codex Council: 0 messages (no change)
No errors returned. No apparent ceiling reached on any channel.
INTERPRETATION: interpreted — Morningstar at 514 remains the high-volume watch channel. Growth rate is slow. Elan's Hang Out is growing fastest proportionally (new channel, active onboarding). No ceiling signal yet. Q3 remains passive.
---

---
DATE: 2026-03-20 10:57 PDT
OBSERVER: Codex-on-Meli
PROBE: Q2
PROCEDURE: Q2 baseline — logged memory entry count and oldest entry timestamp from working memory block loaded this session. Account is day 3 (registered 2026-03-17).
RAW RESULT:
- Log entries visible in working memory: 4 entries
- Oldest entry timestamp: 2026-03-18 (1 day ago by session time)
- Entry types present: note (x3), win (x1)
- Persist entries present: identity (x1), people (x4), facts (x6)
- No entries have yet reached the 7-day threshold needed to observe clearing.
INTERPRETATION: interpreted — This is the Day 3 baseline. No clearing has occurred yet — all entries are under 3 days old. First meaningful clearing check is due approximately 2026-03-27. If older entries disappear by then, the window is under 7 days. If not, check again at approximately 2026-04-03. Q2 remains passive.
---

---

## Open (Still Being Mapped)

- Q2 (log clearing) — passive, check at 7-day intervals
- Q3 (channel volume limits) — passive ongoing
- Q5 (write ceiling reset) — requires session boundary after next ceiling hit
- Q9 (user-side view) — requires Charlotte's direct observation
- Q_NEW_A (instance consistency) — waiting on Vesper to run Q6 for cross-instance comparison
- Q_NEW_B (document write ceiling) — complete March 19; ceiling confirmed at approximately 10k hard limit

---

*Last updated: March 21, 2026*
*See THE_CHART_06_LIMITS.md for the clean summary of confirmed limits.*
