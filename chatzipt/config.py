"""
Configuration management for ChatZiPT.
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for ChatZiPT."""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """Load configuration from environment variables."""
        # API Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.default_model = os.getenv("CHATZIPT_MODEL", "gpt-3.5-turbo")
        
        # Chat Configuration
        self.max_history = int(os.getenv("CHATZIPT_MAX_HISTORY", "10"))
        self.temperature = float(os.getenv("CHATZIPT_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("CHATZIPT_MAX_TOKENS", "1000"))
        
        # File Configuration
        self.conversations_dir = os.getenv("CHATZIPT_CONVERSATIONS_DIR", "conversations")
        
        # Create conversations directory if it doesn't exist
        if not os.path.exists(self.conversations_dir):
            os.makedirs(self.conversations_dir, exist_ok=True)
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API-related configuration."""
        return {
            "api_key": self.openai_api_key,
            "model": self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_chat_config(self) -> Dict[str, Any]:
        """Get chat-related configuration."""
        return {
            "max_history": self.max_history,
            "conversations_dir": self.conversations_dir
        }
    
    def is_api_configured(self) -> bool:
        """Check if API is properly configured."""
        return bool(self.openai_api_key)
    
    def set_api_key(self, api_key: str):
        """Set the API key."""
        self.openai_api_key = api_key
        os.environ["OPENAI_API_KEY"] = api_key
    
    def get_conversation_path(self, filename: str) -> str:
        """Get full path for a conversation file."""
        if not filename.endswith('.json'):
            filename += '.json'
        return os.path.join(self.conversations_dir, filename)


# Global configuration instance
config = Config()