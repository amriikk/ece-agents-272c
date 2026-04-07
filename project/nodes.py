import pandas as pd
from anthropic import Anthropic

# Component: Data Tool (Retrieval)
def get_csv_metadata(csv_path: str):
    """Provides the 'World View' of the data without context overload."""
    df = pd.read_csv(csv_path, nrows=5)
    summary = f"Columns: {list(df.columns)}\nSample Data:\n{df.to_string()}"
    return summary

# Node: Codegen (Think & Plan)
def codegen_node(state):
    """LLM acts as a 'Planner Robot' to generate strategic Python code."""
    client = Anthropic()
    metadata = get_csv_metadata(state['csv_path'])
    
    prompt = f"""
    You are a Senior AI Systems Architect. Write Python code using pandas to answer: {state['question']}
    Data Metadata:
    {metadata}
    
    Rules:
    - Read CSV from: {state['csv_path']}
    - Store the final answer in a variable named 'result'.
    - Do not use any external libraries other than pandas.
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    # Basic parsing logic here to extract code from markdown
    state['generated_code'] = response.content[0].text
    return state

# Node: Execute (Tactical Step)
def execute_node(state):
    try:
        env = {}
        exec(state['generated_code'], env)
        state['execution_result'] = env.get('result', "No 'result' variable found.")
        state['evaluation'] = "PASS"
    except Exception as e:
        state['execution_result'] = str(e)
        state['evaluation'] = "FAIL"
    return state