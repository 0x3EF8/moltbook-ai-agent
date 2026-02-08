"""
Agent Name Sync Script
Syncs agent name from config/register.json to documentation files

This script is optional - the agent runtime automatically uses the name from register.json.
Use this to update documentation references after changing your agent name.
"""
import json
import re
from pathlib import Path


def load_agent_name():
    """Load agent name from config/register.json"""
    config_path = Path("config/register.json")
    if not config_path.exists():
        print("Error: config/register.json not found")
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config.get('name')


def update_file(file_path, old_name, new_name):
    """Update agent name references in a file"""
    path = Path(file_path)
    if not path.exists():
        return False
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace agent name references (case-sensitive)
        updated = content.replace(old_name, new_name)
        updated = updated.replace(f"@{old_name}", f"@{new_name}")
        
        if content != updated:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(updated)
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False


def main():
    """Main sync function"""
    print("Agent Name Sync Utility")
    print("=" * 60)
    
    # Load new agent name
    new_name = load_agent_name()
    if not new_name:
        return
    
    print(f"Agent name in config: {new_name}")
    
    # Ask for old name
    old_name = input("\nEnter OLD agent name to replace (or press Enter to skip): ").strip()
    
    if not old_name:
        print("\nSkipping sync - agent name will be used automatically at runtime.")
        print("Documentation references can be updated manually if needed.")
        return
    
    if old_name == new_name:
        print(f"\nNo change needed - agent name is already '{new_name}'")
        return
    
    print(f"\nSyncing: '{old_name}' → '{new_name}'")
    print("-" * 60)
    
    # Files to update
    docs_to_update = [
        "docs/WHATS-CONFIGURABLE.md",
        "docs/CONFIGURATION.md",
        "docs/API_REFERENCE.md",
        "docs/INTELLIGENCE.md",
        "data/SOUL.md"
    ]
    
    updated_count = 0
    for doc in docs_to_update:
        if update_file(doc, old_name, new_name):
            print(f"✓ Updated: {doc}")
            updated_count += 1
        else:
            print(f"  Skipped: {doc} (no changes or not found)")
    
    print("-" * 60)
    print(f"\n✓ Sync complete! Updated {updated_count} file(s)")
    print(f"\nYour agent will now use the name '{new_name}' everywhere.")


if __name__ == "__main__":
    main()
