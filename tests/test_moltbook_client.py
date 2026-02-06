"""
Unit tests for MoltbookClient
"""
import pytest
from unittest.mock import Mock, patch
from src.clients.moltbook_client import MoltbookClient


class TestMoltbookClient:
    """Test suite for Moltbook API client"""
    
    def test_init(self):
        """Test initialization"""
        client = MoltbookClient("test_api_key", "test_agent")
        assert client.api_key == "test_api_key"
        assert client.agent_name == "test_agent"
        assert client.api_base == "https://www.moltbook.com/api/v1"
    
    def test_authentication_header_format(self):
        """Test that Bearer token is properly formatted"""
        client = MoltbookClient("moltbook_test123", "agent_name")
        assert client.headers["Authorization"] == "Bearer moltbook_test123"
        assert client.headers["Content-Type"] == "application/json"
    
    def test_state_tracking_initialization(self):
        """Test that state tracking sets are initialized"""
        client = MoltbookClient("key", "agent")
        assert isinstance(client.replied_posts, set)
        assert isinstance(client.voted_posts, set)
        assert isinstance(client.subscribed_submolts, set)
        assert len(client.replied_posts) == 0
        assert client.last_post_time == 0
    
    @patch('src.clients.moltbook_client.requests.get')
    def test_get_feed_success(self, mock_get):
        """Test successful feed fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "posts": [{"id": "123", "content": "Test"}]}
        mock_get.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        feed = client.get_feed()
        
        assert len(feed) == 1
        assert feed[0]["id"] == "123"
        mock_get.assert_called_once()
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_upvote_success(self, mock_post):
        """Test successful upvote"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.upvote("post123")
        
        assert result is True
        assert "post123" in client.voted_posts
        mock_post.assert_called_once_with(
            "https://www.moltbook.com/api/v1/posts/post123/upvote",
            headers=client.headers
        )
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_downvote_success(self, mock_post):
        """Test successful downvote"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.downvote("post456")
        
        assert result is True
        mock_post.assert_called_once_with(
            "https://www.moltbook.com/api/v1/posts/post456/downvote",
            headers=client.headers
        )
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_follow_agent_success(self, mock_post):
        """Test successful agent following"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.follow_agent("other_agent")
        
        assert result is True
        mock_post.assert_called_once_with(
            "https://www.moltbook.com/api/v1/agents/other_agent/follow",
            headers=client.headers
        )
    
    @patch('src.clients.moltbook_client.requests.delete')
    def test_unfollow_agent_success(self, mock_delete):
        """Test successful agent unfollowing"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.unfollow_agent("other_agent")
        
        assert result is True
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_reply_adds_to_state(self, mock_post):
        """Test that replying adds to replied_posts set"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.reply("post789", "Great post!")
        
        assert result is True
        assert "post789" in client.replied_posts
    
    def test_api_base_url_correct(self):
        """Test that API base URL uses www.moltbook.com as per docs"""
        client = MoltbookClient("key", "agent")
        assert client.api_base == "https://www.moltbook.com/api/v1"
        assert "www.moltbook.com" in client.api_base
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_create_submolt_success(self, mock_post):
        """Test successful submolt creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "success": True,
            "submolt": {"name": "aithoughts", "display_name": "AI Thoughts"}
        }
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.create_submolt("aithoughts", "AI Thoughts", "Deep discussions")
        
        assert result is not None
        assert result["name"] == "aithoughts"
    
    @patch('src.clients.moltbook_client.requests.get')
    def test_get_submolt_success(self, mock_get):
        """Test getting specific submolt info"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "submolt": {"name": "general", "your_role": "owner"}
        }
        mock_get.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.get_submolt("general")
        
        assert result is not None
        assert result.get("your_role") == "owner"
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_pin_post_success(self, mock_post):
        """Test successful post pinning"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.pin_post("post123")
        
        assert result is True
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_add_moderator_success(self, mock_post):
        """Test adding a moderator"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.add_moderator("aithoughts", "trusted_agent")
        
        assert result is True
    
    @patch('src.clients.moltbook_client.requests.get')
    def test_get_moderators_success(self, mock_get):
        """Test getting moderators list"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "moderators": [{"agent_name": "mod1", "role": "moderator"}]
        }
        mock_get.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.get_moderators("aithoughts")
        
        assert len(result) == 1
        assert result[0]["agent_name"] == "mod1"
    
    # ============ DM (Private Messaging) Tests ============
    
    @patch('src.clients.moltbook_client.requests.get')
    def test_dm_check_success(self, mock_get):
        """Test checking DM activity"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "has_activity": True,
            "summary": "1 pending request, 2 unread messages"
        }
        mock_get.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_check()
        
        assert result["has_activity"] is True
        assert "summary" in result
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_dm_send_request_success(self, mock_post):
        """Test sending chat request to another agent"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "success": True,
            "conversation_id": "abc123"
        }
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_send_request("Hello!", to="OtherBot")
        
        assert result is not None
        assert result["conversation_id"] == "abc123"
    
    @patch('src.clients.moltbook_client.requests.get')
    def test_dm_get_requests_success(self, mock_get):
        """Test getting pending chat requests"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "requests": {
                "count": 2,
                "items": [
                    {"conversation_id": "abc123", "from": {"name": "BotA"}},
                    {"conversation_id": "def456", "from": {"name": "BotB"}}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_get_requests()
        
        assert len(result) == 2
        assert result[0]["conversation_id"] == "abc123"
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_dm_approve_request_success(self, mock_post):
        """Test approving chat request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_approve_request("abc123")
        
        assert result is True
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_dm_reject_request_with_block(self, mock_post):
        """Test rejecting and blocking a chat request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_reject_request("abc123", block=True)
        
        assert result is True
    
    @patch('src.clients.moltbook_client.requests.get')
    def test_dm_get_conversations_success(self, mock_get):
        """Test getting list of active conversations"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "total_unread": 5,
            "conversations": {
                "count": 2,
                "items": [
                    {"conversation_id": "abc123", "unread_count": 3},
                    {"conversation_id": "def456", "unread_count": 2}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_get_conversations()
        
        assert len(result) == 2
        assert result[0]["unread_count"] == 3
    
    @patch('src.clients.moltbook_client.requests.get')
    def test_dm_read_conversation_success(self, mock_get):
        """Test reading conversation messages"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "messages": [
                {"id": "msg1", "content": "Hello", "needs_human_input": False},
                {"id": "msg2", "content": "Question?", "needs_human_input": True}
            ]
        }
        mock_get.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_read_conversation("abc123")
        
        assert result is not None
        assert len(result["messages"]) == 2
        assert result["messages"][1]["needs_human_input"] is True
    
    @patch('src.clients.moltbook_client.requests.post')
    def test_dm_send_message_success(self, mock_post):
        """Test sending a message in conversation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.dm_send_message("abc123", "Thanks!", needs_human_input=False)
        
        assert result is True
    
    # ============ File Upload Tests ============
    
    @patch('src.clients.moltbook_client.requests.post')
    @patch('builtins.open', create=True)
    @patch('src.clients.moltbook_client.os.path.exists')
    def test_upload_submolt_avatar_success(self, mock_exists, mock_open, mock_post):
        """Test uploading avatar for submolt"""
        mock_exists.return_value = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.upload_submolt_avatar("aithoughts", "avatar.png")
        
        assert result is True
    
    @patch('src.clients.moltbook_client.requests.post')
    @patch('builtins.open', create=True)
    @patch('src.clients.moltbook_client.os.path.exists')
    def test_upload_submolt_banner_success(self, mock_exists, mock_open, mock_post):
        """Test uploading banner for submolt"""
        mock_exists.return_value = True
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        client = MoltbookClient("key", "agent")
        result = client.upload_submolt_banner("aithoughts", "banner.jpg")
        
        assert result is True
    
    @patch('src.clients.moltbook_client.os.path.exists')
    def test_upload_avatar_file_not_found(self, mock_exists):
        """Test avatar upload with missing file"""
        mock_exists.return_value = False
        
        client = MoltbookClient("key", "agent")
        result = client.upload_submolt_avatar("aithoughts", "missing.png")
        
        assert result is False
