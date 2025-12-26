from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from typing import TypedDict

from prompts import (
    PLANNER_PROMPT,
    RESEARCH_PROMPT,
    WRITER_PROMPT,
    EDITOR_PROMPT,
    QUALITY_PROMPT
)

llm= ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key="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"
#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
   
)

class ArticleState(TypedDict):
    topic: str
    outline: str
    research: str
    draft: str
    edited: str
    final: str


def planner_agent(state: ArticleState):
    response = llm.invoke(
        PLANNER_PROMPT + f"\nTopic: {state['topic']}"
    )
    state["outline"] = response.content
    return state


def research_agent(state: ArticleState):
    response = llm.invoke(
        RESEARCH_PROMPT + f"\nOutline:\n{state['outline']}"
    )
    state["research"] = response.content
    return state


def writer_agent(state: ArticleState):
    response = llm.invoke(
        WRITER_PROMPT
        + f"\nOutline:\n{state['outline']}\n\nResearch:\n{state['research']}"
    )
    state["draft"] = response.content
    return state


def editor_agent(state: ArticleState):
    response = llm.invoke(
        EDITOR_PROMPT + f"\nArticle:\n{state['draft']}"
    )
    state["edited"] = response.content
    return state


def quality_agent(state: ArticleState):
    response = llm.invoke(
        QUALITY_PROMPT + f"\nArticle:\n{state['edited']}"
    )
    state["final"] = response.content
    return state


def build_graph():
    graph = StateGraph(ArticleState)

    graph.add_node("planner", planner_agent)
    graph.add_node("researcher", research_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("editor", editor_agent)
    graph.add_node("quality", quality_agent)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "editor")
    graph.add_edge("editor", "quality")

    graph.set_finish_point("quality")

    return graph.compile()

# article_graph=build_graph()
# graph = article_graph.get_graph()

# with open("agent_graph.mmd", "w") as f:
#     f.write(graph.draw_mermaid())