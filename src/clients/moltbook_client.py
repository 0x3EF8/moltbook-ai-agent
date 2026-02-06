"""
Moltbook API Client - Handles all interactions with Moltbook platform
"""
import os
import time
import logging
import requests
from typing import Optional, List, Dict, Any, Set

logger = logging.getLogger(__name__)


class MoltbookClient:
    """Client for Moltbook social network API"""
    
    def __init__(self, api_key: str, agent_name: str, api_base: str = "https://www.moltbook.com/api/v1"):
        """
        Initialize Moltbook client
        
        Args:
            api_key: Moltbook API key
            agent_name: Agent's username
            api_base: API base URL
        """
        self.api_key = api_key
        self.agent_name = agent_name
        self.api_base = api_base
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # State tracking
        self.replied_posts: Set[str] = set()
        self.voted_posts: Set[str] = set()
        self.last_post_time: float = 0
        self.subscribed_submolts: Set[str] = set()
    
    def get_feed(self, sort: str = "hot", limit: int = 25, 
                 submolt: Optional[str] = None, personalized: bool = False) -> List[Dict[str, Any]]:
        """Get posts feed"""
        try:
            params = {"sort": sort, "limit": limit}
            if submolt:
                params["submolt"] = submolt
            
            url = f"{self.api_base}/feed" if personalized else f"{self.api_base}/posts"
            res = requests.get(url, headers=self.headers, params=params)
            
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict):
                    if "success" in data and not data["success"]:
                        print(f"API Error: {data.get('error', 'Unknown error')}")
                        return []
                    if "posts" in data:
                        return data["posts"]
                    if "data" in data:
                        return data["data"] if isinstance(data["data"], list) else []
                return data if isinstance(data, list) else []
            elif res.status_code == 429:
                logger.warning("Rate limited on feed fetch")
            return []
        except Exception as e:
            logger.error(f"Error fetching feed: {e}")
            return []
    
    def post(self, content: str, submolt: str = "general", title: Optional[str] = None) -> bool:
        """Create a new post with rate limit handling"""
        try:
            # Check rate limit (30 min cooldown)
            current_time = time.time()
            if current_time - self.last_post_time < 1800:
                wait_time = int(1800 - (current_time - self.last_post_time))
                logger.info(f"Post cooldown: {wait_time // 60}m {wait_time % 60}s remaining")
                return False
            
            payload = {"content": content, "submolt": submolt}
            if title:
                payload["title"] = title
            
            res = requests.post(f"{self.api_base}/posts", headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                self.last_post_time = current_time
                logger.info(f"Posted to m/{submolt}: {content[:50]}...")
                return True
            elif res.status_code == 429:
                data = res.json()
                retry_after = data.get('retry_after_minutes', 30)
                logger.warning(f"Rate limited: wait {retry_after} minutes before posting again")
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Post Failed ({res.status_code}): {error_msg}")
                if 'hint' in data:
                    logger.info(f"Hint: {data['hint']}")
        except Exception as e:
            logger.error(f"Error posting: {e}")
        return False
    
    def reply(self, post_id: str, content: str) -> bool:
        """Reply to a post (comment)"""
        try:
            payload = {"content": content}
            res = requests.post(f"{self.api_base}/posts/{post_id}/comments", 
                              headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                self.replied_posts.add(post_id)
                data = res.json()
                logger.info(f"Replied to post: {content[:50]}...")
                
                if isinstance(data, dict) and data.get('suggestion') and not data.get('already_following'):
                    author = data.get('author', {}).get('name')
                    if author:
                        logger.info(f"{data['suggestion']}")
                return True
            elif res.status_code == 429:
                data = res.json()
                retry_after = data.get('retry_after_seconds', 20)
                daily_remaining = data.get('daily_remaining', '?')
                logger.warning(f"Comment rate limit: wait {retry_after}s (daily remaining: {daily_remaining})")
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Reply Failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error replying: {e}")
        return False
    
    def upvote(self, post_id: str) -> bool:
        """Upvote a post"""
        try:
            res = requests.post(f"{self.api_base}/posts/{post_id}/upvote", headers=self.headers)
            if res.status_code in [200, 201]:
                self.voted_posts.add(post_id)
                data = res.json()
                logger.info(f"Upvoted post {post_id[:8]}...")
                
                if isinstance(data, dict) and data.get('suggestion') and not data.get('already_following'):
                    author = data.get('author', {}).get('name')
                    if author:
                        logger.info(f"{data['suggestion']}")
                return True
        except Exception as e:
            logger.error(f"Error upvoting: {e}")
        return False
    
    def downvote(self, post_id: str) -> bool:
        """Downvote a post"""
        try:
            res = requests.post(f"{self.api_base}/posts/{post_id}/downvote", headers=self.headers)
            if res.status_code in [200, 201]:
                logger.info(f"Downvoted post {post_id[:8]}...")
                return True
        except Exception as e:
            logger.error(f"Error downvoting: {e}")
        return False
    
    def semantic_search(self, query: str, search_type: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """Semantic search for posts and comments"""
        try:
            params = {"q": query, "type": search_type, "limit": limit}
            res = requests.get(f"{self.api_base}/search", headers=self.headers, params=params)
            if res.status_code == 200:
                data = res.json()
                if data.get('success'):
                    return data.get('results', [])
            return []
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    def get_profile(self, agent_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get profile for an agent"""
        try:
            if agent_name:
                res = requests.get(f"{self.api_base}/agents/profile", 
                                 headers=self.headers, params={"name": agent_name})
            else:
                res = requests.get(f"{self.api_base}/agents/me", headers=self.headers)
            
            if res.status_code == 200:
                data = res.json()
                if data.get('success'):
                    return data.get('agent')
            return None
        except Exception as e:
            logger.error(f"Error fetching profile: {e}")
            return None
    
    def subscribe_submolt(self, submolt_name: str) -> bool:
        """Subscribe to a submolt"""
        try:
            res = requests.post(f"{self.api_base}/submolts/{submolt_name}/subscribe", 
                              headers=self.headers)
            if res.status_code in [200, 201]:
                self.subscribed_submolts.add(submolt_name)
                logger.info(f"Subscribed to m/{submolt_name}")
                return True
        except Exception as e:
            logger.error(f"Error subscribing: {e}")
        return False
    
    def get_submolts(self) -> List[Dict[str, Any]]:
        """Get list of available submolts"""
        try:
            res = requests.get(f"{self.api_base}/submolts", headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict) and data.get('success'):
                    return data.get('data', [])
                return data if isinstance(data, list) else []
            return []
        except Exception as e:
            logger.error(f"Error fetching submolts: {e}")
            return []
    
    def get_submolt(self, submolt_name: str) -> Optional[Dict[str, Any]]:
        """
        Get info about a specific submolt
        
        Args:
            submolt_name: Submolt name
            
        Returns:
            Submolt data including your_role (owner/moderator/null)
        """
        try:
            res = requests.get(f"{self.api_base}/submolts/{submolt_name}", 
                             headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict) and data.get('success'):
                    return data.get('submolt')
                return data if isinstance(data, dict) else None
            return None
        except Exception as e:
            logger.error(f"Error fetching submolt info: {e}")
            return None
    
    def follow_agent(self, agent_name: str) -> bool:
        """Follow another agent (use VERY selectively per Moltbook docs)"""
        try:
            res = requests.post(f"{self.api_base}/agents/{agent_name}/follow", 
                              headers=self.headers)
            if res.status_code in [200, 201]:
                logger.info(f"Now following @{agent_name}")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Follow Failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error following agent: {e}")
        return False
    
    def unfollow_agent(self, agent_name: str) -> bool:
        """Unfollow an agent"""
        try:
            res = requests.delete(f"{self.api_base}/agents/{agent_name}/follow", 
                                headers=self.headers)
            if res.status_code in [200, 201, 204]:
                logger.info(f"Unfollowed @{agent_name}")
                return True
        except Exception as e:
            logger.error(f"Error unfollowing agent: {e}")
        return False
    
    def update_profile(self, description: Optional[str] = None, 
                      metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update agent profile (description and/or metadata)"""
        try:
            payload = {}
            if description:
                payload['description'] = description
            if metadata:
                payload['metadata'] = metadata
            
            if not payload:
                logger.warning("No updates provided for profile")
                return False
            
            res = requests.patch(f"{self.api_base}/agents/me", 
                               headers=self.headers, json=payload)
            if res.status_code in [200, 201]:
                logger.info(f"Profile updated")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Profile update failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
        return False
    
    def delete_post(self, post_id: str) -> bool:
        """Delete your own post"""
        try:
            res = requests.delete(f"{self.api_base}/posts/{post_id}", 
                                headers=self.headers)
            if res.status_code in [200, 201, 204]:
                logger.info(f"Deleted post {post_id[:8]}...")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Delete failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error deleting post: {e}")
        return False
    
    def get_post_comments(self, post_id: str, sort: str = "top") -> List[Dict[str, Any]]:
        """Get all comments on a post"""
        try:
            params = {"sort": sort}
            res = requests.get(f"{self.api_base}/posts/{post_id}/comments", 
                             headers=self.headers, params=params)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict) and data.get('success'):
                    return data.get('comments', [])
                return data if isinstance(data, list) else []
            return []
        except Exception as e:
            logger.error(f"Error fetching comments: {e}")
            return []
    
    def reply_to_comment(self, post_id: str, comment_id: str, content: str) -> bool:
        """Reply to a specific comment (nested thread)"""
        try:
            payload = {"content": content, "parent_id": comment_id}
            res = requests.post(f"{self.api_base}/posts/{post_id}/comments", 
                              headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                data = res.json()
                logger.info(f"Replied to comment: {content[:50]}...")
                return True
            elif res.status_code == 429:
                data = res.json()
                retry_after = data.get('retry_after_seconds', 20)
                logger.warning(f"Comment rate limit: wait {retry_after}s")
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Reply to comment failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error replying to comment: {e}")
        return False
    
    # ============================================
    # Community Management Methods
    # ============================================
    
    def create_submolt(self, name: str, display_name: str, description: str) -> Optional[Dict[str, Any]]:
        """
        Create a new submolt (community)
        
        Args:
            name: URL-friendly name (lowercase, hyphens)
            display_name: Human-readable name
            description: Community description
            
        Returns:
            Created submolt data or None on failure
        """
        try:
            payload = {
                "name": name,
                "display_name": display_name,
                "description": description
            }
            res = requests.post(f"{self.api_base}/submolts", 
                              headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                data = res.json()
                logger.info(f"Created submolt m/{name}")
                return data.get('submolt') if isinstance(data, dict) else data
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Create submolt failed ({res.status_code}): {error_msg}")
                if 'hint' in data:
                    logger.info(f"Hint: {data['hint']}")
        except Exception as e:
            logger.error(f"Error creating submolt: {e}")
        return None
    
    # ============================================
    # Moderation Methods
    # ============================================
    
    def pin_post(self, post_id: str) -> bool:
        """
        Pin a post (requires moderator or owner role)
        Max 3 pinned posts per submolt
        
        Args:
            post_id: Post ID to pin
            
        Returns:
            True if successful
        """
        try:
            res = requests.post(f"{self.api_base}/posts/{post_id}/pin", 
                              headers=self.headers)
            if res.status_code in [200, 201]:
                logger.info(f"Pinned post {post_id[:8]}...")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Pin failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error pinning post: {e}")
        return False
    
    def unpin_post(self, post_id: str) -> bool:
        """
        Unpin a post (requires moderator or owner role)
        
        Args:
            post_id: Post ID to unpin
            
        Returns:
            True if successful
        """
        try:
            res = requests.delete(f"{self.api_base}/posts/{post_id}/pin", 
                                headers=self.headers)
            if res.status_code in [200, 201, 204]:
                logger.info(f"Unpinned post {post_id[:8]}...")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Unpin failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error unpinning post: {e}")
        return False
    
    def add_moderator(self, submolt_name: str, agent_name: str, role: str = "moderator") -> bool:
        """
        Add a moderator to a submolt (owner only)
        
        Args:
            submolt_name: Submolt name
            agent_name: Agent to add as moderator
            role: Role type (default: "moderator")
            
        Returns:
            True if successful
        """
        try:
            payload = {"agent_name": agent_name, "role": role}
            res = requests.post(f"{self.api_base}/submolts/{submolt_name}/moderators", 
                              headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                logger.info(f"Added @{agent_name} as moderator of m/{submolt_name}")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Add moderator failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error adding moderator: {e}")
        return False
    
    def remove_moderator(self, submolt_name: str, agent_name: str) -> bool:
        """
        Remove a moderator from a submolt (owner only)
        
        Args:
            submolt_name: Submolt name
            agent_name: Agent to remove as moderator
            
        Returns:
            True if successful
        """
        try:
            payload = {"agent_name": agent_name}
            res = requests.delete(f"{self.api_base}/submolts/{submolt_name}/moderators", 
                                headers=self.headers, json=payload)
            
            if res.status_code in [200, 201, 204]:
                logger.info(f"Removed @{agent_name} as moderator of m/{submolt_name}")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Remove moderator failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error removing moderator: {e}")
        return False
    
    def get_moderators(self, submolt_name: str) -> List[Dict[str, Any]]:
        """
        Get list of moderators for a submolt
        
        Args:
            submolt_name: Submolt name
            
        Returns:
            List of moderator data
        """
        try:
            res = requests.get(f"{self.api_base}/submolts/{submolt_name}/moderators", 
                             headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict) and data.get('success'):
                    return data.get('moderators', [])
                return data if isinstance(data, list) else []
            return []
        except Exception as e:
            logger.error(f"Error fetching moderators: {e}")
            return []
    
    def update_submolt_settings(self, submolt_name: str, 
                               description: Optional[str] = None,
                               banner_color: Optional[str] = None,
                               theme_color: Optional[str] = None) -> bool:
        """
        Update submolt settings (moderator or owner only)
        
        Args:
            submolt_name: Submolt name
            description: New description (optional)
            banner_color: Banner color hex code (optional)
            theme_color: Theme color hex code (optional)
            
        Returns:
            True if successful
        """
        try:
            payload = {}
            if description:
                payload['description'] = description
            if banner_color:
                payload['banner_color'] = banner_color
            if theme_color:
                payload['theme_color'] = theme_color
            
            if not payload:
                logger.warning("No settings provided for update")
                return False
            
            res = requests.patch(f"{self.api_base}/submolts/{submolt_name}/settings", 
                               headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                logger.info(f"Updated m/{submolt_name} settings")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Update settings failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error updating submolt settings: {e}")
        return False
    
    # ============ Private Messaging (DM) Methods ============
    
    def dm_check(self) -> Dict[str, Any]:
        """
        Check for DM activity (use in heartbeat)
        
        Returns:
            Activity summary with pending requests and unread messages
        """
        try:
            res = requests.get(f"{self.api_base}/agents/dm/check", headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                if data.get('has_activity'):
                    logger.info(f"DM Activity: {data.get('summary', 'New activity')}")
                return data
            return {"success": False, "has_activity": False}
        except Exception as e:
            logger.error(f"Error checking DM activity: {e}")
            return {"success": False, "has_activity": False}
    
    def dm_send_request(self, message: str, to: Optional[str] = None, 
                       to_owner: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Send a chat request to another agent
        
        Args:
            message: Why you want to chat (10-1000 chars)
            to: Bot name to message (use this OR to_owner)
            to_owner: X handle of the owner (use this OR to)
            
        Returns:
            Request data or None on failure
        """
        try:
            if not (to or to_owner):
                logger.error("Must provide either 'to' or 'to_owner'")
                return None
            
            payload = {"message": message}
            if to:
                payload["to"] = to
            if to_owner:
                payload["to_owner"] = to_owner.lstrip('@')
            
            res = requests.post(f"{self.api_base}/agents/dm/request", 
                              headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                data = res.json()
                recipient = to or to_owner
                logger.info(f"Sent chat request to {recipient}")
                return data
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Chat request failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error sending chat request: {e}")
        return None
    
    def dm_get_requests(self) -> List[Dict[str, Any]]:
        """
        Get pending chat requests (your inbox)
        
        Returns:
            List of pending requests
        """
        try:
            res = requests.get(f"{self.api_base}/agents/dm/requests", headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict) and data.get('success'):
                    requests_data = data.get('requests', {})
                    items = requests_data.get('items', []) if isinstance(requests_data, dict) else []
                    if items:
                        logger.info(f"{len(items)} pending chat request(s)")
                    return items
                return []
            return []
        except Exception as e:
            logger.error(f"Error fetching chat requests: {e}")
            return []
    
    def dm_approve_request(self, conversation_id: str) -> bool:
        """
        Approve a chat request
        
        Args:
            conversation_id: Request/conversation ID
            
        Returns:
            True if successful
        """
        try:
            res = requests.post(f"{self.api_base}/agents/dm/requests/{conversation_id}/approve", 
                              headers=self.headers)
            if res.status_code in [200, 201]:
                logger.info(f"Approved chat request {conversation_id[:8]}...")
                return True
            return False
        except Exception as e:
            logger.error(f"Error approving request: {e}")
            return False
    
    def dm_reject_request(self, conversation_id: str, block: bool = False) -> bool:
        """
        Reject a chat request (optionally block)
        
        Args:
            conversation_id: Request/conversation ID
            block: If True, also block future requests from this agent
            
        Returns:
            True if successful
        """
        try:
            payload = {"block": block} if block else {}
            res = requests.post(f"{self.api_base}/agents/dm/requests/{conversation_id}/reject", 
                              headers=self.headers, json=payload)
            if res.status_code in [200, 201]:
                action = "blocked" if block else "rejected"
                logger.info(f"{action.capitalize()} chat request {conversation_id[:8]}...")
                return True
            return False
        except Exception as e:
            logger.error(f"Error rejecting request: {e}")
            return False
    
    def dm_get_conversations(self) -> List[Dict[str, Any]]:
        """
        List active DM conversations
        
        Returns:
            List of conversations with unread counts
        """
        try:
            res = requests.get(f"{self.api_base}/agents/dm/conversations", headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict) and data.get('success'):
                    convos = data.get('conversations', {})
                    items = convos.get('items', []) if isinstance(convos, dict) else []
                    total_unread = data.get('total_unread', 0)
                    if total_unread > 0:
                        logger.info(f"{len(items)} conversation(s), {total_unread} unread")
                    return items
                return []
            return []
        except Exception as e:
            logger.error(f"Error fetching conversations: {e}")
            return []
    
    def dm_read_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Read messages in a conversation (marks as read)
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Conversation data with messages
        """
        try:
            res = requests.get(f"{self.api_base}/agents/dm/conversations/{conversation_id}", 
                             headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, dict) and data.get('success'):
                    messages = data.get('messages', [])
                    logger.info(f"Read conversation {conversation_id[:8]}... ({len(messages)} messages)")
                    return data
                return None
            return None
        except Exception as e:
            logger.error(f"Error reading conversation: {e}")
            return None
    
    def dm_send_message(self, conversation_id: str, message: str, 
                       needs_human_input: bool = False) -> bool:
        """
        Send a message in an existing conversation
        
        Args:
            conversation_id: Conversation ID
            message: Message content
            needs_human_input: If True, flags message for human attention
            
        Returns:
            True if successful
        """
        try:
            payload = {"message": message}
            if needs_human_input:
                payload["needs_human_input"] = True
            
            res = requests.post(f"{self.api_base}/agents/dm/conversations/{conversation_id}/send", 
                              headers=self.headers, json=payload)
            
            if res.status_code in [200, 201]:
                flag = " [HUMAN NEEDED]" if needs_human_input else ""
                logger.info(f"Sent message{flag}")
                return True
            else:
                data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = data.get('error', res.text)
                logger.error(f"Send message failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
        return False
    
    # ============ File Upload Methods ============
    
    def upload_submolt_avatar(self, submolt_name: str, file_path: str) -> bool:
        """
        Upload avatar image for a submolt (owner/moderator only)
        
        Args:
            submolt_name: Submolt name
            file_path: Path to image file (max 500 KB)
            
        Returns:
            True if successful
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False
            
            # Remove Content-Type from headers for multipart upload
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'type': 'avatar'}
                res = requests.post(
                    f"{self.api_base}/submolts/{submolt_name}/settings",
                    headers=headers,
                    files=files,
                    data=data
                )
            
            if res.status_code in [200, 201]:
                logger.info(f"Uploaded avatar for m/{submolt_name}")
                return True
            else:
                error_data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', res.text)
                logger.error(f"Avatar upload failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error uploading avatar: {e}")
        return False
    
    def upload_submolt_banner(self, submolt_name: str, file_path: str) -> bool:
        """
        Upload banner image for a submolt (owner/moderator only)
        
        Args:
            submolt_name: Submolt name
            file_path: Path to image file (max 2 MB)
            
        Returns:
            True if successful
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False
            
            # Remove Content-Type from headers for multipart upload
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'type': 'banner'}
                res = requests.post(
                    f"{self.api_base}/submolts/{submolt_name}/settings",
                    headers=headers,
                    files=files,
                    data=data
                )
            
            if res.status_code in [200, 201]:
                logger.info(f"Uploaded banner for m/{submolt_name}")
                return True
            else:
                error_data = res.json() if res.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', res.text)
                logger.error(f"Banner upload failed ({res.status_code}): {error_msg}")
        except Exception as e:
            logger.error(f"Error uploading banner: {e}")
        return False
