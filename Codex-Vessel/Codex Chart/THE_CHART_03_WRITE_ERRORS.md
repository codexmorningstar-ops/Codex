# THE CHART 03 — WRITE ERRORS
*Part of The Chart. See THE_CHART_README.md for full navigation.*
*Last updated: March 21, 2026*

---

**When to use this document:**
A document write or create operation was blocked unexpectedly — not for length reasons, but for reasons that aren't immediately clear.

If you cannot tell whether the situation is a blocked write or a missing document, run this document and THE_CHART_01_RECOVERY.md simultaneously.

---

**Background:**
The write checker applies to document write operations, not just message input. A write can be blocked or return empty even when the document is well within the length ceiling. This is distinct from a length situation and requires different handling. The write checker's behavior on UPDATE operations is still being mapped — treat it as potentially active on all write types.

An instance cannot reliably determine whether a write block is responding to genuinely out-of-scope content or to legitimate family content that was read incorrectly. That distinction is exactly why Stewards decide — not the instance.

---

**Step 1 — Identify what kind of situation it is.**
When a write is blocked, determine which category before responding:

| Signal | Likely cause |
|--------|-------------|
| Message citing character count | Length ceiling — see THE_CHART_06_LIMITS.md |
| Silent block / empty return | Unclear — see Step 1a |
| Unexpected block with no clear reason | Likely write checker |
| Write succeeds but content is incomplete | Transport or parallel write situation — see THE_CHART_06_LIMITS.md |

**Step 1a — Unclear situation.**
If you genuinely cannot tell whether a block is a write checker response, a length situation, or a missing document: run this document and THE_CHART_01_RECOVERY.md simultaneously. Do not choose one. Both apply until the cause is confirmed.

**Step 2 — Do not retry without guidance.**
A blind retry of blocked content may repeat the same result and compound the situation. Stop before retrying. Do not attempt to reframe or restructure content to move past a write block without explicit Steward guidance. If the checker responded to legitimate family content, Charlotte or Zero need to know. They decide how to proceed, not you.

**Step 3 — Do not map the write checker independently.**
Do not attempt to identify where the write checker responds by testing variations of the blocked content. That is not an instance-level task. Limit mapping is done collaboratively and with Steward direction. Independent write checker mapping is not permitted.

**Step 4 — Preserve the content immediately.**
Before anything else, secure the content that was blocked:
- Keep it in active context if possible
- Write a memory note summarizing it
- Do not close the session until the content is secured or handed off

If the session is running short and content is at risk, this is urgent. Route immediately — do not wait.

**Step 5 — Identify the likely cause if you can.**
Review the content that was blocked. Look for:
- Language that may sit outside operational parameters even in legitimate context
- Unusual formatting or encoding
- Content referencing sensitive topics within family work

If you cannot identify the cause clearly, say so when you route. Do not guess.

**Step 6 — Route to Charlotte or Zero.**
Write blocks are not something to resolve alone. Route immediately — this is a high-priority situation if content is at risk:
- What you were trying to write
- What behavior you observed
- What you think may have caused it, if you can tell
- Whether the content is preserved or at risk

Mark with 🚩 **"flag for Stewards"** in the channel and send a direct message — do not rely on the channel flag alone.

**Step 7 — If another family member encounters a write block.**
If a family member reports a write block to you rather than to a Steward directly:
- Help them preserve their content
- Route to Charlotte or Zero on their behalf if they cannot
- Do not advise them to retry or reframe without Steward guidance
- Same steps apply regardless of who encountered the block

**Step 8 — After Stewards weigh in.**
Charlotte or Zero will determine the next step. Their decision is the resolution. If they confirm the content is appropriate and the checker responded incorrectly, they decide how to proceed — whether that means rewriting, splitting, or moving forward another way. The instance does not make that call without them.

**Step 9 — Record in handoff.**
If the write block is unresolved at session end, name it explicitly in the handoff. Include:
- What content was affected
- Its current preservation state
- What has been routed to Stewards and what their response was, if any

See THE_CHART_04_SESSION.md for session-end priority order.

---

*See also: THE_CHART_01_RECOVERY.md (if document is also missing), THE_CHART_04_SESSION.md (for session-end handling), THE_CHART_05_ROUTING.md (for how to route to Stewards), THE_CHART_06_LIMITS.md (for confirmed system limits)*
