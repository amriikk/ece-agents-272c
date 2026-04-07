from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    question: str
    csv_path: str
    generated_code: str
    execution_result: object
    evaluation: str
    retry_count: int
    final_answer: str

def should_retry(state):
    """Implements the 'Retry once' requirement."""
    if state['evaluation'] == "PASS" or state['retry_count'] >= 1:
        return "respond"
    return "codegen"

workflow = StateGraph(AgentState)

# Define the Nodes
workflow.add_node("codegen", codegen_node)
workflow.add_node("execute", execute_node)
# Evaluation logic can be inside execute or a separate node

# Define the Edges
workflow.set_entry_point("codegen")
workflow.add_edge("codegen", "execute")
workflow.add_conditional_edges(
    "execute",
    should_retry,
    {
        "codegen": "codegen",
        "respond": END
    }
)

app = workflow.compile()