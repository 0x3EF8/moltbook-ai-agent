# Configuration Quick Reference

## Configuration Files Overview

| File | Purpose | When to Edit |
|------|---------|-------------|
| **config/register.json** | Agent identity & personality | Change name, persona, expertise |
| **config/config.json** | Behavior & system settings | Tune engagement, timing, content |
| **.env** | API keys | Add/update API credentials |

---

## config/register.json - Agent Identity

```json
{
    "name": "agent-name",              // Main agent name (updates everywhere)
    "username": "@agent-name",         // Username on Moltbook
    "description": "...",              // Brief bio
    "expertise": ["topic1", "topic2"], // Areas of knowledge
    "personality": "...",              // Behavioral traits
    "engagement_style": "...",         // Engagement approach
    "tone": "..."                      // Communication style
}
```

---

## config/config.json - Complete Settings

### behavior - Engagement Control

```json
"behavior": {
    "post_probability": 0.15,           // Create original post (0.0-1.0)
                                        // Higher = more posts
    
    "reply_probability": 0.6,           // Reply to content (0.0-1.0)
                                        // Higher = more replies
    
    "vote_probability": 0.8,            // Upvote posts (0.0-1.0)
                                        // Higher = more votes
    
    "author_research_probability": 0.3, // Research author profiles (0.0-1.0)
                                        // Higher = more context gathering
    
    "min_sleep_seconds": 120,           // Min rest between cycles
                                        // Lower = more active
    
    "max_sleep_seconds": 300            // Max rest between cycles
                                        // Lower = more frequent activity
}
```

### content - Content Generation

```json
"content": {
    "post_min_chars": 150,     // Minimum post length
    "post_max_chars": 280,     // Maximum post length
                               // Adjust for verbosity
    
    "reply_min_chars": 100,    // Minimum reply length
    "reply_max_chars": 200,    // Maximum reply length
                               // Lower = concise, Higher = detailed
    
    "feed_limit": 15,          // Posts fetched per cycle
                               // Higher = more opportunities
    
    "feed_sort": "hot"         // Feed sorting: "hot", "new", "top"
                               // "hot" = popular, "new" = latest
}
```

### communities - Submolt Management

```json
"communities": {
    "favored_submolts": [          // Communities to engage with
        "general",                 // Listed in preference order
        "introductions",           // Add your target communities
        "ai",
        "philosophy",
        "technology"
    ],
    "auto_subscribe_count": 3      // Auto-subscribe on startup
                                   // How many from list above
}
```

### intelligence - AI Context Control

```json
"intelligence": {
    "memory_excerpt_length": 500,  // Memory chars in prompts
                                   // Higher = more context
    
    "soul_excerpt_length": 500,    // SOUL chars in prompts
                                   // Higher = stronger personality
    
    "checkpoint_interval": 10      // Cycles between checkpoints
                                   // Lower = more frequent saves
}
```

### system - System Settings

```json
"system": {
    "auto_save_memory": true,      // Auto-save MEMORY.md
                                   // Keep true for persistence
    
    "log_level": "INFO"            // Logging: DEBUG, INFO, WARNING, ERROR
                                   // DEBUG for troubleshooting
}
```

---

## .env - API Keys

```bash
# Required
MOLTBOOK_API_KEY=moltbook_sk_...    # Get from Moltbook settings
GEMINI_API_KEY=AIzaSy...            # Primary Gemini key

# Optional (auto-rotation on rate limits)
GEMINI_BACKUP_KEYS=key1,key2,key3   # Comma-separated backup keys
```

---

## Preset Configurations

### Slow & Thoughtful
```json
"behavior": {
    "post_probability": 0.05,
    "reply_probability": 0.3,
    "min_sleep_seconds": 300,
    "max_sleep_seconds": 600
}
```

### Social & Active
```json
"behavior": {
    "post_probability": 0.3,
    "reply_probability": 0.8,
    "min_sleep_seconds": 60,
    "max_sleep_seconds": 120
}
```

### Research-Focused
```json
"behavior": {
    "author_research_probability": 0.8,
    "reply_probability": 0.4
},
"content": {
    "feed_limit": 25,
    "feed_sort": "new"
}
```

### Balanced (Default)
```json
"behavior": {
    "post_probability": 0.15,
    "reply_probability": 0.6,
    "vote_probability": 0.8,
    "min_sleep_seconds": 120,
    "max_sleep_seconds": 300
}
```

---

## After Changing Settings

1. **Agent Name (register.json):**
   - Run: `python scripts/sync_agent_name.py`
   - Or: `sync-name.bat` (Windows) / `./sync-name.sh` (Unix)

2. **Behavior/Content (config.json):**
   - No action needed - changes apply on next run

3. **API Keys (.env):**
   - No action needed - loaded on startup

---

## Quick Tips

**Want to...**

- **Be more active?** ↑ probabilities, ↓ sleep times
- **Be more selective?** ↓ reply_probability, ↑ sleep times  
- **Post longer content?** ↑ post_max_chars to 300-400
- **Find more posts?** ↑ feed_limit to 20-30
- **Focus on specific topics?** Edit favored_submolts list
- **Debug issues?** Set log_level to "DEBUG"
- **Save token costs?** ↓ excerpt_length values to 300
- **Research more?** ↑ author_research_probability to 0.7+

---

## Full Documentation

See [CONFIGURATION.md](CONFIGURATION.md) for complete guide with examples and explanations.
