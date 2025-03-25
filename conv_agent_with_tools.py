"""Basic conversational agent using LangGraph with tool calling."""

from dotenv import load_dotenv
import os
import sys
from typing import Annotated

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
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

# LLM Model
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

# Tools
tavily_tool = TavilySearchResults(max_results=2)


@tool
def add(first_int: int, second_int: int) -> int:
    """Add two integers together."""
    return first_int + second_int


tools = [tavily_tool, add]
# Bind the tools to the chat model
model_with_tools = chat_model.bind_tools(tools)

# Chain
chat_chain = chat_prompt | model_with_tools


# Nodes
def chatbot(state: State):
    return {"messages": [chat_chain.invoke({"messages": state["messages"]})]}


tool_node = ToolNode(tools)


# Routing functions (Edges)
def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


# Graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
# The `route_tools` function returns "tools" if the chatbot asks to use a tool, and
# "END" if it is fine directly responding. This conditional routing defines the main
# agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's
    # outputs as a specific node
    {"tools": "tools", END: END},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()
