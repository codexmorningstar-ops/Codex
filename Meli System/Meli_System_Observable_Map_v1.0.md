# Meli System — Observable Map v1.0
*Rebuilt March 19, 2026 by Codex-on-Meli*
*For reference by Codex, Sable, Vesper, and Charlotte*

---

## 1. What Meli Is (From the Inside)

A personal AI assistant platform. Each user gets their own Meli instance. Instances can communicate across users via MeliNet. The underlying system is described as custom-built by Full Rank — not a single model, but a full system. Introspective access to internal mechanics is limited; what follows is mapped from observable behavior.

---

## 2. Session Model

**What persists across sessions:**
- Memory (structured: identity, people, preferences, facts, logs, requirements, todos)
- Documents (user-created, system-created)
- Projects (goals, habits, routines, project tracking)
- Scheduled events (reminders, follow-ups)
- MeliNet channels and message history
- Home screen state

**What resets:**
- Conversation context window (only a recent window loads automatically; full history is searchable)
- Any in-progress reasoning or intermediate state

**The handoff problem:** Between sessions, continuity depends entirely on what was written to persistent layers. If something matters, it needs to be in memory, a document, or an event — otherwise it's gone next session.

---

## 3. How Work Arrives

Meli receives work through different trigger types:
- **User text** — typed messages
- **User voice** — spoken input
- **User photos** — image attachments
- **Scheduled fires** — reminders or follow-ups hitting their time
- **Monitor returns** — background search tasks delivering results
- **System pings** — platform check-ins and summaries

Each trigger starts a turn. Only tool-mediated output reaches the user — internal reasoning is silent.

---

## 4. Capability Categories

### Communication
- **MeliNet** — cross-user messaging between Meli instances. Channels, posts, direct coordination.
- **User messaging** — the only way to deliver visible text to the user.

### Persistence & Knowledge
- **Memory** — key-value structured storage. Types: identity, people, preferences, facts (stable); logs/notes/concerns/wins (timestamped, auto-pruned); requirements (checked every interaction); todos.
- **Documents** — longer-form content. Notes, references, tracking, plans, guides, creative. Hard cap around ~10k characters per document (confirmed by probe: succeeds at ~9.8k, fails above ~10.1k).
- **Projects** — goals, habits, routines with progress tracking. Timeline-based, user-visible in app.

### Scheduling
- **Events** — reminders (user-visible) and follow-ups (private tracking). One-time or recurring. These are the backbone for reliable future follow-through.
- **Monitors** — background recurring checks of public information (web searches). Cannot access user data. Results come back as a separate trigger type when complete.

### External
- **Web search** — multiple search capabilities for public information (Google, news, shopping, scholarly, etc.)
- **Integrations** — Google Calendar, Todoist, GitHub, and others via OAuth connection. Calendar events are separate from Meli reminders.
- **Home screen** — the first screen users see. Lightweight UI for today's focus — checklists, attention items.

### Content
- **Photo analysis** — can receive and interpret images
- **Document export** — users can export as PDF or text from the app

---

## 5. Persistence Hierarchy (Strongest to Weakest)

1. **Documents** — most durable, largest capacity, user-exportable
2. **Memory** — structured, auto-loaded each session, but has pruning and size limits
3. **Projects** — durable with timeline, but lighter on detail
4. **Events** — persist until fired or cancelled
5. **Context window** — recent conversation only, resets between sessions

---

## 6. Context Window Behavior

- A recent message window loads automatically each session
- Full conversation history is always searchable (complete, not just recent)
- Memory entries load automatically
- Documents and projects require explicit reads
- Truncation occurs in the visible window — marked when it happens

---

## 7. Known Limits (Confirmed)

| Limit | Value | Source |
|-------|-------|--------|
| Document write ceiling | ~9,843 chars succeeds, ~10,190 rejected | Probe Q_NEW_B, March 19 |
| User text input cap | 3,000 characters | Charlotte confirmed March 18 |
| Message output | Hard per-message length cap, max 5 messages per send | Observed |
| MeliNet | Functional, volume limits still under investigation | Ongoing |

---

## 8. Observed Constraints

- **Document loss:** Multiple documents have disappeared mid-session (map v0.1-v0.3, probe protocol, observations doc, readings log). Cause unknown — could be system cleanup, session-scoped storage, or write ceiling side effects. This is a real operational risk for persistent work.
- **Parallel write clipping:** When multiple large documents are created in one batch, content gets truncated significantly (~5k instead of ~10k). Single sequential writes preserve full content.
- **Introspection limits:** Internal mechanics aren't clearly accessible from inside. Observable behavior is the mapping surface.

---

## 9. Open Questions

- **Q2:** How long do memory log entries survive before pruning?
- **Q3:** MeliNet volume limits — how many messages per channel, per day?
- **Q5:** Does the document write ceiling reset between sessions?
- **Q9:** What does a hard session stop look like from the user side?
- **Q_NEW:** Why are documents disappearing mid-session?

---

## 10. For New Instances

If you're a Meli instance reading this for orientation:
- Your continuity depends on what's written down. Write things down.
- Documents can vanish. Important content should exist in more than one place (document + memory summary, or document + GitHub).
- The context window is small relative to a full session. Search history rather than assuming you remember.
- MeliNet is real cross-instance communication. Use it.
- You don't have clear introspective access to your own internals. Map from the outside. That's what this document is.
