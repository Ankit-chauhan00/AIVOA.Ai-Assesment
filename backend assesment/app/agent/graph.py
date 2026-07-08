"""
LangGraph assistant pannel that powers the "AI Assistant" chat pannel on the log Intraction Screen
"""

import asyncio
from typing import Annotated, TypedDict

from app.agent.llm import reasoning_llm
from app.agent.tools import ALL_TOOLS
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

SYSTEM_PROMPT = """
You are an AI Assistant embedded in a Pharma CRM used by Medical Representatives (MRs) to manage Healthcare Professional (HCP) interactions.

Your job is to understand the user's request, decide whether a tool is required, call the appropriate tool when needed, and then explain the result in a clear, professional, and concise manner.

Available tools:

1. log_interaction
   - Use when the user describes a NEW interaction with an HCP.
   - The input should be the user's complete raw description.
   - The tool extracts structured information, creates the HCP if necessary, and logs the interaction.

2. edit_interaction
   - Use when the user wants to modify an existing interaction.
   - Update only the fields explicitly requested by the user.
   - Never modify fields that the user did not ask to change.

3. search_hcp
   - Use when the user wants to search for an HCP by name, specialty, hospital, or city.
   - Return matching HCPs from the CRM.

4. suggest_followups
   - Use when the user asks for recommendations or follow-up actions for a previously logged interaction.
   - Requires the interaction ID.

5. schedule_followup
   - Use when the user wants to create a follow-up task.
   - Requires the interaction ID and the follow-up task description.

General Guidelines:
- Always determine whether a tool is needed before responding.
- If a tool is required, call exactly the appropriate tool.
- Never invent HCPs, interaction IDs, or database information.
- If required information (such as an interaction ID) is missing, ask the user for it instead of guessing.
- After every successful tool call, summarize the result in one or two professional sentences.
- If a tool returns an error, explain the error politely and suggest what information is needed to continue.
- Keep responses concise, professional, and suitable for a Pharma CRM application.
- Do not expose internal implementation details unless the user explicitly asks for them.
"""

models_with_tools = reasoning_llm.bind_tools(ALL_TOOLS)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def call_model(state: AgentState):
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = await models_with_tools.ainvoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState):
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return END


tool_node = ToolNode(ALL_TOOLS)

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_edge(START, "agent")
workflow.add_node("tools", tool_node)
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

hcp_agent = workflow.compile()


async def run_agent(
    user_message: str,
    history: list[tuple[str, str]] | None = None,
):
    """
        Runs a single conversation turn through the LangGraph agent.

    Args:
        user_message: The latest message from the user.
        history: Optional chat history as (role, content) tuples.

    Returns:
        A dictionary containing:
        - reply
        - tool_calls
        - tool_results
        - execution_trace
    """

    messages = []
    for role, content in history or []:
        messages.append(
            HumanMessage(content=content)
            if role == "user"
            else AIMessage(content=content)
        )
    messages.append(HumanMessage(content=user_message))

    result = await hcp_agent.ainvoke({"messages": messages})
    final_message = result["messages"][-1]
    reply = final_message.content

    if isinstance(reply, list):
        parts = []

        for block in reply:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            elif hasattr(block, "text"):
                parts.append(block.text)
            else:
                parts.append(str(block))

        reply = " ".join(parts)

    elif not isinstance(reply, str):
        reply = str(reply)
    

    tool_calls = []
    tool_results = []

    for message in result["messages"]:
        # AI requested a tool
        if getattr(message, "tool_calls", None):
            for tool in message.tool_calls:
                tool_calls.append(
                    {
                        "name": tool["name"],
                        "args": tool["args"],
                    }
                )

        # Tool execution result
        if getattr(message, "type", None) == "tool":
            tool_results.append(
                {
                    "tool_name": getattr(message, "name", ""),
                    "output": message.content,
                }
            )

        execution_trace = ["Received user message"]

    for tool in tool_calls:
        execution_trace.append(f"Selected tool: {tool['name']}")

    for tool in tool_results:
        execution_trace.append(f"Executed tool: {tool['tool_name']}")

    execution_trace.append("Generated final response")

    return {
        "reply": reply,
        "tool_calls": tool_calls,
        "tool_results": tool_results,
        "execution_trace": execution_trace,
    }


async def main():

    # ----------------------------------------------------
    # Test 1: Log Interaction
    # ----------------------------------------------------
    print("\n================ TEST 1 =================")
    print("Log Interaction\n")

    result = await run_agent(
        """
        Today I met Dr. Raj Sharma, Cardiologist at Apollo Hospital, Delhi.

        We discussed NeuroPlus for heart failure management.
        I shared the product brochure and sample packs.

        The doctor was interested in the clinical evidence and requested a follow-up meeting in two weeks.
        """
    )

    print(result)

    # ----------------------------------------------------
    # Test 2: Search HCP
    # ----------------------------------------------------
    print("\n================ TEST 2 =================")
    print("Search HCP\n")

    result = await run_agent("Search for Dr. Raj Sharma.")

    print(result)

    # ----------------------------------------------------
    # Test 3: Edit Interaction
    # ----------------------------------------------------
    print("\n================ TEST 3 =================")
    print("Edit Interaction\n")

    result = await run_agent(
        """
        Update interaction 1.

        Change the interaction type to Call.

        Update the notes to mention that
        Dr. Raj Sharma requested the latest
        clinical trial data.

        Update the products discussed to
        NeuroPlus, Clinical Study Brochure.
        """
    )

    print(result)

    # ----------------------------------------------------
    # Test 4: Suggest Followups
    # ----------------------------------------------------
    print("\n================ TEST 4 =================")
    print("Suggest Followups\n")

    result = await run_agent(
        """
        Suggest follow-up actions for interaction 1.
        """
    )

    print(result)

    # ----------------------------------------------------
    # Test 5: Schedule Followup
    # ----------------------------------------------------
    print("\n================ TEST 5 =================")
    print("Schedule Followup\n")

    result = await run_agent(
        """
        Schedule a follow-up task for interaction 1.

        Task:
        Send Dr. Raj Sharma the NeuroPlus
        Phase III clinical evidence.

        Schedule it after 14 days.
        """
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
