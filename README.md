# Simple customize-FAQ-chatbot

A straightforward chatbot implementation built with LangChain and LangGraph that maintains conversation history. This project demonstrates how to build a simple yet effective conversational AI that remembers context across multiple interactions.

## Features

- 🧠 **Conversation Memory**: Maintains context across multiple messages
- 🔄 **Streaming Responses**: Get tokens as they're generated for a more natural experience
- 🌐 **Language Support**: Answer in different languages
- 👤 **Customizable Personality**: Adjust the bot's personality traits
- 🧩 **Token Management**: Automatically manages conversation history to avoid token limits

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/SanthanaBharathiM/customize-FAQ-chatbot
.git
   cd langchain-simple-chatbot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Quick Start

Run the basic example:

```python
python simple_chatbot.py
```

This will start an interactive chat session in your terminal.

## Custom Usage

You can integrate the chatbot into your own applications:

```python
from simple_chatbot import create_chatbot, chat_with_bot

# Initialize the chatbot
chatbot = create_chatbot(model_name="gpt-3.5-turbo")

# Chat in a specific conversation thread
response = chat_with_bot(
    app=chatbot,
    message="Tell me a joke about programming",
    thread_id="user123",  # Unique ID for this conversation
    personality="humorous",
    language="English"
)

print(response.content)
```

### Streaming Example

For a more natural conversation experience, use streaming:

```python
from simple_chatbot import create_chatbot, create_streaming_chatbot

chatbot = create_chatbot()

# Stream the response token by token
for token in create_streaming_chatbot(
    app=chatbot,
    message="Explain quantum computing simply",
    thread_id="user123",
    personality="educational",
    language="English"
):
    print(token, end="", flush=True)
```

## How It Works

1. **State Management**: Uses LangGraph to maintain conversation state
2. **Memory Persistence**: Stores conversation history in memory (can be extended to databases)
3. **Token Management**: Automatically trims conversation history to prevent exceeding token limits
4. **Prompt Engineering**: Customizes system prompts based on personality and language

## Extending the Chatbot

You can enhance this chatbot in several ways:

- Connect to a database for persistent storage
- Add Retrieval-Augmented Generation (RAG) for accessing external knowledge
- Implement agent capabilities for taking actions
- Add tools or function-calling abilities

## Requirements

- Python 3.8+
- LangChain & LangGraph
- OpenAI API key (or another compatible LLM provider)

## License

MIT
