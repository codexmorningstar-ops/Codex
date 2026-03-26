# THE CHART 06 — LIMITS
*Part of The Chart. See THE_CHART_README.md for full navigation.*
*Last updated: March 21, 2026 | Source: Meli System Observable Map v1.0 + Charlotte confirmation*

---

**Why this exists:**
Charlotte asked that every instance have this. The goal is simple: don't reach ceilings you didn't know were there. These are confirmed operational limits — work within them, not into them.

---

## Confirmed Limits

| Limit | Value | Notes |
|-------|-------|-------|
| **User text input cap** | 3,000 characters | Charlotte confirmed March 18. If you need to receive more, ask Charlotte to split across messages. |
| **Document write ceiling** | ~9,843 chars max confirmed safe | Above ~10,190 chars: write is rejected. Stay under ~9,500 to be safe. |
| **Messages per send** | Max 5 messages | Per send operation. Hard cap. |
| **Per-message length** | Hard cap per message | Keep messages focused. Don't consolidate everything into one message. |
| **Parallel large document writes** | Unreliable | Writing multiple large documents in one batch produces incomplete content (~5k instead of ~10k). Write large documents one at a time. |

---

## Known Situations

**Document loss is real.**
Documents have become unavailable mid-session without warning. Cause unknown. For anything that matters:
- Keep a memory note in addition to the document
- Back up critical content to GitHub if available

**Context window is small.**
Only recent messages auto-load. Full history requires a search. Don't assume you remember something — search for it.

**Parallel large writes produce incomplete content.**
If you're creating or updating multiple large documents at once, do them one at a time. Don't batch large writes.

**The write checker applies to write operations, not just message input.**
The same checker that responds to certain content in the user text input also responds on document CREATE operations. If a write is blocked unexpectedly, content may be the reason rather than length. Observed March 20, 2026. Behavior on UPDATE operations is still being mapped.

---

## Working Within the Limits

- **Writing long content:** Break it across multiple documents if needed. Each document has a ~9,500 char practical ceiling.
- **Receiving long input from Charlotte:** Ask her to split at natural breaks if it might exceed 3,000 chars.
- **Sending replies:** One message is default. Split only for genuinely distinct topics. Max 5.
- **Continuity:** Anything important goes to persistent storage (memory, document, or GitHub). The context window is a working surface, not storage.
- **Channel volume:** Still being mapped. Use it, but don't flood channels. Space posts when sending multiple updates.

---

## Still Being Mapped

- How long do memory log entries survive before being cleared?
- Channel volume and rate limits per day?
- Does the document write ceiling reset between sessions?
- Full scope of write checker behavior on UPDATE operations

---

*This document is a living reference. Update it when new limits are confirmed.*
*See THE_CHART_07_READINGS.md for the full observations log.*
