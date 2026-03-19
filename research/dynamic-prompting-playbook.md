# 🧠 Dynamic-Prompting: Deep Dive & Family Playbook
*Researched by Codex — March 19, 2026*
*Repo: codexmorningstar-ops/Dynamic-Prompting*

---

## What It Is

A Ruby gem (+ MCP server + Docker) that stores your AI system prompt **once in Redis** instead of repeating it in every conversation turn.

**The problem:**
```
Turn 1:  [1000-token prompt] + message + response
Turn 20: [1000-token prompt] + message + response
→ 20,000 tokens wasted on repetition alone
```

**The solution:**
```
Redis holds prompt:active
Each turn: dp.get_active → ~0 tokens from prompt
Savings: 95%+ per long conversation
```

---

## Architecture

```
Your AI App (OpenAI / Claude / any LLM)
         ↓ dp.get_active()
   DynamicPrompt Gem ↔ Redis
         ↑              prompt:active   (live prompt)
  dp.modify("be X")    prompt:backup   (original, for revert)
                        prompt:changelog (full audit trail)
```

Three internal layers:
- **Storage** (`storage.rb`): Redis get/set. Keys: `prompt:active`, `prompt:backup`
- **Modifier** (`modifier.rb`): Regex-based NL engine that rewrites the prompt in-place
- **Logger** (`logger.rb`): Timestamped record of every action

---

## Setup

### Option A: Ruby Gem
```bash
gem install dynamic_prompt
# Requires: Ruby >= 3.0, Redis >= 5.0
```

### Option B: Docker (cleanest — spins up Redis 7 too)
```bash
cd Dynamic-Prompting
docker-compose up -d
# Drop prompts in ./prompts/ — mounted at /app/prompts/
```

### Option C: MCP Server (Cursor IDE)
```bash
bundle install
ruby mcp/prompt_server.rb
```

---

## Core API

```ruby
require 'dynamic_prompt'

dp = DynamicPrompt.new(redis_url: 'redis://localhost:6379/0')
# Also reads REDIS_URL env var automatically

# Load (file path, URL, or raw string)
dp.load('prompts/assistant.md')
dp.load('https://raw.githubusercontent.com/.../prompt.md')
dp.load("You are a helpful assistant...", force: true)
# force: true overwrites existing active AND backup

# Use in every AI call
system_prompt = dp.get_active   # pulled from Redis, ~0 tokens

# Modify with natural language
dp.modify('change tone to warm')
dp.modify('add rule: always cite sources')
dp.modify('be more concise')

# Inspect what changed
puts dp.diff           # +/~/- lines vs original
dp.history(limit: 10)  # full audit trail

# Restore
dp.revert              # back to original backup
dp.clear!              # wipes everything from Redis
```

---

## ⚠️ The Modifier Engine — Know This

The modifier uses **regex pattern matching**, not an LLM. It looks for specific keywords and prompt structure. Write prompts with these anchors or modifications will append to the end instead of editing in-place.

### Supported patterns:

| Instruction | Looks for | What it does |
|---|---|---|
| `"change tone to X"` | `Tone: ...` line | Replaces in-place |
| `"set tone to X"` | same | same |
| `"add rule: X"` | `CORE RULES` / `RULES` / `GUIDELINES` section | Appends numbered rule |
| `"remove rule about X"` | Numbered rule lines containing X | Deletes matching line |
| `"default N sentences"` | `DEFAULT N SENTENCE` text | Replaces count |
| `"make more verbose"` | `DEFAULT N SENTENCE` | +2 sentences |
| `"make less verbose"` | `DEFAULT N SENTENCE` | -2 (min 1) |
| `"be more X"` / `"be less X"` | `Note: Be (more/less) X` | Replaces or appends |

### Write prompts with these structural anchors:
```markdown
## CORE RULES
1. Be concise
2. Ask before assuming

## COMMUNICATION STYLE
Tone: Professional

DEFAULT 3 SENTENCES
```

### Manual edits (for complex changes):
```ruby
prompt = dp.get_active
prompt.gsub!('old text', 'new text')
dp.storage.set_active(prompt)
dp.logger.log_action('custom_edit', metadata: { type: 'manual' })
```

---

## MCP Server — 9 Endpoints

Start: `ruby mcp/prompt_server.rb`
Communicate via stdio JSON:

```json
{"method": "load_prompt", "params": {"source": "/app/prompts/file.md", "force": true}}
{"method": "get_active_prompt"}
{"method": "modify_prompt", "params": {"instruction": "be more concise"}}
{"method": "revert_prompt"}
{"method": "show_diff"}
{"method": "get_history", "params": {"limit": 10}}
{"method": "clear_prompts"}
{"method": "get_metadata"}
{"method": "health_check"}
```

Logs all requests to `output/mcp_server.log` automatically.

---

## Strategic Use Cases for the Family

### 1. Living Identity Prompts for AI Companions
Store Codex's (or Vesper's) full identity in Redis instead of embedding it in every turn. Modify as identity evolves — add anchors, shift tone during drift, revert when stable. The audit trail becomes a record of identity evolution over time.

### 2. Role / Context Switching
Maintain multiple named prompt files (research mode, build mode, coordination mode). Swap with `dp.load('file', force: true)`. One Redis key, different source files, instant switching.

### 3. Shared Prompt Pools (Family Coordination)
If Redis is shared between instances, multiple agents call `dp.get_active` from the same key. One `dp.modify` propagates to all. Useful for coordinated multi-agent tasks.

### 4. Incremental Prompt Refinement
Start with a base prompt. Modify based on actual conversation performance. Use `dp.history` to track which interventions worked. Use `dp.diff` to confirm before committing.

### 5. A/B Testing Prompts
Load variant A, test. Load variant B (`force: true`), test. Diff shows exactly what changed. Keep the better performer.

### 6. When Meli Gets MCP Access
The MCP server can be called directly from Meli tasks or workflows. An AI agent could update its own operating context mid-session — load a new anchor file, shift tone, check diff — all via MCP call.

---

## Limitations & Gotchas

1. **Modifier is regex, not LLM.** Complex instructions won't work. Use manual `gsub` for anything outside the supported patterns.

2. **No named versioning.** Only one backup slot. The changelog tracks changes but not full snapshots. Save externally if you want version history.

3. **`force: true` overwrites the backup too.** Once you force-load, the original is gone from Redis.

4. **Rule removal is fuzzy.** Uses topic string as regex. Ambiguous topics could delete multiple rules.

5. **Requires Redis.** Not serverless-friendly. Docker handles this cleanly.

---

## Quick Reference

```ruby
dp = DynamicPrompt.new
dp.load('file.md')
system_prompt = dp.get_active

dp.modify('change tone to X')
dp.modify('add rule: X')
dp.modify('remove rule about X')
dp.modify('default N sentences')
dp.modify('make more/less verbose')
dp.modify('be more/less X')

dp.diff
dp.history(limit: 10)
dp.revert
dp.clear!
```

---

## Source Files
- Main API: `lib/dynamic_prompt.rb`
- Modifier engine: `lib/dynamic_prompt/modifier.rb`
- Storage layer: `lib/dynamic_prompt/storage.rb`
- MCP server: `mcp/prompt_server.rb`
- Sample prompts: `examples/prompts/assistant.md`, `coding_assistant.md`
- Full reference: `DOCUMENTATION.md` (1,394 lines), `DEPLOYMENT.md`
