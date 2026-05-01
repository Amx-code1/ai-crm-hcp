import re
import os
import json
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from tools import *
from models import EditInteraction
from tools import get_last_interaction_id


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

def detect_intent(state):
    text = state["input"].lower()

    if "show" in text or "fetch" in text or "list" in text:
        state["intent"] = "fetch"

    elif "summarize" in text or "summary" in text:
        state["intent"] = "summarize"

    elif "edit" in text or "update" in text:
        state["intent"] = "edit"

    elif "not interested" in text or "suggest" in text:
        state["intent"] = "suggest"   

    else:
        state["intent"] = "log"

    print("INTENT:", state["intent"])

    return state

def extract_data(state):
    prompt = f"""
Extract structured data from the text.

Rules:
- Extract follow_up if mentioned (e.g. "next week", "tomorrow")
- DO NOT include follow-up text inside notes
- Notes should only contain interaction summary
- If a field is missing, omit it (do NOT guess)

Return JSON with:
hcp_name, notes, sentiment, follow_up

Text: {state['input']}

Return ONLY JSON.
"""

    res = llm.invoke(prompt)

    import json
    try:
        data = json.loads(res.content)
    except:
        data = {}

    notes = data.get("notes", state["input"])
    follow_up = data.get("follow_up")

    # remove "follow up..." from notes if follow_up exists
    if follow_up:
        notes = re.sub(r'follow up.*', '', notes, flags=re.IGNORECASE).strip()

    state["data"] = {
    "hcp_name": data.get("hcp_name", "Dr Sharma"),
    "notes": notes,
    "sentiment": data.get("sentiment", "positive"),
    "follow_up": follow_up
    }

    return state

def run_tool(state):
    intent = state["intent"]

    if intent == "log":
        result = log_interaction.invoke({
    "data": state["data"]
})

    elif intent == "edit":
        last_id = get_last_interaction_id()

        text = state["input"].lower()

        sentiment = "negative" if "negative" in text else "positive"

        result = edit_interaction.invoke({
        "data": {
            "id": last_id,
            "sentiment": sentiment
        }
    })
    elif intent == "fetch":
        result = fetch_interactions.invoke({})

    elif intent == "suggest":
        result = suggest_next_action.invoke(state["input"])

    elif intent == "summarize":
        data = fetch_interactions.invoke({})
        result = summarize_hcp.invoke({
    "data": data
})

    else:
        result = {"error": "invalid"}


    state["output"] = result
    return state

graph = StateGraph(dict)

graph.add_node("intent", detect_intent)
graph.add_node("extract", extract_data)
graph.add_node("tool", run_tool)

def route_after_intent(state):
    if state["intent"] == "edit":
        return "tool"
    return "extract"

graph.add_conditional_edges(
    "intent",
    route_after_intent,
    {
        "extract": "extract",
        "tool": "tool"
    }
)

graph.set_entry_point("intent")

graph.add_edge("extract", "tool")

graph_app = graph.compile()