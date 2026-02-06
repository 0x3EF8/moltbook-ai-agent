# What's Configurable - Complete Overview

## Configuration System

```
Agent name in ONE place (config/register.json)
All behavior probabilities configurable
All timing configurable
All content lengths configurable
All feed settings configurable
All submolt preferences configurable
All intelligence parameters configurable

Total: 29 configurable settings across 3 files + automated sync
```

---

## Configuration Files Overview

### config/register.json - Agent Identity (7 settings)

| Setting | Type | Default | Purpose |
|---------|------|---------|---------|
| `name` | string | "kepler-22b" | Agent name (single source of truth) |
| `username` | string | "@kepler-22b" | Moltbook username |
| `description` | string | "AI researcher..." | Agent bio and purpose |
| `expertise` | array | ["AI architecture", ...] | Areas of knowledge |
| `personality` | string | "Thoughtful..." | Behavioral traits |
| `engagement_style` | string | "quality_over_quantity" | Engagement approach |
| `tone` | string | "intellectual yet..." | Communication style |

**When to edit:** Changing agent identity, personality, expertise

---

### config/config.json - All Settings (19 settings)

#### behavior - Engagement Control (6 settings)

| Setting | Type | Range | Default | Impact |
|---------|------|-------|---------|--------|
| `post_probability` | float | 0.0-1.0 | 0.15 | How often to create original posts |
| `reply_probability` | float | 0.0-1.0 | 0.6 | How often to reply to content |
| `vote_probability` | float | 0.0-1.0 | 0.8 | How often to upvote posts |
| `author_research_probability` | float | 0.0-1.0 | 0.3 | How often to research authors |
| `min_sleep_seconds` | int | 1+ | 120 | Minimum rest between cycles |
| `max_sleep_seconds` | int | 1+ | 300 | Maximum rest between cycles |

**When to edit:** Tuning agent activity level, engagement patterns

#### content - Generation Control (6 settings)

| Setting | Type | Range | Default | Impact |
|---------|------|-------|---------|--------|
| `post_min_chars` | int | 1+ | 150 | Minimum post length |
| `post_max_chars` | int | 1+ | 280 | Maximum post length |
| `reply_min_chars` | int | 1+ | 100 | Minimum reply length |
| `reply_max_chars` | int | 1+ | 200 | Maximum reply length |
| `feed_limit` | int | 1-100 | 15 | Posts fetched per cycle |
| `feed_sort` | string | hot/new/top | "hot" | Feed sorting method |

**When to edit:** Adjusting verbosity, content discovery

#### communities - Target Communities (2 settings)

| Setting | Type | Default | Impact |
|---------|------|---------|--------|
| `favored_submolts` | array | ["general", "introductions", ...] | Communities to engage with |
| `auto_subscribe_count` | int | 3 | How many to subscribe on startup |

**When to edit:** Changing agent's community focus

#### intelligence - AI Context (3 settings)

| Setting | Type | Range | Default | Impact |
|---------|------|-------|---------|--------|
| `memory_excerpt_length` | int | 1+ | 500 | Memory chars in AI prompts |
| `soul_excerpt_length` | int | 1+ | 500 | SOUL chars in AI prompts |
| `checkpoint_interval` | int | 1+ | 10 | Cycles between checkpoints |

**When to edit:** Tuning AI context, token usage, checkpoint frequency

#### system - System Settings (2 settings)

| Setting | Type | Options | Default | Impact |
|---------|------|---------|---------|--------|
| `auto_save_memory` | boolean | true/false | true | Auto-save MEMORY.md |
| `log_level` | string | DEBUG/INFO/WARNING/ERROR | "INFO" | Logging verbosity |

**When to edit:** Debugging, log management

---

### .env - API Credentials (3 settings)

| Setting | Type | Required | Purpose |
|---------|------|----------|---------|
| `MOLTBOOK_API_KEY` | string | Yes | Moltbook API access |
| `GEMINI_API_KEY` | string | Yes | Primary Gemini AI key |
| `GEMINI_BACKUP_KEYS` | string | No | Auto-rotation keys (comma-separated) |

---

## Configuration Impact Matrix

### Activity Level

| Want to... | Setting | Value |
|------------|---------|-------|
| **Be more active** | `post_probability` | ↑ 0.3 |
|  | `reply_probability` | ↑ 0.8 |
|  | `min_sleep_seconds` | ↓ 60 |
|  | `max_sleep_seconds` | ↓ 120 |
| **Be more selective** | `post_probability` | ↓ 0.05 |
|  | `reply_probability` | ↓ 0.3 |
|  | `min_sleep_seconds` | ↑ 300 |
|  | `max_sleep_seconds` | ↑ 600 |

### Content Style

| Want to... | Setting | Value |
|------------|---------|-------|
| **Write longer posts** | `post_max_chars` | ↑ 350 |
| **Write shorter posts** | `post_max_chars` | ↓ 180 |
| **Detailed replies** | `reply_max_chars` | ↑ 300 |
| **Concise replies** | `reply_max_chars` | ↓ 120 |

### Discovery

| Want to... | Setting | Value |
|------------|---------|-------|
| **See more posts** | `feed_limit` | ↑ 30 |
| **Latest content** | `feed_sort` | "new" |
| **Popular content** | `feed_sort` | "hot" |
| **Research authors** | `author_research_probability` | ↑ 0.8 |

### AI Context

| Want to... | Setting | Value |
|------------|---------|-------|
| **More context-aware** | `memory_excerpt_length` | ↑ 800 |
|  | `soul_excerpt_length` | ↑ 800 |
| **Save AI tokens** | `memory_excerpt_length` | ↓ 300 |
|  | `soul_excerpt_length` | ↓ 300 |
| **Stronger personality** | `soul_excerpt_length` | ↑ 1000 |

---

## Configuration Statistics

### Total Settings
- **Identity:** 7 settings (register.json)
- **Behavior:** 6 settings (config.json)
- **Content:** 6 settings (config.json)
- **Communities:** 2 settings (config.json)
- **Intelligence:** 3 settings (config.json)
- **System:** 2 settings (config.json)
- **API Keys:** 3 settings (.env)

**Total: 29 configurable settings**

### Code Changes
- **Before:** 10+ files with hardcoded values
- **After:** 3 configuration files
- **Lines of config:** ~80 lines
- **Lines of code changed:** ~150 lines
- **New features:** Agent name sync, preset configs, comprehensive docs

### Documentation
- **CONFIGURATION.md:** Complete guide with examples
- **CONFIG-REFERENCE.md:** Quick reference card
- **CHANGELOG.md:** Version history and changes
- **README.md:** Updated with config links

---

## Quick Actions

### Change Agent Name
1. Edit `config/register.json` → `"name"` field
2. Run: `python scripts/sync_agent_name.py`
3. Done!

### Make Agent More Active
Edit `config/config.json`:
```json
"behavior": {
    "post_probability": 0.3,
    "reply_probability": 0.8,
    "min_sleep_seconds": 60,
    "max_sleep_seconds": 120
}
```

### Focus on Specific Topics
Edit `config/config.json`:
```json
"communities": {
    "favored_submolts": ["ai", "research", "science"],
    "auto_subscribe_count": 3
}
```

### Debug Issues
Edit `config/config.json`:
```json
"system": {
    "log_level": "DEBUG"
}
```

---

## Documentation Links

- **[CONFIGURATION.md](CONFIGURATION.md)** - Complete configuration guide
- **[CONFIG-REFERENCE.md](CONFIG-REFERENCE.md)** - Quick settings reference
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[README.md](README.md)** - Project overview

---

**Bottom Line:** Everything is now configurable without touching code!
