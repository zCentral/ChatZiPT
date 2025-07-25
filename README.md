# ChatZiPT 🤖

A Python-based AI chat application that provides an interactive command-line interface for chatting with AI models.

## Features

- 💬 Interactive command-line chat interface
- 🧠 Support for multiple OpenAI models (GPT-3.5, GPT-4, etc.)
- 📚 Conversation history management
- 💾 Save and load conversations
- 🎨 Rich text formatting and markdown support
- ⚙️ Configurable settings
- 📊 Session statistics

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/zCentral/ChatZiPT.git
cd ChatZiPT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

### Using pip (when published)

```bash
pip install chatzipt
```

## Configuration

### API Key Setup

You'll need an OpenAI API key to use AI features. You can get one from [OpenAI's website](https://platform.openai.com/api-keys).

Set your API key using one of these methods:

1. **Environment variable** (recommended):
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. **`.env` file** in the project directory:
```
OPENAI_API_KEY=your-api-key-here
```

3. **Command line argument**:
```bash
chatzipt --api-key your-api-key-here
```

### Optional Configuration

You can customize ChatZiPT's behavior with these environment variables:

```bash
# AI Model Configuration
CHATZIPT_MODEL=gpt-3.5-turbo          # Default AI model
CHATZIPT_TEMPERATURE=0.7              # Response creativity (0.0-1.0)
CHATZIPT_MAX_TOKENS=1000              # Maximum response length

# Chat Configuration
CHATZIPT_MAX_HISTORY=10               # Number of messages to remember
CHATZIPT_CONVERSATIONS_DIR=conversations  # Directory for saved conversations
```

## Usage

### Command Line Interface

Start the interactive chat:

```bash
chatzipt
```

### Available Commands

While chatting, you can use these commands:

- `/help` - Show available commands
- `/clear` - Clear conversation history
- `/save <filename>` - Save conversation to file
- `/load <filename>` - Load conversation from file
- `/model <model_name>` - Change AI model (e.g., gpt-4, gpt-3.5-turbo)
- `/stats` - Show session statistics
- `/quit` or `/exit` - Exit the application

### Example Session

```
You: Hello! How are you?
ChatZiPT: Hello! I'm doing well, thank you for asking. I'm ChatZiPT, your AI assistant. How can I help you today?

You: /stats
Session Statistics:
- Total messages: 2
- Your messages: 1
- Assistant messages: 1
- Current model: gpt-3.5-turbo
- API configured: Yes

You: /save my-conversation
💾 Conversation saved to my-conversation.json

You: /quit
👋 Goodbye! Thanks for using ChatZiPT!
```

### Python API

You can also use ChatZiPT programmatically:

```python
from chatzipt import ChatZiPT

# Initialize the chat
chat = ChatZiPT()

# Send a message
response = chat.chat("Hello, how are you?")
print(response)

# Get conversation history
history = chat.get_conversation_history()

# Save conversation
chat.save_conversation("my_chat.json")

# Clear conversation
chat.clear_conversation()
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black chatzipt/
isort chatzipt/
```

### Linting

```bash
flake8 chatzipt/
```

## Requirements

- Python 3.8+
- OpenAI API key (for AI features)
- Internet connection (for API calls)

## Dependencies

- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management
- `colorama` - Cross-platform colored terminal output
- `rich` - Rich text and beautiful formatting

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.