# ECE 157C/272C: Homework 1

**Name:** Jeitī Trujillo
**Institution:** University of California, Santa Barbara (UCSB)  
**Department:** Electrical & Computer Engineering / Master of Technology Management

---

## 🚀 Overview

This project implements an **Autonomous CSV Question-Answering AI Agent** tailored for engineering workflows. Built using **LangGraph** and **Claude 3.5 Sonnet**, the agent functions as an **Intelligent Engineering Assistant (IEA)**.

It translates natural language queries into executable Python code, verifies the output, & provides data-driven insights through a stateful **Perceive-Think-Act-Learn** loop.

---

## 🏗️ Architecture: The Agentic Loop

The agent is modeled after the operational flowchart of a goal-based reasoning agent:

### **Perceive (World View)**

The agent utilizes a **RAG-lite metadata strategy**. Instead of loading the entire dataset into the prompt, it retrieves a **Snapshot** (schema and sample rows) to build its world view without context overload, avoiding **Digital HSAM**.

### **Think & Plan (Codegen)**

The agent utilizes the **LATM (LLMs As Tool Makers)** paradigm. It generates custom Python/Pandas scripts dynamically to solve novel data problems.

### **Act (Execution)**

The tactical step is performed in a sandboxed environment using:

```python
exec(code, env)
```

<pre>
📁 Project Structure
project/
├── agent.py           # LangGraph state machine & workflow orchestration
├── nodes.py           # Implementation of Perceive, Think, and Act logic
├── test_agent.py      # Mandatory entry point & batch execution script
├── housing.csv        # California Housing Prices dataset
├── custom_dataset.csv # Custom Semiconductor Wafer Yield dataset
├── results.csv        # Automated log of 18 test cases (Fixed & Custom)
└── Report.pdf         # Detailed failure analysis & advanced reflections
</pre>

📊 Datasets

1. California Housing (Fixed)

Analysis of geographic and economic trends, including spatial price variation and income correlations.

2. Semiconductor Wafer Yield (Custom)

A custom manufacturing log simulating IEA data:Metrics: wafer_id, batch_id, critical_dimension_nm, defect_density, yield_score, process_temp.

🛠️ Setup & Usage

Installationpip install langgraph anthropic pandas python-dotenv

ConfigurationEnsure your API credentials are set in the environment or a .env file:export ANTHROPIC_API_KEY='your_key_here'

ExecutionRun the batch processing script to generate the final results:python3 test_agent.py

🧠 Core Engineering Principles

Contextual Guardrails: The agent is restricted to Pandas operations to ensure stability.

Reflection & Debugging: Documented failure cases led to the implementation of robust code-stripping logic to handle unwanted Markdown formatting.

Scalability: The LangGraph architecture is extensible for future assignments involving more complex domain knowledge.

"There Is A Difference Between Knowing The Path And Walking The Path." — Morpheus

