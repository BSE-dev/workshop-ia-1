"""Basic conversational agent using LangGraph."""

from dotenv import load_dotenv
import os
import sys
from typing import Annotated

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

load_dotenv()


class State(TypedDict):
    """LangGraph State"""
    messages: Annotated[list, add_messages]


# Prompt
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", ("You are a helpful AI assistant providing support for a series of "
                "workshops for AI engineers in Brest.")),
    MessagesPlaceholder("messages")
])

# LLM model
# Select the appropriate chat model based on available API keys
chat_model: AzureChatOpenAI | ChatOpenAI | None = None
if os.getenv("AZURE_OPENAI_API_KEY"):
    chat_model = AzureChatOpenAI(
        model="gpt-4o-mini",
        api_version="2025-02-01-preview",
        temperature=0.7
    )
elif os.getenv("OPENAI_API_KEY"):
    chat_model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )
else:
    print("Error: No API keys found. Please set either OPENAI_API_KEY or "
          "AZURE_OPENAI_API_KEY in your environment variables.")
    sys.exit(1)

# Chain
chat_chain = chat_prompt | chat_model


# Chatbot node
def chatbot(state: State):
    return {"messages": [chat_chain.invoke({"messages": state["messages"]})]}


# Graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
