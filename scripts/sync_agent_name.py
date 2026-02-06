#!/usr/bin/env python3
"""
Sync agent name from config/register.json to documentation files.

Usage:
    python scripts/sync_agent_name.py

This script reads the agent name from config/register.json and updates:
- data/MEMORY.md (Identity section)
- README.md (examples and links)
"""

import json
import os
import re
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent


def load_agent_name():
    """Load agent name from register.json."""
    register_path = PROJECT_ROOT / "config" / "register.json"
    if not register_path.exists():
        register_path = PROJECT_ROOT / "register.json"
    
    if not register_path.exists():
        print("Error: register.json not found!")
        return None
    
    with open(register_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("name", "").strip()


def update_memory_md(agent_name: str):
    """Update agent name in data/MEMORY.md."""
    memory_path = PROJECT_ROOT / "data" / "MEMORY.md"
    
    if not memory_path.exists():
        print(f"Warning: {memory_path} not found, skipping...")
        return False
    
    with open(memory_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Update patterns
    patterns = [
        (r"^# .* Memory System", f"# {agent_name} Memory System"),  # Title
        (r"- \*\*Name\*\*: .*$", f"- **Name**: {agent_name}", re.MULTILINE),  # Identity name
        (r"- \*\*Home\*\*: Moltbook \(@.*\)", f"- **Home**: Moltbook (@{agent_name})"),  # Home
    ]
    
    updated_content = content
    changes_made = False
    
    for pattern, replacement, *flags in patterns:
        flag = flags[0] if flags else 0
        new_content = re.sub(pattern, replacement, updated_content, flags=flag)
        if new_content != updated_content:
            changes_made = True
            updated_content = new_content
    
    if changes_made:
        with open(memory_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated {memory_path.relative_to(PROJECT_ROOT)}")
        return True
    else:
        print(f"No changes needed in {memory_path.relative_to(PROJECT_ROOT)}")
        return False


def update_readme_md(agent_name: str):
    """Update agent name in README.md (title and examples)."""
    readme_path = PROJECT_ROOT / "README.md"
    
    if not readme_path.exists():
        print(f"Warning: {readme_path} not found, skipping...")
        return False
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Note: Only update direct @mentions and profile links
    # Don't replace title to preserve branding
    old_pattern = r"@kepler-22b"
    new_replacement = f"@{agent_name}"
    
    updated_content = content.replace(old_pattern, new_replacement)
    
    if updated_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated {readme_path.relative_to(PROJECT_ROOT)}")
        return True
    else:
        print(f"No @mentions to update in {readme_path.relative_to(PROJECT_ROOT)}")
        return False


def main():
    """Main sync function."""
    print("Syncing agent name from config/register.json...\n")
    
    # Load agent name
    agent_name = load_agent_name()
    if not agent_name:
        print("Failed to load agent name!")
        return 1
    
    print(f"Agent name: {agent_name}\n")
    
    # Update files
    results = []
    results.append(update_memory_md(agent_name))
    results.append(update_readme_md(agent_name))
    
    # Summary
    print(f"\n{'='*50}")
    if any(results):
        print("Sync complete! Files updated with new agent name.")
    else:
        print("Sync complete! All files already up to date.")
    print(f"{'='*50}")
    
    return 0


if __name__ == "__main__":
    exit(main())
