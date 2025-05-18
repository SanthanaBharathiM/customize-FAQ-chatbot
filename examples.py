"""
Example demonstrating different use cases for the simple chatbot
"""

import os
from simple_chatbot import create_chatbot, chat_with_bot, create_streaming_chatbot

# Set your OpenAI API key here or as an environment variable
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = input("Enter your OpenAI API key: ")

def basic_demo():
    """Basic demo showing a simple conversation."""
    print("\n=== Basic Demo ===")
    
    # Initialize the chatbot
    chatbot = create_chatbot()
    
    # Define conversation parameters
    thread_id = "basic-demo"
    personality = "friendly"
    language = "English"
    
    # First message
    response = chat_with_bot(
        chatbot,
        "Hi, my name is Alice.",
        thread_id,
        personality,
        language
    )
    print(f"User: Hi, my name is Alice.")
    print(f"Bot: {response.content}\n")
    
    # Second message - test if the bot remembers the name
    response = chat_with_bot(
        chatbot,
        "Do you remember my name?",
        thread_id,
        personality,
        language
    )
    print(f"User: Do you remember my name?")
    print(f"Bot: {response.content}\n")


def language_demo():
    """Demo showing language switching capabilities."""
    print("\n=== Language Demo ===")
    
    # Initialize the chatbot
    chatbot = create_chatbot()
    
    # Define conversation parameters
    thread_id = "language-demo"
    personality = "professional"
    
    # English response
    response = chat_with_bot(
        chatbot,
        "Tell me about artificial intelligence.",
        thread_id,
        personality,
        "English"
    )
    print(f"User: Tell me about artificial intelligence.")
    print(f"Bot (English): {response.content}\n")
    
    # Spanish response
    response = chat_with_bot(
        chatbot,
        "Tell me about artificial intelligence.",
        thread_id,
        personality,
        "Spanish"
    )
    print(f"User: Tell me about artificial intelligence.")
    print(f"Bot (Spanish): {response.content}\n")


def personality_demo():
    """Demo showing personality customization."""
    print("\n=== Personality Demo ===")
    
    # Initialize the chatbot
    chatbot = create_chatbot()
    
    # Define conversation parameters
    language = "English"
    
    # Formal personality
    response = chat_with_bot(
        chatbot,
        "Give me a weather forecast.",
        "formal-demo",
        "formal and professional",
        language
    )
    print(f"User: Give me a weather forecast.")
    print(f"Bot (Formal): {response.content}\n")
    
    # Humorous personality
    response = chat_with_bot(
        chatbot,
        "Give me a weather forecast.",
        "humorous-demo",
        "humorous and witty",
        language
    )
    print(f"User: Give me a weather forecast.")
    print(f"Bot (Humorous): {response.content}\n")


def streaming_demo():
    """Demo showing streaming capabilities."""
    print("\n=== Streaming Demo ===")
    print("(Token-by-token output)\n")
    
    # Initialize the chatbot
    chatbot = create_chatbot()
    
    # Define conversation parameters
    thread_id = "streaming-demo"
    personality = "concise"
    language = "English"
    
    # Streaming response
    print(f"User: Write a short poem about technology.")
    print(f"Bot: ", end="")
    
    for token in create_streaming_chatbot(
        chatbot,
        "Write a short poem about technology.",
        thread_id,
        personality,
        language
    ):
        print(token, end="", flush=True)
    
    print("\n")


if __name__ == "__main__":
    print("Running chatbot demos...")
    
    basic_demo()
    language_demo()
    personality_demo()
    streaming_demo()
    
    print("All demos completed!")
