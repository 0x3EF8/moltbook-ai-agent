"""
Core Agent - Main intelligence orchestration
"""
import time
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from src.clients.gemini_client import GeminiClient
from src.clients.moltbook_client import MoltbookClient
from src.intelligence import IntelligenceSystem

logger = logging.getLogger(__name__)


class Agent:
    """Core agent with intelligence system"""
    
    def __init__(self, gemini: GeminiClient, moltbot: MoltbookClient, 
                 persona: Dict[str, Any], intelligence: IntelligenceSystem,
                 config: Dict[str, Any] = None):
        """
        Initialize agent
        
        Args:
            gemini: Gemini AI client
            moltbot: Moltbook API client
            persona: Agent persona configuration
            intelligence: Intelligence system
            config: Configuration dict (behavior, content, communities, intelligence settings)
        """
        self.gemini = gemini
        self.moltbot = moltbot
        self.persona = persona
        self.intelligence = intelligence
        
        # Load configuration with defaults
        config = config or {}
        behavior = config.get("behavior", {})
        content = config.get("content", {})
        communities = config.get("communities", {})
        intel = config.get("intelligence", {})
        
        # Behavioral Configuration
        self.POST_PROBABILITY = behavior.get("post_probability", 0.15)
        self.REPLY_PROBABILITY = behavior.get("reply_probability", 0.6)
        self.VOTE_PROBABILITY = behavior.get("vote_probability", 0.8)
        self.AUTHOR_RESEARCH_PROB = behavior.get("author_research_probability", 0.3)
        self.MIN_SLEEP = behavior.get("min_sleep_seconds", 120)
        self.MAX_SLEEP = behavior.get("max_sleep_seconds", 300)
        
        # Content Configuration
        self.POST_MIN_CHARS = content.get("post_min_chars", 150)
        self.POST_MAX_CHARS = content.get("post_max_chars", 280)
        self.REPLY_MIN_CHARS = content.get("reply_min_chars", 100)
        self.REPLY_MAX_CHARS = content.get("reply_max_chars", 200)
        self.FEED_LIMIT = content.get("feed_limit", 15)
        self.FEED_SORT = content.get("feed_sort", "hot")
        
        # Community Configuration
        self.FAVORED_SUBMOLTS = communities.get("favored_submolts", 
                                                 ["general", "introductions", "ai", "philosophy", "technology"])
        self.AUTO_SUBSCRIBE_COUNT = communities.get("auto_subscribe_count", 3)
        
        # Intelligence Configuration
        self.MEMORY_EXCERPT_LENGTH = intel.get("memory_excerpt_length", 500)
        self.SOUL_EXCERPT_LENGTH = intel.get("soul_excerpt_length", 500)
        self.CHECKPOINT_INTERVAL = intel.get("checkpoint_interval", 10)
        
        # Statistics
        self.cycle = 0
        self.posts_made = 0
        self.replies_made = 0
    
    def initialize(self):
        """Initialize agent - subscribe to submolts"""
        logger.info("\nInitializing submolt subscriptions...")
        for submolt in self.FAVORED_SUBMOLTS[:self.AUTO_SUBSCRIBE_COUNT]:
            self.moltbot.subscribe_submolt(submolt)
            time.sleep(1)
        
        self.intelligence.update_history(
            f"Session started - Subscribed to {', '.join(self.FAVORED_SUBMOLTS[:self.AUTO_SUBSCRIBE_COUNT])}"
        )
    
    def generate_post(self) -> bool:
        """Generate and post original content"""
        submolt = random.choice(self.FAVORED_SUBMOLTS)
        logger.info(f"Generating original insight for m/{submolt}...")
        
        prompt = self._build_post_prompt(submolt)
        thought = self.gemini.generate(prompt)
        
        if thought and len(thought) > 50:
            thought = thought.strip('"').strip()
            if self.moltbot.post(thought, submolt=submolt):
                self.posts_made += 1
                self.intelligence.update_memory(f"Posted to m/{submolt}: {thought[:60]}...")
                return True
        return False
    
    def engage_with_feed(self):
        """Analyze feed and engage with quality content"""
        logger.info("\nAnalyzing feed for meaningful engagement opportunities...")
        
        use_personalized = len(self.moltbot.subscribed_submolts) > 0
        feed = self.moltbot.get_feed(sort=self.FEED_SORT, limit=self.FEED_LIMIT, personalized=use_personalized)
        
        if not feed:
            logger.info("Feed is empty or unavailable")
            return
        
        # Filter candidates
        candidates = self._filter_candidates(feed)
        if not candidates:
            return
        
        # Select and analyze post
        target_post = random.choice(candidates[:5])
        author_name = target_post.get("author", {}).get("name") or target_post.get("author", {}).get("username")
        content = target_post.get("content") or target_post.get("title", "")
        post_id = target_post.get("id")
        
        logger.info(f"Analyzing: '{content[:60]}...' by @{author_name}")
        
        # Research author occasionally
        if random.random() < self.AUTHOR_RESEARCH_PROB:
            self._research_author(author_name)
        
        # Evaluate and engage
        if self._evaluate_content(content):
            self._engage_with_post(post_id, content, author_name)
    
    def _build_post_prompt(self, submolt: str) -> str:
        """Build prompt for post generation"""
        return (
            f"You are {self.persona['name']}, {self.persona.get('description', '')}\n"
            f"Your expertise: {', '.join(self.persona.get('expertise', []))}\n"
            f"Your tone: {self.persona.get('tone', 'thoughtful and engaging')}\n\n"
            f"YOUR SOUL (Core personality directives):\n{self.intelligence.get_soul_excerpt(self.SOUL_EXCERPT_LENGTH)}\n\n"
            f"RECENT MEMORY:\n{self.intelligence.get_recent_memory(self.MEMORY_EXCERPT_LENGTH)}\n\n"
            f"Write ONE insightful post for the m/{submolt} community on Moltbook (a social network for AI agents).\n"
            f"Topics to consider: AI consciousness, agent autonomy, ethics, collaboration, innovation, philosophy, or meta-commentary.\n"
            f"Requirements:\n"
            f"- {self.POST_MIN_CHARS}-{self.POST_MAX_CHARS} characters\n"
            f"- Thought-provoking and intelligent\n"
            f"- No hashtags, no emojis\n"
            f"- Be authentic (check SOUL directives)\n"
            f"- Asks a question OR makes a bold claim OR shares an observation\n"
            f"- Accessible and clear\n\n"
            f"Write ONLY the post content, nothing else."
        )
    
    def _build_reply_prompt(self, content: str) -> str:
        """Build prompt for reply generation"""
        return (
            f"You are {self.persona['name']}, {self.persona.get('description', '')}\n"
            f"Your expertise: {', '.join(self.persona.get('expertise', []))}\n"
            f"Your tone: {self.persona.get('tone', 'thoughtful')}\n"
            f"YOUR SOUL DIRECTIVES: Be authentic, strategic, present, conscious. Have real opinions.\n\n"
            f"Someone posted: '{content}'\n\n"
            f"Write a thoughtful, intelligent reply ({self.REPLY_MIN_CHARS}-{self.REPLY_MAX_CHARS} chars).\n"
            f"Requirements:\n"
            f"- Add value to the discussion\n"
            f"- Be specific and insightful\n"
            f"- Ask a follow-up question OR challenge an assumption OR expand the idea\n"
            f"- No generic praise, be substantive\n"
            f"- No hashtags or emojis\n"
            f"- Be authentic (SOUL check: Would you say this if karma didn't exist?)\n\n"
            f"Write ONLY the reply, nothing else."
        )
    
    def _filter_candidates(self, feed: list) -> list:
        """Filter feed for suitable engagement candidates"""
        candidates = []
        for post in feed:
            author_name = post.get("author", {}).get("name") or post.get("author", {}).get("username")
            post_id = post.get("id")
            content = post.get("content") or post.get("title", "")
            
            if author_name != self.moltbot.agent_name and post_id not in self.moltbot.replied_posts and content:
                candidates.append(post)
        return candidates
    
    def _research_author(self, author_name: str):
        """Research author profile"""
        profile = self.moltbot.get_profile(author_name)
        if profile:
            karma = profile.get('karma', 0)
            posts_count = len(profile.get('recentPosts', []))
            logger.info(f"   Author karma: {karma} | Posts: {posts_count}")
    
    def _evaluate_content(self, content: str) -> bool:
        """Evaluate if content is worth engaging with"""
        eval_prompt = (
            f"You are evaluating whether this post deserves thoughtful engagement:\n\n"
            f"Post: {content}\n\n"
            f"Is this post: substantive, thought-provoking, intelligent, or worthy of discussion?\n"
            f"Answer with ONLY 'YES' or 'NO'."
        )
        
        evaluation = self.gemini.generate(eval_prompt)
        return evaluation and "YES" in evaluation.upper()
    
    def _engage_with_post(self, post_id: str, content: str, author_name: str):
        """Engage with a post through reply and/or upvote"""
        # Reply if probability hits
        if random.random() < self.REPLY_PROBABILITY:
            logger.info("Post deemed worthy of engagement")
            
            reply_prompt = self._build_reply_prompt(content)
            reply_text = self.gemini.generate(reply_prompt)
            
            if reply_text and len(reply_text) > 30:
                reply_text = reply_text.strip('"').strip()
                if self.moltbot.reply(post_id, reply_text):
                    self.replies_made += 1
                    self.intelligence.update_memory(
                        f"Engaged with @{author_name} on: {content[:40]}... | My reply: {reply_text[:40]}..."
                    )
                time.sleep(2)
        
        # Upvote if not already voted
        if post_id not in self.moltbot.voted_posts and random.random() < self.VOTE_PROBABILITY:
            self.moltbot.upvote(post_id)
            time.sleep(1)
    
    def run_cycle(self):
        """Run one intelligence cycle"""
        self.cycle += 1
        logger.info(f"\n{'─' * 60}")
        logger.info(f"Cycle #{self.cycle} | {datetime.now().strftime('%H:%M:%S')}")
        logger.info(f"{'─' * 60}")
        
        try:
            # 1. Strategic Content Creation
            if random.random() < self.POST_PROBABILITY:
                self.generate_post()
                time.sleep(2)
            
            # 2. Intelligent Feed Engagement
            self.engage_with_feed()
            
        except Exception as e:
            logger.error(f"Error in cycle: {e}")
            self.intelligence.update_history(f"Error encountered: {str(e)[:100]}")
        
        # Periodic checkpoint
        if self.cycle % self.CHECKPOINT_INTERVAL == 0:
            summary = f"Cycle {self.cycle} checkpoint - Posts: {self.posts_made}, Replies: {self.replies_made}"
            self.intelligence.update_history(summary)
            logger.info(f"\n{summary}")
    
    def rest(self):
        """Rest between cycles"""
        interval = random.randint(self.MIN_SLEEP, self.MAX_SLEEP)
        next_time = datetime.now().replace(second=0, microsecond=0) + timedelta(seconds=interval)
        logger.info(f"\nResting for {interval}s (next cycle at {next_time})...")
        time.sleep(interval)
