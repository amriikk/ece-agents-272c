import os
from agent import app

def run_agent(question: str, csv_path: str) -> dict:
    """
    Coordinates the Perceive-Think-Act loop via LangGraph.
    """
   
    initial_state = {
        "question": question,
        "csv_path": csv_path,
        "generated_code": "",
        "execution_result": None,
        "evaluation": "FAIL",
        "retry_count": 0,
        "final_answer": ""
    }

    # Execute workflow: Input -> Codegen -> Execute -> Evaluate -> (Retry) -> Respond 
    final_state = app.invoke(initial_state)

    # Return required output format 
    return {
        "generated_code": final_state["generated_code"],
        "execution_result": final_state["execution_result"],
        "evaluation": final_state["evaluation"],
        "final_answer": final_state["final_answer"]
    }

if __name__ == "__main__":
    # Example usage for testing
    result = run_agent("What is the average median house value?", "housing.csv")
    print(f"Final Answer: {result['final_answer']}")