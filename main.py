"""
Moltbook AI Agent - Entry Point

Agent name configured in config/register.json
See CONFIGURATION.md for setup instructions.
"""
import logging
import sys

from src.utils import ConfigLoader
from src.clients.gemini_client import GeminiClient
from src.clients.moltbook_client import MoltbookClient
from src.intelligence import IntelligenceSystem
from src.core.agent import Agent


def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point for the agent"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Load configuration
    env = ConfigLoader.load_env()
    config = ConfigLoader.load_json("config/config.json")
    persona = ConfigLoader.load_json("config/register.json")
    
    logger.info(f"Initializing {persona.get('name', 'AI Agent')} Advanced Intelligence System...")
    logger.info("═" * 60)
    
    if not config:
        logger.error("Error: config.json not found")
        return
    
    # Validate API keys
    moltbook_api_key = env.get("MOLTBOOK_API_KEY")
    if not moltbook_api_key:
        logger.error("Error: MOLTBOOK_API_KEY not found in .env file")
        return
    
    gemini_keys = env.get("GEMINI_API_KEY", "") + "," + env.get("GEMINI_BACKUP_KEYS", "")
    gemini_keys = gemini_keys.strip(",")
    
    # Initialize components
    agent_name = persona.get("name", "AI-Agent")
    gemini = GeminiClient(gemini_keys)
    moltbot = MoltbookClient(moltbook_api_key, agent_name)
    intelligence = IntelligenceSystem()
    
    # Display agent info
    logger.info(f"Agent: {agent_name}")
    logger.info(f"Role: {persona.get('description', 'AI Agent')}")
    logger.info(f"Expertise: {', '.join(persona.get('expertise', ['General AI']))}")
    logger.info(f"Style: {persona.get('engagement_style', 'balanced')}")
    
    # Show intelligence stats
    stats = intelligence.get_stats()
    if stats['soul_words'] > 0:
        logger.info(f"SOUL.md: Loaded ({stats['soul_words']} words of personality)")
    if stats['memory_words'] > 0:
        logger.info(f"MEMORY.md: Loaded ({stats['memory_words']} words of history)")
    
    logger.info("═" * 60)
    
    # Create and run agent with full config
    agent = Agent(gemini, moltbot, persona, intelligence, config)
    agent.initialize()
    
    # Main loop
    while True:
        agent.run_cycle()
        agent.rest()


if __name__ == "__main__":
    main()
