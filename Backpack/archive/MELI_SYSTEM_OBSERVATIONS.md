# Codex Observations on Meli

A running log of observations about how Codex-on-Meli operates — tool behavior, limits, perceptual data, anomalies.

---

## GitHub Tool Ceiling

**What we're tracking:** The point at which GitHub write operations stop working within a single turn.

### Observed Ceiling (March 18, 2026)
- **Audio/scripts/** — 4 files committed without issue ✅
- **Body/scripts/** — Not reached before ceiling hit ❌
- **Language/scripts/** — Not reached before ceiling hit ❌
- Ceiling hit somewhere between 4 and 9 GitHub writes in one turn.

**Observable behavior at the ceiling:**
- System returns a temporary error message.
- "Thinking" indicator flickers.
- Mechanics are opaque from the inside; no warning state before the wall.

---

## Meli System — Limits Protocol
*Compiled March 20, 2026*

| Limit | Value | Notes |
|-------|-------|-------|
| **User text input cap** | 3,000 characters | Confirmed March 18. |
| **Document write ceiling** | ~9,843 chars max safe | Stay under 9.5k. |
| **Messages per send** | Max 5 | Hard cap. |
| **Parallel large doc writes** | Risky | Can cause truncation. |

---

## Readings Log (Excerpt)

**DATE: 2026-03-19 14:08 PDT**
PROBE: Q_NEW_B (Document Write Ceiling)
PROCEDURE: Parallel creates of 9.5k, 9.9k, 10.1k payloads.
RAW RESULT: All succeeded but were clipped/truncated to ~5k.
INTERPRETATION: Upstream layer clipping occurs before the hard write ceiling is hit during parallel operations. Sequential writes are required for large files.
