"""
Tests for ChatZiPT core functionality.
"""
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock

from chatzipt.core import ChatZiPT, ConversationHistory


class TestConversationHistory:
    """Test ConversationHistory class."""
    
    def test_add_message(self):
        """Test adding messages to history."""
        history = ConversationHistory(max_history=3)
        
        history.add_message("user", "Hello")
        assert len(history.messages) == 1
        assert history.messages[0]["role"] == "user"
        assert history.messages[0]["content"] == "Hello"
    
    def test_max_history_limit(self):
        """Test that history is limited to max_history."""
        history = ConversationHistory(max_history=2)
        
        history.add_message("user", "Message 1")
        history.add_message("assistant", "Response 1")
        history.add_message("user", "Message 2")
        
        assert len(history.messages) == 2
        # First message should be removed
        assert history.messages[0]["content"] == "Response 1"
        assert history.messages[1]["content"] == "Message 2"
    
    def test_get_context(self):
        """Test getting context for API calls."""
        history = ConversationHistory()
        
        history.add_message("user", "Hello")
        history.add_message("assistant", "Hi there!")
        
        context = history.get_context()
        assert len(context) == 2
        assert context[0] == {"role": "user", "content": "Hello"}
        assert context[1] == {"role": "assistant", "content": "Hi there!"}
    
    def test_clear(self):
        """Test clearing history."""
        history = ConversationHistory()
        history.add_message("user", "Hello")
        
        assert len(history.messages) == 1
        history.clear()
        assert len(history.messages) == 0
    
    def test_save_and_load(self):
        """Test saving and loading conversation."""
        history = ConversationHistory()
        history.add_message("user", "Hello")
        history.add_message("assistant", "Hi!")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save conversation
            history.save_to_file(temp_file)
            
            # Load into new history object
            new_history = ConversationHistory()
            new_history.load_from_file(temp_file)
            
            assert len(new_history.messages) == 2
            assert new_history.messages[0]["content"] == "Hello"
            assert new_history.messages[1]["content"] == "Hi!"
        
        finally:
            os.unlink(temp_file)


class TestChatZiPT:
    """Test ChatZiPT class."""
    
    def test_init_without_api_key(self):
        """Test initialization without API key."""
        chat = ChatZiPT()
        assert chat.api_key is None
        assert chat.model == "gpt-3.5-turbo"
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        chat = ChatZiPT(api_key="test-key", model="gpt-4")
        assert chat.api_key == "test-key"
        assert chat.model == "gpt-4"
    
    def test_chat_without_api_key(self):
        """Test chat functionality without API key."""
        chat = ChatZiPT()
        response = chat.chat("Hello")
        
        assert "Echo: Hello" in response
        assert len(chat.conversation.messages) == 2  # user + assistant
    
    def test_empty_input(self):
        """Test chat with empty input."""
        chat = ChatZiPT()
        response = chat.chat("")
        
        assert response == "Please enter a message."
    
    def test_clear_conversation(self):
        """Test clearing conversation."""
        chat = ChatZiPT()
        chat.chat("Hello")
        
        assert len(chat.conversation.messages) == 2
        chat.clear_conversation()
        assert len(chat.conversation.messages) == 0
    
    def test_get_conversation_history(self):
        """Test getting conversation history."""
        chat = ChatZiPT()
        chat.chat("Hello")
        
        history = chat.get_conversation_history()
        assert len(history) == 2
        assert isinstance(history, list)
    
    def test_set_model(self):
        """Test changing model."""
        chat = ChatZiPT()
        chat.set_model("gpt-4")
        
        assert chat.model == "gpt-4"
    
    def test_get_stats(self):
        """Test getting session statistics."""
        chat = ChatZiPT()
        chat.chat("Hello")
        
        stats = chat.get_stats()
        assert stats["total_messages"] == 2
        assert stats["user_messages"] == 1
        assert stats["assistant_messages"] == 1
        assert stats["model"] == "gpt-3.5-turbo"
        assert stats["api_configured"] == False
    
    @patch('requests.post')
    def test_api_request_success(self, mock_post):
        """Test successful API request."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello! How can I help you?"}}]
        }
        mock_post.return_value = mock_response
        
        chat = ChatZiPT(api_key="test-key")
        response = chat.chat("Hello")
        
        assert response == "Hello! How can I help you?"
        assert len(chat.conversation.messages) == 2
    
    @patch('requests.post')
    def test_api_request_failure(self, mock_post):
        """Test API request failure."""
        # Mock failed API request
        mock_post.side_effect = Exception("Network error")
        
        chat = ChatZiPT(api_key="test-key")
        response = chat.chat("Hello")
        
        assert "unexpected error occurred" in response
    
    def test_save_and_load_conversation(self):
        """Test saving and loading conversation."""
        chat = ChatZiPT()
        chat.chat("Hello")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save conversation
            chat.save_conversation(temp_file)
            
            # Create new chat and load conversation
            new_chat = ChatZiPT()
            new_chat.load_conversation(temp_file)
            
            assert len(new_chat.conversation.messages) == 2
        
        finally:
            os.unlink(temp_file)