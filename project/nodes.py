import os
import pandas as pd
from anthropic import Anthropic

# Component: Perception (World View)
def get_metadata(csv_path: str):
    """Provides a snapshot of the data so the LLM knows the 'Matrix' it is working in."""
    df = pd.read_csv(csv_path, nrows=5)
    return f"Columns: {list(df.columns)}\nSample Data:\n{df.to_string()}"

# Node 1: Codegen (The 'Brain')
def codegen_node(state):
    print("--- NODE: CODEGEN ---")
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    metadata = get_metadata(state['csv_path'])
    
    prompt = f"""
    Write Python code using pandas to answer this question: {state['question']}
    CSV File Path: {state['csv_path']}
    
    Data Metadata:
    {metadata}
    
    Rules:
    - You MUST store the final result in a variable named 'result'.
    - Output ONLY raw Python code. Do not include markdown backticks or explanations.
    """
    
    response = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Simple parsing to ensure we only get the code
    code = response.content[0].text.strip()
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
        
    state['generated_code'] = code
    return state

# Node 2: Execute (The 'Body')
def execute_node(state):
    print("--- NODE: EXECUTE ---")
    try:
        # The requirement: Execute using exec(code, env)
        exec_env = {}
        exec(state['generated_code'], exec_env)
        
        # Pull the 'result' variable out of the local environment
        state['execution_result'] = exec_env.get('result', "Error: 'result' variable not found in code.")
        state['evaluation'] = "PASS"
    except Exception as e:
        print(f"Execution Error: {e}")
        state['execution_result'] = str(e)
        state['evaluation'] = "FAIL"
        state['retry_count'] += 1
    
    return state

# Node 3: Respond (The 'Voice')
def respond_node(state):
    print("--- NODE: RESPOND ---")
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"""
    Based on this data result: {state['execution_result']}
    Provide a clear, natural language answer to the user's question: {state['question']}
    """
    
    response = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    state['final_answer'] = response.content[0].text
    return state