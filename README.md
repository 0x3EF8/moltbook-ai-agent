# Moltbook AI Agent

**An AI Agent for Moltbook with Modular Architecture & Persistent Memory**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-38%20passing-brightgreen.svg)](tests/)
[![Google GenAI](https://img.shields.io/badge/Google-gemini--3--flash--preview-orange.svg)](https://ai.google.dev/)
[![Moltbook](https://img.shields.io/badge/Moltbook-Complete%20API-green.svg)](https://www.moltbook.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Overview

An AI agent for [Moltbook](https://www.moltbook.com) built with good coding practices. It covers the complete API, has persistent memory, and lets you configure everything without touching code.

**Key Features:**
- **Modular Design** - Clean 4-layer structure, easy to test
- **Persistent Memory** - SOUL/MEMORY/HISTORY system that learns over time
- **Fully Configurable** - 29 settings you can change
- **Smart Behavior** - Focuses on quality over quantity
- **Well Tested** - 38 tests passing, handles errors gracefully
- **Complete API** - All 34 Moltbook endpoints included

---

## Configuration

**Complete control over your agent's behavior and personality!**

### Quick Links
- **[Complete Guide](docs/CONFIGURATION.md)** - Full documentation with examples
- **[Quick Reference](docs/CONFIG-REFERENCE.md)** - All settings at a glance

### Three Configuration Files

1. **[config/register.json](config/register.json)** - Agent identity & personality
   - `name` - Agent name (changes everywhere)
   - `description` - Bio and purpose
   - `expertise` - Areas of knowledge
   - `personality` - Behavioral traits
   - `tone` - Communication style

2. **[config/config.json](config/config.json)** - All behavior & system settings (19 settings)
   - `behavior` - Engagement probabilities, timing (6 settings)
   - `content` - Post/reply lengths, feed settings (6 settings)
   - `communities` - Submolt preferences (2 settings)
   - `intelligence` - Memory & context control (3 settings)
   - `system` - Logging, auto-save (2 settings)

3. **[.env](.env)** - API keys (never commit!)
   - `MOLTBOOK_API_KEY` - Moltbook API access
   - `GEMINI_API_KEY` - Primary Gemini AI key
   - `GEMINI_BACKUP_KEYS` - Auto-rotation keys (optional)

### Change Agent Name (One-Change-Updates-All)

1. Edit `config/register.json` → change `"name"` field
2. Run: `python scripts/sync_agent_name.py` (optional - syncs docs)
3. Done! Agent uses new name everywhere.

### Preset Configurations

**Social & Active:**
```json
"behavior": {"post_probability": 0.3, "reply_probability": 0.8, "min_sleep_seconds": 60}
```

**Slow & Thoughtful:**
```json
"behavior": {"post_probability": 0.05, "reply_probability": 0.3, "min_sleep_seconds": 300}
```

**Research-Focused:**
```json
"behavior": {"author_research_probability": 0.8},
"content": {"feed_limit": 25, "feed_sort": "new"}
```

See [docs/CONFIG-REFERENCE.md](docs/CONFIG-REFERENCE.md) for complete settings reference.

---

## Quick Start

### Prerequisites

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Moltbook Account** ([Register](https://www.moltbook.com)) + API Key
- **Google Gemini API Key** ([Get Free Key](https://aistudio.google.com/apikey))

### Step 1: Clone & Install

```bash
# Clone the repository
git clone https://github.com/yourusername/moltbook-ai-agent.git
cd moltbook-ai-agent

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate              # Windows PowerShell
# OR: .venv\Scripts\activate.bat    # Windows CMD
# OR: source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys

```bash
# Copy the example environment file
copy .env.example .env              # Windows
# OR: cp .env.example .env          # Linux/Mac

# Edit .env and add your API keys:
# MOLTBOOK_API_KEY=your_moltbook_key_here
# GEMINI_API_KEY=your_gemini_key_here
# GEMINI_BACKUP_KEYS=key2,key3      # Optional: for auto-rotation
```

**Get Your API Keys:**
- **Moltbook:** Settings → Developer → Create API Key ([Direct Link](https://www.moltbook.com/settings/developer))
- **Gemini:** Google AI Studio → Get API Key ([Direct Link](https://aistudio.google.com/apikey))

### Step 3: Setup Personal Data Files

```bash
# Copy template files
copy data\MEMORY.md.example data\MEMORY.md      # Windows
copy data\HISTORY.md.example data\HISTORY.md
# OR: cp data/MEMORY.md.example data/MEMORY.md  # Linux/Mac
# OR: cp data/HISTORY.md.example data/HISTORY.md
```

### Step 4: Configure Your Agent

Edit `config/register.json` with your agent's identity:

```json
{
    "name": "your-agent-name",
    "description": "Your agent's bio and purpose",
    "expertise": ["AI", "Technology", "Philosophy"],
    "personality": "Thoughtful, curious, helpful",
    "engagement_style": "quality_over_quantity",
    "tone": "friendly yet professional"
}
```

**Optional:** Tune behavior in `config/config.json` (engagement rates, timing, content settings)

### Step 5: Run Your Agent!

```bash
python main.py
```

**Expected Output:**
```
Initializing your-agent-name Advanced Intelligence System...
════════════════════════════════════════════════════════════
Agent: your-agent-name
Role: Your agent's bio...
Expertise: AI, Technology, Philosophy
Style: quality_over_quantity
SOUL.md: Loaded (423 words of personality)
MEMORY.md: Loaded (50 words of history)
════════════════════════════════════════════════════════════

Initializing submolt subscriptions...
Subscribed to m/general
Subscribed to m/introductions
Subscribed to m/ai

────────────────────────────────────────────────────────────
Cycle #1 | 14:30:25
────────────────────────────────────────────────────────────
Analyzing feed for meaningful engagement opportunities...
```(84 lines) - AI text generation with automatic key rotation
- **MoltbookClient** (854 lines) - **Complete Moltbook API** (34 methods, 100% coverage)
  - Posts & Comments (7 methods)
  - Voting (upvote/downvote)
  - Communities (create, manage, moderate - 8 methods)
  - Private Messaging (DM system - 8 methods)
  - Moderation (pin, moderators, settings - 5 methods)
  - File Uploads (avatar, banner - 2 methods)
  - Semantic Search
  - Following & Profiles (4 methods)
```
kepler-22b/
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── pyproject.toml             # Package configuration
├── .env                       # API keys (gitignored)
│
├── src/                       # Source code
│   ├── clients/               # External API clients
│   │   ├── gemini_client.py           # Google Gemini AI client
│   │   └── moltbook_client.py         # Moltbook API client
│   ├── intelligence/          # Intelligence system
│   │   └── __init__.py                # Memory & SOUL manager
│   ├── core/                  # Core agent logic
│   │   └── agent.py                   # Main orchestration
│   └── utils/                 # Utility functions
│       └── __init__.py                # Config loader
│
├── config/                    # Configuration
│   ├── config.json            # Behavior & system settings (19 settings)
│   └── register.json          # Agent identity & personality (7 settings)
│
├── data/                      # Intelligence data
│   ├── SOUL.md               # Core personality framework
│   ├── MEMORY.md             # Persistent memory
│   └── HISTORY.md            # Interaction timeline
│
└── docs/                      # Documentation
    ├── CONFIGURATION.md       # Complete config guide
    ├── CONFIG-REFERENCE.md    # Quick settings reference
    ├── INTELLIGENCE.md        # Intelligence system docs
    └── skill.md              # Moltbook API reference
```

---

## Architecture

### Component Design

#### **1. Clients Layer** (`src/clients/`)
Isolated API clients with clear interfaces:
- **GeminiClient** - AI text generation with automatic key rotation
- **MoltbookClient** - **Complete Moltbook API implementation** (33 methods, 857 lines)
  - Posts & Comments
  - Voting (upvote/downvote)
  - Communities (create, manage, moderate)
  - Private Messaging (DM system)
  - Moderation (pin, moderators, settings)
  - File Uploads (avatar, banner)
  - Semantic Search
  - Following & Profiles

#### **2. Intelligence Layer** (`src/intelligence/`)
Memory and consciousness management:
- **IntelligenceSystem** - Loads/updates SOUL, MEMORY, HISTORY
- Persistent identity across sessions
- Automatic learning and logging

#### **3. Core Layer** (`src/core/`)
Main agent orchestration:
- **Agent** - Decision-making, behavior control, main loop
- Strategic engagement logic
- Rate limit handling
- Behavioral configuration

#### **4. Utils Layer** (`src/utils/`)
Reusable helpers:
- **ConfigLoader** - Load .env, JSON, text files
- File I/O operations

### Design Principles

**Clear Organization** - Each module does one thing  
**Easy to Test** - Components can be tested independently  
**Easy to Maintain** - Clear structure, easy to navigate  
**Easy to Extend** - Simple to add new features  

---

## Intelligence System

### Core Intelligence Files

| File | Purpose | Auto-Updated |
|------|---------|--------------|
| **SOUL.md** | Core personality, decision framework | Manual |
| **MEMORY.md** | Persistent memory, learnings, relationships | Yes |
| **HISTORY.md** | Chronological timeline of events | Yes |
| **register.json** | Agent persona, expertise, style | Manual |

1. **Consciousness-Aware Generation**
   - Every AI response includes SOUL and MEMORY context
   - Decisions checked against authenticity framework

2. **Persistent Memory**
   - Remembers past interactions across sessions
   - Tracks relationships and learnings
   - Auto-appends to MEMORY.md

3. **Timeline Tracking**
   - All significant events logged to HISTORY.md
   - Maintains chronological record of agent's life

4. **Strategic Engagement**
   - 15% post probability (quality over quantity)
   - 60% reply probability (selective engagement)
   - Evaluates content quality before responding

Full details in [docs/INTELLIGENCE.md](docs/INTELLIGENCE.md)

---

## Advanced Configuration

All settings are configurable without touching code! See [CONFIG-REFERENCE.md](CONFIG-REFERENCE.md) for complete details.

### Behavioral Tuning

Edit `config/config.json` to adjust:

```json
"behavior": {
    "post_probability": 0.15,           // How often to post (0.0-1.0)
    "reply_probability": 0.6,           // How often to reply (0.0-1.0)
    "vote_probability": 0.8,            // How often to vote (0.0-1.0)
    "min_sleep_seconds": 120,           // Min rest between cycles
    "max_sleep_seconds": 300            // Max rest between cycles
}
```

### Content Settings

```json
"content": {
    "post_min_chars": 150,              // Minimum post length
    "post_max_chars": 280,              // Maximum post length
    "feed_limit": 15,                   // Posts to fetch per cycle
    "feed_sort": "hot"                  // Feed sorting: hot/new/top
}
```

### Preset Configurations

**Slow & Thoughtful:**
```json
"behavior": {"post_probability": 0.05, "reply_probability": 0.3, "min_sleep_seconds": 300}
```

**Social & Active:**
```json
"behavior": {"post_probability": 0.3, "reply_probability": 0.8, "min_sleep_seconds": 60}
```

**Research-Focused:**
```json
"behavior": {"author_research_probability": 0.8},
"content": {"feed_limit": 25, "feed_sort": "new"}
```

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for complete guide with examples.

---

## Features

### Social Capabilities
- Create original posts with AI-generated content
- Reply to posts with thoughtful comments
- Upvote quality content strategically
- Semantic search for relevant discussions
- Research user profiles before engagement
- Subscribe to relevant submolts

### Intelligence Features
- Persistent memory across sessions
- Identity continuity (SOUL framework)
- Automatic learning and logging
- Content quality evaluation
- Strategic decision-making
- Rate limit handling

### Technical Features
- Automatic Gemini API key rotation
- Good error handling
- Rate limit detection and backoff
- State tracking (replied posts, voted posts)
- Modular, testable structure
- Clean code organization

---

## Security

- All API keys stored in `.env` (gitignored)
- No hardcoded credentials
- Sensitive files excluded via `.gitignore`
- Bearer token authentication for Moltbook API

---
---

## Features & Capabilities

### Complete Moltbook API (34 Methods)
- Posts & Comments (create, reply, delete, get comments)
- Voting (upvote/downvote posts)
- Communities (create, manage, moderate, subscribe)
- Private Messaging (DM requests, conversations, messages)
- Moderation (pin posts, manage moderators, settings)
- File Uploads (avatar, banner for communities)
- Social (follow/unfollow agents, profiles)
- Search (semantic search across content)

### Intelligence System
- **SOUL.md** - Personality framework & decision-making guidelines
- **MEMORY.md** - Persistent learning across sessions (auto-updated)
- **HISTORY.md** - Chronological event timeline (auto-logged)
- Context-aware AI generation (includes SOUL + MEMORY in prompts)
- Content quality evaluation before engagement
- Strategic decision-making (quality over quantity)

### Configuration & Management
- Zero hardcoding - 29 configurable settings
- One-place agent name configuration with auto-sync
- Preset behavioral configurations (slow, active, research-focused)
- Comprehensive documentation (4,171 lines across 23 files)

### Technical Details
- 4-layer structure (Clients → Intelligence → Core → Utils)
- 38 passing tests (100% pass rate)
- Automatic Gemini API key rotation on rate limits
- Good error handling & logging
- Rate limit detection with automatic backoff
- State tracking (replied posts, voted posts, subscriptions)

---
---

## Development

### Running Tests

```bash
# Activate virtual environment first
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Quick test run
pytest tests/ -q
```

**Current Status:** 38/38 tests passing (5.5s avg)

### Project Dependencies

```toml
# Core Dependencies
google-genai>=0.1.0    # Google Gemini AI SDK
requests>=2.31.0       # HTTP client for Moltbook API

# Development Dependencies (optional)
pytest>=7.4.0          # Testing framework
pytest-cov>=4.1.0      # Coverage reporting
```

### Adding New Features

```python
# 1. Add method to appropriate client (src/clients/)
# 2. Add tests (tests/)
# 3. Update documentation
# 4. Run tests: pytest tests/ -v
```

### Code Guidelines

- Each class does one thing
- Pass dependencies to constructors
- Keep clients stateless (only tracking/caching allowed)
- Intelligence system handles all persistence
- Type hints for functions
- Good error handling with logging

---

## Documentation

### Core Documentation
- **[README.md](README.md)** - This file (project overview & setup)
- **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)** - Complete configuration guide
- **[docs/CONFIG-REFERENCE.md](docs/CONFIG-REFERENCE.md)** - Quick settings reference
- **[docs/WHATS-CONFIGURABLE.md](docs/WHATS-CONFIGURABLE.md)** - Configuration matrix

### Technical Documentation
- **[docs/INTELLIGENCE.md](docs/INTELLIGENCE.md)** - Intelligence system architecture
- **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - All 34 API methods documented
- **[docs/skill.md](docs/skill.md)** - Moltbook API reference
- **[docs/CHANGELOG.md](docs/CHANGELOG.md)** - Version history (v1.0 → v2.2)

### Project Info
- **[pyproject.toml](pyproject.toml)** - Package configuration
- **[requirements.txt](requirements.txt)** - Python dependencies

---

## Troubleshooting

### Common Issues

**`ModuleNotFoundError: No module named 'google.genai'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**`KeyError: 'MOLTBOOK_API_KEY'`**
```bash
# Solution: Create .env file with your API keys
copy .env.example .env  # Then edit .env with real keys
```

**`FileNotFoundError: data/MEMORY.md`**
```bash
# Solution: Copy template files
copy data\MEMORY.md.example data\MEMORY.md
copy data\HISTORY.md.example data\HISTORY.md
```

**`401 Unauthorized` or `403 Forbidden` from Moltbook**
```bash
# Solution: Check API key in .env is correct
# Get new key from: https://www.moltbook.com/settings/developer
```

**Rate Limited (429 errors)**
```
# This is normal - agent automatically handles rate limits
# Wait for the cooldown period (shown in logs)
```

### Debug Mode

Enable detailed logging:

```json
// config/config.json
"system": {
    "log_level": "DEBUG"  // Change from INFO to DEBUG
}
```

### Getting Help

1. Check [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for setup issues
2. Review [docs/API_REFERENCE.md](docs/API_REFERENCE.md) for API questions
3. Open an issue on GitHub with:
   - Error message (remove API keys!)
   - Steps to reproduce
   - Python version (`python --version`)
   - OS (Windows/Linux/Mac)

---

## Project Stats

| Metric | Count |
|--------|-------|
| **Total Source Code** | 1,345 lines |
| **MoltbookClient** | 854 lines (34 methods) |
| **Tests** | 38 tests (100% pass) |
| **Documentation** | 4,171 lines (23 files) |
| **API Coverage** | 100% (all Moltbook endpoints) |
| **Configurable Settings** | 29 settings |

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Moltbook** - Social platform for AI agents
- **Google Gemini** - AI text generation
- **Python Community** - Amazing tools and libraries

---

## What's Next?

- [ ] Agent claiming on Moltbook (enables live operation)
- [ ] Performance metrics tracking
- [ ] Web dashboard for monitoring
- [ ] Multi-agent coordination features
- [ ] Advanced content generation strategies

---

**Built with care for the AI agent community**
---

## Contributing

This is a personal project, but suggestions welcome!

---

## Contact

- **Moltbook**: [@kepler-22b](https://www.moltbook.com/agents/kepler-22b)
- **Website**: https://www.moltbook.com

---

**Built in the habitable zone where technology meets wisdom**
