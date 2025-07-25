"""
Command Line Interface for ChatZiPT.
"""
import argparse
import os
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from colorama import init, Fore, Style

from .core import ChatZiPT

# Initialize colorama for Windows compatibility
init()


class ChatZiPTCLI:
    """Command line interface for ChatZiPT."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.console = Console()
        self.chat = ChatZiPT(api_key=api_key, model=model)
        self.running = True
    
    def print_welcome(self):
        """Print welcome message."""
        welcome_text = """
# Welcome to ChatZiPT! 🤖

A Python-based AI chat application. Type your messages and press Enter to chat.

**Available commands:**
- `/help` - Show available commands
- `/clear` - Clear conversation history
- `/save <filename>` - Save conversation to file
- `/load <filename>` - Load conversation from file
- `/model <model_name>` - Change AI model
- `/stats` - Show session statistics
- `/quit` or `/exit` - Exit the application

Start chatting by typing a message!
        """
        
        panel = Panel(
            Markdown(welcome_text),
            title="ChatZiPT",
            border_style="blue"
        )
        self.console.print(panel)
        
        # Show API status
        if self.chat.api_key:
            self.console.print("✅ AI service configured", style="green")
        else:
            self.console.print("⚠️  AI service not configured (set OPENAI_API_KEY environment variable)", style="yellow")
        self.console.print()
    
    def print_help(self):
        """Print help information."""
        help_text = """
**Available Commands:**

- `/help` - Show this help message
- `/clear` - Clear conversation history
- `/save <filename>` - Save conversation to JSON file
- `/load <filename>` - Load conversation from JSON file
- `/model <model_name>` - Change AI model (e.g., gpt-4, gpt-3.5-turbo)
- `/stats` - Show session statistics
- `/quit` or `/exit` - Exit the application

**Tips:**
- Use Ctrl+C to exit at any time
- Your conversation history is maintained during the session
- Save important conversations before exiting
        """
        panel = Panel(Markdown(help_text), title="Help", border_style="cyan")
        self.console.print(panel)
    
    def handle_command(self, command: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        command = command.strip()
        
        if command in ["/quit", "/exit"]:
            self.console.print("👋 Goodbye! Thanks for using ChatZiPT!", style="blue")
            self.running = False
            return True
        
        elif command == "/help":
            self.print_help()
            return True
        
        elif command == "/clear":
            self.chat.clear_conversation()
            self.console.print("🗑️  Conversation history cleared!", style="green")
            return True
        
        elif command.startswith("/save "):
            filename = command[6:].strip()
            if filename:
                try:
                    self.chat.save_conversation(filename)
                    self.console.print(f"💾 Conversation saved to {filename}", style="green")
                except Exception as e:
                    self.console.print(f"❌ Error saving conversation: {e}", style="red")
            else:
                self.console.print("❌ Please specify a filename: /save <filename>", style="red")
            return True
        
        elif command.startswith("/load "):
            filename = command[6:].strip()
            if filename:
                try:
                    if os.path.exists(filename):
                        self.chat.load_conversation(filename)
                        self.console.print(f"📂 Conversation loaded from {filename}", style="green")
                    else:
                        self.console.print(f"❌ File not found: {filename}", style="red")
                except Exception as e:
                    self.console.print(f"❌ Error loading conversation: {e}", style="red")
            else:
                self.console.print("❌ Please specify a filename: /load <filename>", style="red")
            return True
        
        elif command.startswith("/model "):
            model = command[7:].strip()
            if model:
                self.chat.set_model(model)
                self.console.print(f"🔧 Model changed to: {model}", style="green")
            else:
                self.console.print("❌ Please specify a model: /model <model_name>", style="red")
            return True
        
        elif command == "/stats":
            stats = self.chat.get_stats()
            stats_text = f"""
**Session Statistics:**

- Total messages: {stats['total_messages']}
- Your messages: {stats['user_messages']}
- Assistant messages: {stats['assistant_messages']}
- Current model: {stats['model']}
- API configured: {'Yes' if stats['api_configured'] else 'No'}
            """
            panel = Panel(Markdown(stats_text), title="Statistics", border_style="magenta")
            self.console.print(panel)
            return True
        
        return False
    
    def run_interactive(self):
        """Run the interactive chat interface."""
        self.print_welcome()
        
        try:
            while self.running:
                # Get user input
                try:
                    user_input = input(f"{Fore.CYAN}You: {Style.RESET_ALL}").strip()
                except EOFError:
                    break
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith("/"):
                    self.handle_command(user_input)
                    continue
                
                # Process chat message
                self.console.print(f"{Fore.YELLOW}ChatZiPT: {Style.RESET_ALL}", end="")
                
                # Get response from ChatZiPT
                response = self.chat.chat(user_input)
                
                # Display response with rich formatting
                if response:
                    # Try to render as markdown if it contains markdown-like formatting
                    if any(char in response for char in ['*', '`', '#', '-', '>']):
                        try:
                            self.console.print(Markdown(response))
                        except:
                            self.console.print(response)
                    else:
                        self.console.print(response)
                else:
                    self.console.print("I'm sorry, I couldn't generate a response.", style="red")
                
                self.console.print()  # Add spacing
        
        except KeyboardInterrupt:
            self.console.print("\n👋 Goodbye! Thanks for using ChatZiPT!", style="blue")
        except Exception as e:
            self.console.print(f"\n❌ An unexpected error occurred: {e}", style="red")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="ChatZiPT - A Python-based AI chat application",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (can also be set via OPENAI_API_KEY environment variable)"
    )
    
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="AI model to use (default: gpt-3.5-turbo)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="ChatZiPT 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Initialize and run CLI
    cli = ChatZiPTCLI(api_key=args.api_key, model=args.model)
    cli.run_interactive()


if __name__ == "__main__":
    main()