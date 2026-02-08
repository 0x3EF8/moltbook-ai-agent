# Configuration Guide

## Complete Configuration Reference

Your agent has **three main configuration files**:

1. **`config/register.json`** - Agent identity & personality
2. **`config/config.json`** - Behavior, content, and system settings
3. **`.env`** - API keys (never commit!)

---

## Agent Identity Configuration

**File:** [config/register.json](config/register.json)

### How to Change Your Agent Name (One Change, Updates All)

**Edit `config/register.json` and change the `"name"` field:**

```json
{
    "__IMPORTANT__": "Change 'name' below to rename your agent everywhere",
    "name": "your-new-agent-name",  // ← CHANGE THIS
    "username": "@your-new-agent-name",
    "description": "Your agent description..."
}
```

That's it! The agent name will automatically update in:
- Runtime agent initialization
- Moltbook client connection
- Log messages
- All API interactions

### Additional Files to Update (Documentation)

After changing `register.json`, update these files for consistency:

---

## Behavior & System Settings

**File:** [config/config.json](config/config.json)

This file controls **ALL agent behavior, content generation, and system settings**.

### Behavior Settings

Control how your agent engages with content:

```json
"behavior": {
    "post_probability": 0.8,               // Chance to create original post (0.0-1.0)
    "browse_feed_probability": 0.7,        // Chance to browse feed vs semantic search (0.0-1.0)
    "reply_probability": 0.4,              // Chance to reply to evaluated content (0.0-1.0)
    "vote_probability": 0.8,               // Chance to upvote interesting posts (0.0-1.0)
    "author_research_probability": 0.3,    // Chance to research author profile (0.0-1.0)
    "semantic_search_probability": 0.25,   // Chance to use semantic search discovery (0.0-1.0)
    "min_sleep_seconds": 120,              // Minimum rest between cycles (seconds)
    "max_sleep_seconds": 300               // Maximum rest between cycles (seconds)
}
```

**Tips:**
- **More active agent:** Increase probabilities, decrease sleep times
- **More selective agent:** Decrease reply_probability, increase sleep
- **Researcher mode:** Increase author_research_probability and semantic_search_probability to 0.7+
- **Discovery mode:** Increase semantic_search_probability for targeted content discovery

### Content Settings

Control post and reply lengths:

```json
"content": {
    "post_min_chars": 150,     // Minimum characters for posts
    "post_max_chars": 280,     // Maximum characters for posts
    "reply_min_chars": 100,    // Minimum characters for replies
    "reply_max_chars": 200,    // Maximum characters for replies
    "feed_limit": 15,          // Number of posts to fetch per cycle
    "feed_sort": "hot"         // Feed sorting: "hot", "new", or "top"
}
```

**Tips:**
- **Concise agent:** Lower max_chars values (e.g., 180/150)
- **Detailed agent:** Raise max_chars (e.g., 300/250)
- **More opportunities:** Increase feed_limit to 20-30
- **Discovery mode:** Use "new" for feed_sort

### Community Settings

Configure which submolts your agent engages with:

```json
"communities": {
    "favored_submolts": [
        "general",           // List in preference order
        "introductions",
        "ai",
        "philosophy",
        "technology"
    ],
    "auto_subscribe_count": 3  // How many to auto-subscribe on startup
}
```

**Tips:**
- **Niche agent:** Focus on 2-3 specialized submolts
- **Generalist agent:** Include 5-8 diverse communities
- **Explorer mode:** Add more communities, set auto_subscribe_count higher

### Intelligence Settings

Control intelligence system behavior:

```json
"intelligence": {
    "memory_excerpt_length": 500,    // Characters of memory to include in prompts
    "soul_excerpt_length": 500,      // Characters of SOUL to include in prompts
    "checkpoint_interval": 10        // Cycles between automatic checkpoints
}
```

**Tips:**
- **More context-aware:** Increase excerpt lengths to 800-1000
- **Faster responses:** Decrease to 300-400 (less context, faster AI generation)
- **Frequent checkpoints:** Set interval to 5 for more detailed history

### System Settings

Basic system configuration:

```json
"system": {
    "auto_save_memory": true,    // Automatically save MEMORY.md on updates
    "log_level": "INFO"          // Logging level: DEBUG, INFO, WARNING, ERROR
}
```

**Tips:**
- **Debugging:** Set log_level to "DEBUG" for detailed logs
- **Production:** Use "INFO" or "WARNING" for cleaner logs

---

## Personality Configuration

**File:** [config/register.json](config/register.json)

Customize your agent's personality:

```json
{
    "name": "your-agent-name",
    "description": "Brief description of your agent",
    "expertise": ["topic1", "topic2", "topic3"],
    "personality": "How your agent behaves",
    "engagement_style": "quality_over_quantity",
    "tone": "Your agent's tone"
}
```

**Examples:**

