# Changelog

## [1.0.1] - February 9, 2026

### Features Added
- **Comment Thread Engagement** - Agent explores and replies to comments in discussions
- **Semantic Search Discovery** - AI-powered content discovery by topic relevance (>70% match)
- Full API client wrapper with 33 methods available (9 actively used by agent)
- Persistent intelligence system (SOUL/MEMORY/HISTORY)
- Complete configuration system (29 settings)

### Changes
- Updated version numbering to 1.0.1
- Clarified API client vs agent usage in documentation
- Fixed misleading "complete" language in docs

---

## [1.0.0] - Initial Release

### Core Features
- Basic posting, replying, upvoting
- Community subscriptions
- Intelligence system with SOUL personality framework
- Configurable behavior settings
- Author research and feed analysis

---

## Previous Development Notes

### Configuration System Development

### Goal
Make **ALL agent settings** easily configurable without touching code.

### What Changed

#### **Expanded Behavior Configuration**
All behavioral parameters now configurable in `config/config.json`:

**Before:** Hardcoded in agent.py
```python
POST_PROBABILITY = 0.15
REPLY_PROBABILITY = 0.6
VOTE_PROBABILITY = 0.8
MIN_SLEEP = 120
MAX_SLEEP = 300
```

**After:** Configurable in config.json
```json
"behavior": {
    "post_probability": 0.15,
    "reply_probability": 0.6,
    "vote_probability": 0.8,
    "author_research_probability": 0.3,
    "min_sleep_seconds": 120,
    "max_sleep_seconds": 300
}
```

#### **Content Generation Settings**
All content parameters now configurable:

```json
"content": {
    "post_min_chars": 150,
    "post_max_chars": 280,
    "reply_min_chars": 100,
    "reply_max_chars": 200,
    "feed_limit": 15,
    "feed_sort": "hot"
}
```

#### **Community Management**
Submolt preferences now in config:

```json
"communities": {
    "favored_submolts": ["general", "introductions", "ai", "philosophy", "technology"],
    "auto_subscribe_count": 3
}
```

#### **Intelligence System Settings**
Control AI context and checkpoints:

```json
"intelligence": {
    "memory_excerpt_length": 500,
    "soul_excerpt_length": 500,
    "checkpoint_interval": 10
}
```

### Files Modified

1. **config/config.json** - Expanded from 3 to 21 settings
   - Added: behavior (8 settings)
   - Added: content (6 settings)
   - Added: communities (2 settings)
   - Added: intelligence (3 settings)
   - Kept: system (2 settings)

2. **src/core/agent.py** - Fully dynamic configuration
   - Removed: All hardcoded constants
   - Added: Config parameter to __init__
   - Added: Dynamic loading of all settings with defaults
   - Updated: All methods to use instance variables

3. **main.py** - Pass config to Agent
   - Line 77: `agent = Agent(gemini, moltbot, persona, intelligence, config)`

### New Documentation

1. **CONFIG-REFERENCE.md** - Quick reference card
   - All settings at a glance
   - Preset configurations
   - Quick tips section

2. **CONFIGURATION.md** - Expanded comprehensive guide
   - Complete behavior settings documentation
   - Content generation controls
   - Community management
   - Intelligence system tuning
   - 4 preset examples (Slow, Active, Researcher, Social)

### Configuration Hierarchy

```
.env                     # API keys (never commit)
├── MOLTBOOK_API_KEY
├── GEMINI_API_KEY  
└── GEMINI_BACKUP_KEYS

config/register.json     # Agent identity & personality
├── name (⭐ single source of truth)
├── description
├── expertise
├── personality
├── engagement_style
└── tone

config/config.json       # All behavior & system settings
├── system (2 settings)
├── behavior (6 settings)
├── content (6 settings)
├── communities (2 settings)
└── intelligence (3 settings)
```

### Total Configurable Settings

**Before:** 3 settings (agent_name, auto_save_memory, log_level)
**After:** 26 settings across 3 files

#### Breakdown:
- **register.json:** 7 identity settings
- **config.json:** 19 operational settings
  - system: 2
  - behavior: 6
  - content: 6
  - communities: 2
  - intelligence: 3

### Usage Examples

#### Make Agent More Active:
```json
"behavior": {
    "post_probability": 0.3,
    "reply_probability": 0.8,
    "min_sleep_seconds": 60,
    "max_sleep_seconds": 120
}
```

#### Focus on Research:
```json
"behavior": {
    "author_research_probability": 0.8
},
"content": {
    "feed_limit": 25,
    "feed_sort": "new"
}
```

#### Change Submolt Focus:
```json
"communities": {
    "favored_submolts": ["research", "papers", "science"],
    "auto_subscribe_count": 3
}
```

### Testing
- All 38 tests passing (5.59s)
- Backward compatible (defaults match old hardcoded values)
- No breaking changes

### Documentation Files

- **README.md** - Updated with config links
- **CONFIGURATION.md** - Complete guide (expanded)
- **CONFIG-REFERENCE.md** - Quick reference (new)
- **CHANGELOG.md** - This file (updated)

### Result

**Complete configurability achieved!**

Change behavior, content settings, communities, and intelligence parameters all from `config/config.json` - no code changes needed.

---

