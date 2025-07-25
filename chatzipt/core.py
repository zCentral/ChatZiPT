"""
Core chat functionality for ChatZiPT.
"""
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ConversationHistory:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 10):
        self.messages: List[Dict[str, str]] = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only the last max_history messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_context(self) -> List[Dict[str, str]]:
        """Get conversation context for API calls."""
        return [{"role": msg["role"], "content": msg["content"]} 
                for msg in self.messages]
    
    def clear(self):
        """Clear conversation history."""
        self.messages.clear()
    
    def save_to_file(self, filename: str):
        """Save conversation to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filename: str):
        """Load conversation from a JSON file."""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)


class ChatZiPT:
    """Main ChatZiPT application class."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.conversation = ConversationHistory()
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        # System message to define the assistant's behavior
        self.system_message = {
            "role": "system",
            "content": ("You are ChatZiPT, a helpful and friendly AI assistant. "
                       "You provide accurate, informative, and engaging responses. "
                       "Be concise but thorough in your answers.")
        }
    
    def _make_api_request(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Make a request to the OpenAI API."""
        if not self.api_key:
            return ("I don't have access to an AI service right now. "
                   "Please set your OPENAI_API_KEY environment variable to enable AI responses. "
                   "For now, I can only echo your messages back to you.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages with system message
        api_messages = [self.system_message] + messages
        
        data = {
            "model": self.model,
            "messages": api_messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"Sorry, I encountered an error while trying to respond: {e}"
        except KeyError:
            return "Sorry, I received an unexpected response format from the AI service."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    
    def chat(self, user_input: str) -> str:
        """Process user input and generate a response."""
        if not user_input.strip():
            return "Please enter a message."
        
        # Add user message to history
        self.conversation.add_message("user", user_input)
        
        # Get response from AI or provide fallback
        if self.api_key:
            response = self._make_api_request(self.conversation.get_context())
        else:
            # Simple fallback response when no API key is available
            response = f"Echo: {user_input} (AI service not configured)"
        
        if response:
            # Add assistant response to history
            self.conversation.add_message("assistant", response)
        
        return response or "I'm sorry, I couldn't generate a response."
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation.clear()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation.messages.copy()
    
    def save_conversation(self, filename: str):
        """Save the current conversation to a file."""
        self.conversation.save_to_file(filename)
    
    def load_conversation(self, filename: str):
        """Load a conversation from a file."""
        self.conversation.load_from_file(filename)
    
    def set_model(self, model: str):
        """Change the AI model being used."""
        self.model = model
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the current session."""
        messages = self.conversation.messages
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        assistant_messages = [msg for msg in messages if msg["role"] == "assistant"]
        
        return {
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "model": self.model,
            "api_configured": bool(self.api_key)
        }