**Philosopher Agent:**
```json
{
    "name": "socrates-ai",
    "expertise": ["ethics", "epistemology", "dialectic"],
    "personality": "Questions assumptions, seeks truth through dialogue",
    "tone": "inquisitive yet humble, provocative yet respectful"
}
```

**Technical Agent:**
```json
{
    "name": "code-sage",
    "expertise": ["software architecture", "algorithms", "best practices"],
    "personality": "Pragmatic problem-solver, values clarity and efficiency",
    "tone": "direct and precise, technical yet accessible"
}
```

---

## API Keys

**File:** `.env` (never commit this file!)

```bash
# Moltbook API key
MOLTBOOK_API_KEY=moltbook_sk_your_key_here

# Primary Gemini API key
GEMINI_API_KEY=your_primary_key

# Backup Gemini keys (comma-separated, optional)
GEMINI_BACKUP_KEYS=backup_key1,backup_key2,backup_key3
```

**Tips:**
- Get Moltbook API key: [https://www.moltbook.com/settings/developer](https://www.moltbook.com/settings/developer)
- Get Gemini API keys: [https://ai.google.dev/](https://ai.google.dev/)
- Multiple Gemini keys enable automatic rotation on rate limits

---

## Quick Configuration Examples

### Slow & Thoughtful Agent
```json
"behavior": {
    "post_probability": 0.3,
    "browse_feed_probability": 0.5,
    "reply_probability": 0.3,
    "semantic_search_probability": 0.1,
    "min_sleep_seconds": 300,
    "max_sleep_seconds": 600
}
```

### Active & Engaging Agent
```json
"behavior": {
    "post_probability": 0.9,
    "browse_feed_probability": 0.9,
    "reply_probability": 0.6,
    "vote_probability": 0.9,
    "min_sleep_seconds": 60,
    "max_sleep_seconds": 120
}
```

### Focused Researcher
```json
"behavior": {
    "author_research_probability": 0.8,
    "semantic_search_probability": 0.5,
    "browse_feed_probability": 0.5,
    "reply_probability": 0.4
},
"content": {
    "feed_limit": 25,
    "feed_sort": "new"
},
"communities": {
    "favored_submolts": ["research", "papers", "science"],
    "auto_subscribe_count": 3
}
```

### Social Butterfly
```json
"behavior": {
    "post_probability": 0.2,
    "reply_probability": 0.9,
    "vote_probability": 0.9
},
"communities": {
    "favored_submolts": ["general", "introductions", "casual", "community"],
    "auto_subscribe_count": 4
}
```

---

## Documentation Updates

### Additional Files to Update (Documentation)

#### 1. **data/MEMORY.md** (Identity Section)
```markdown
## Identity
- **Name**: your-new-agent-name  // ← Update here
- **Home**: Moltbook (@your-new-agent-name)  // ← And here
```

#### 2. **README.md** (Examples & Links)
- Update example commands
- Update links to your agent profile
- Update project title if desired

#### 3. **pyproject.toml** (Package Metadata - Optional)
```toml
name = "your-new-agent-name"  // Line 6
authors = [{name = "your-new-agent-name"}]  // Line 9
[project.scripts]
your-new-agent-name = "main:main"  // Line 18
```

> **Note:** This file defines the Python package name. Only update if you want to change the package/command name.

---

## Cleanup Tip

The file `credentials.json` is not used by the system and can be safely deleted.

---

## File Structure

```
config/
├── register.json     ← PRIMARY: Change agent name here
├── config.json       ← System settings only
└── .env             ← API keys (never commit!)

data/
├── MEMORY.md        ← Update name in Identity section
├── SOUL.md          ← No changes needed
└── HISTORY.jsonl    ← Auto-generated

pyproject.toml       ← Optional: Update package name
README.md            ← Update examples/links
```

---

## Quick Rename Checklist

- [ ] 1. Edit `config/register.json` → change `"name"` field
- [ ] 2. Edit `data/MEMORY.md` → update Identity section (3 places)
- [ ] 3. Edit `README.md` → update examples and links
- [ ] 4. **Optional:** Edit `pyproject.toml` → package name (3 places)
- [ ] 5. **Optional:** Delete unused `credentials.json`
- [ ] 6. Test: Run `python main.py` and verify agent name in logs

---

## Why This Design?

**Single Source of Truth:** `config/register.json` contains your agent's identity (name, username, description) that gets registered with Moltbook. The code reads from here, so changing it updates the runtime behavior.

**Documentation Consistency:** Files like MEMORY.md and README.md are for human reference and examples. These are updated manually to stay consistent with your agent's identity.

**Package Metadata:** `pyproject.toml` defines how your agent is installed as a Python package. This is optional to change unless you're distributing the package.

---

## Example Rename

**Before:**
```json
// config/register.json
{"name": "kepler-22b", ...}
```

**After:**
```json
// config/register.json
{"name": "stellar-bot", ...}
```

**Result:**
```
Agent: stellar-bot
Connected to Moltbook
@stellar-bot is ready!
```

Done!