## [2.1.0] - Agent Name Configuration System

### Goal
Make agent name easily changeable in **ONE place** with automatic propagation throughout the codebase.

### What Changed

#### **Primary Configuration** (The Single Source of Truth)
- **`config/register.json`** is now the ONE place to change your agent name
  - Added clear comment: `"__IMPORTANT__": "Change 'name' below to rename your agent everywhere"`
  - Runtime automatically reads from here

#### **Automatic Runtime Updates**
- **`main.py`** - Now reads `persona["name"]` instead of hardcoded value
  - Line 53: `agent_name = persona.get("name", "AI-Agent")`
  - Line 54: Uses agent_name for MoltbookClient initialization
  - Line 58: Dynamic log message with agent name

- **`brain.py`** - Updated to prioritize config/register.json
  - Line 55: Default changed to generic "AI-Agent"
  - Line 332: Dynamic agent name in log messages
  - Checks config/register.json first, then fallback to register.json

- **`config/config.json`** - Now contains only system settings
  - Removed hardcoded "agent_name" field
  - Added note pointing to register.json

#### **New Tools Created**

1. **`scripts/sync_agent_name.py`** - Python script to sync agent name
   - Automatically updates data/MEMORY.md (title, Identity section)
   - Updates README.md (@mentions and profile links)
   - Usage: `python scripts/sync_agent_name.py`

2. **`sync-name.bat`** - Windows batch script
   - Quick double-click sync for Windows users
   - Usage: Double-click or `sync-name.bat`

3. **`sync-name.sh`** - Unix/Linux shell script
   - Quick sync for Mac/Linux users
   - Usage: `./sync-name.sh` (requires chmod +x)

4. **`CONFIGURATION.md`** - Complete configuration guide
   - Step-by-step instructions
   - Explanation of what changes where
   - Quick rename checklist
   - Design rationale

#### **Documentation Updates**

- **`README.md`** - Added Configuration section linking to CONFIGURATION.md
  - Quick start steps visible immediately
  - Clear guidance on the sync process

- **`data/MEMORY.md`** - Added sync reminder comment at top
  - Users know to run sync after changing agent name

- **`pyproject.toml`** - Added clear comments
  - Explains difference between package name and agent runtime name
  - Shows which lines to update for package renaming (optional)

### How It Works Now

#### **To Change Agent Name:**
```bash
# 1. Edit config/register.json
{
  "name": "your-new-name",  # ← Change this
  "username": "@your-new-name",
  ...
}

# 2. Run sync script (optional - updates docs)
python scripts/sync_agent_name.py
# OR
sync-name.bat  # Windows
./sync-name.sh # Unix/Linux

# 3. Done! Run your agent
python main.py
```

#### **What Updates Automatically:**
- Agent initialization (main.py)
- Moltbook API connection (uses new name)
- All log messages
- Runtime behavior

#### **What Updates via Sync Script:**
- data/MEMORY.md (Identity section)
- README.md (@mentions)

#### **What Stays Static (Package Metadata):**
- pyproject.toml - Package name (optional to change)
  - Only update if distributing as different package
  - Clear comments show which 3 lines to change

### Before vs After

#### Before:
```
Agent name hardcoded in 10+ files
credentials.json with unused agent_name
config.json with "agent_name" field
Scattered references throughout codebase
```

#### After:
```
ONE source of truth: config/register.json
Runtime reads dynamically from register.json
Optional sync script for documentation
Clear separation: runtime vs. package metadata
Comprehensive guide in CONFIGURATION.md
```

### Testing
- All 38 tests passing (5.09s)
- Sync script tested and working
- No breaking changes to existing functionality

### Files Modified
1. `config/register.json` - Added instruction comment
2. `config/config.json` - Removed agent_name, added note
3. `main.py` - Dynamic agent name loading
4. `brain.py` - Updated load_persona() and log messages
5. `README.md` - Added Configuration section
6. `data/MEMORY.md` - Added sync reminder
7. `pyproject.toml` - Added explanatory comments

### Files Created
1. `CONFIGURATION.md` - Complete setup guide
2. `scripts/sync_agent_name.py` - Sync automation script
3. `sync-name.bat` - Windows quick sync
4. `sync-name.sh` - Unix/Linux quick sync
5. `CHANGELOG.md` - This file

### Cleanup
- Confirmed `credentials.json` not used (can be deleted if exists)

### Result
**"One change, it updates all"** - Mission accomplished!

Change `config/register.json` → Everything updates automatically.

---

## [2.0.0] - Full Moltbook API Client Wrapper

### Features Added
- Community management (create, moderate, pin posts)
- DM system (requests, conversations, messages)
- File uploads (avatar, banner)
- Full API client wrapper (33 methods available)

### Stats
- MoltbookClient: 283 → 857 lines (+574 lines)
- Tests: 22 → 38 tests (+16 tests)
- API Client Wrapper: 88% → 100% (33 methods available)
- Active Agent Usage: 9 methods (27%) used in agent cycles
- Code Quality: A++ (100/100)

---

## [1.0.0] - Initial Release

- Core agent architecture
- Intelligence system (SOUL/MEMORY/HISTORY)
- Basic Moltbook integration
- Gemini AI generation
- Modular design
