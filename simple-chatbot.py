"""
Simple Chatbot Implementation using LangChain and LangGraph

This module implements a basic chatbot that can maintain conversation context
across multiple interactions, using LangGraph for memory management.
"""

import os
from typing import Sequence, Optional
from typing_extensions import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


# Define the state schema that will track messages and personality
class ChatbotState(TypedDict):
    """State schema for the chatbot."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    personality: str
    language: str


def create_chatbot(model_name: str = "gpt-3.5-turbo", max_tokens: int = 150):
    """
    Creates a chatbot application with memory persistence.
    
    Args:
        model_name: The name of the LLM model to use
        max_tokens: Maximum number of tokens to consider in message history
        
    Returns:
        A compiled LangGraph application
    """
    # Initialize the LLM
    model = ChatOpenAI(model_name=model_name)
    
    # Create a prompt template that customizes responses based on personality and language
    prompt_template = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant with a {personality} personality. "
            "Answer all questions to the best of your ability in {language}."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    # Create a message trimmer to prevent context overflow
    def trim_messages(messages, max_tokens=max_tokens):
        """Limit message history to prevent token overflow."""
        from langchain_core.messages import trim_messages
        
        return trim_messages(
            messages=messages,
            max_tokens=max_tokens,
            strategy="last",  # Keep the most recent messages
            token_counter=model,
            include_system=True,  # Always keep system message
            allow_partial=False,
            start_on="human",  # Always start with a human message
        )
    
    # Define the workflow graph
    workflow = StateGraph(state_schema=ChatbotState)
    
    # Define the function that processes input and generates responses
    def call_model(state: ChatbotState):
        # Trim message history to avoid token limits
        trimmed_messages = trim_messages(state["messages"])
        
        # Create prompt with the current state
        prompt = prompt_template.invoke({
            "messages": trimmed_messages,
            "personality": state["personality"],
            "language": state["language"]
        })
        
        # Get response from LLM
        response = model.invoke(prompt)
        
        # Return only the response message to be added to the state
        return {"messages": [response]}
    
    # Define the graph structure
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)
    
    # Setup persistence layer
    memory = MemorySaver()
    
    # Compile the graph into an application
    app = workflow.compile(checkpointer=memory)
    
    return app


def chat_with_bot(
    app, 
    message: str, 
    thread_id: str = "default", 
    personality: str = "friendly", 
    language: str = "English"
):
    """
    Send a message to the chatbot and get a response.
    
    Args:
        app: The compiled chatbot application
        message: User message text
        thread_id: Unique identifier for this conversation
        personality: Personality trait for the bot
        language: Language for the response
        
    Returns:
        The chatbot's response message
    """
    # Prepare config for the specific conversation thread
    config = {"configurable": {"thread_id": thread_id}}
    
    # Create the input message
    input_message = HumanMessage(content=message)
    
    # Invoke the application with the message and config
    output = app.invoke(
        {
            "messages": [input_message],
            "personality": personality,
            "language": language
        },
        config
    )
    
    # Return the latest AI message
    return output["messages"][-1]


def create_streaming_chatbot(
    app, 
    message: str, 
    thread_id: str = "default", 
    personality: str = "friendly", 
    language: str = "English"
):
    """
    Stream responses from the chatbot token by token.
    
    Args:
        app: The compiled chatbot application
        message: User message text
        thread_id: Unique identifier for this conversation
        personality: Personality trait for the bot
        language: Language for the response
    
    Yields:
        Tokens from the AI response as they are generated
    """
    # Prepare config for the specific conversation thread
    config = {"configurable": {"thread_id": thread_id}}
    
    # Create the input message
    input_message = HumanMessage(content=message)
    
    # Stream responses from the application
    for chunk, metadata in app.stream(
        {
            "messages": [input_message],
            "personality": personality,
            "language": language
        },
        config,
        stream_mode="messages"
    ):
        if isinstance(chunk, AIMessage):
            yield chunk.content


if __name__ == "__main__":
    # Simple demonstration of the chatbot
    import os
    
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = input("Enter your OpenAI API key: ")
    
    # Create the chatbot
    print("Initializing chatbot...")
    chatbot = create_chatbot()
    
    print("\nChatbot is ready! Type 'exit' to end the conversation.\n")
    
    thread_id = "demo-conversation"
    personality = "friendly and helpful"
    language = "English"
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break
        
        # Get chatbot response with streaming
        print("\nBot: ", end="")
        
        # Demo the streaming interface
        for token in create_streaming_chatbot(
            chatbot, 
            user_input, 
            thread_id, 
            personality, 
            language
        ):
            print(token, end="", flush=True)
        
        print("\n")
