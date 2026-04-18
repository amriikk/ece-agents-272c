import os
import csv
from agent import app

# 1. REQUIRED FUNCTION
def run_agent(question: str, csv_path: str) -> dict:
    """
    Executes the LangGraph Perceive-Think-Act loop.
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
    
    # Trigger the Agentic Loop
    final_state = app.invoke(initial_state)
    
    # Return exactly what the TA requested
    return {
        "generated_code": final_state["generated_code"],
        "execution_result": final_state["execution_result"],
        "evaluation": final_state["evaluation"],
        "final_answer": final_state["final_answer"]
    }

# 2. BATCH QUESTIONS
FIXED_QUESTIONS = [
    "What is the average median house value across the dataset?",
    "Which ocean proximity category has the highest average median house value?",
    "What are the minimum, maximum, and median values of median house value?",
    "How does median income vary across different ocean proximity categories?",
    "Which geographic areas (based on latitude and longitude ranges) have the highest average house prices?",
    "How does population density (defined as population per household) relate to median house value?",
    "Identify the top 5 most expensive geographic areas and explain the key factors contributing to their high prices.",
    "Find coastal areas where house prices are relatively low despite proximity to the ocean. What factors might explain this?",
    "Identify areas with similar median income levels but significantly different median house value. What factors might explain these differences?"
]

CUSTOM_QUESTIONS = [
    "What is the average yield_score across all batches?",
    "How many wafers have a defect_density greater than 4.0?",
    "What is the maximum and minimum process_temp recorded?",
    "Which batch_id has the highest average critical_dimension_nm?",
    "Is there a correlation between process_temp and yield_score?",
    "What is the standard deviation of defect_density for wafers in Batch B-01?",
    "Identify the top 5 wafers with the lowest yield_score and determine if they share a common batch_id or high process_temp.",
    "Segment the wafers into 'High Yield' (>90) and 'Low Yield' (<80). What is the average defect_density for each segment?",
    "Find wafers where critical_dimension_nm is an outlier (more than 2 standard deviations from the mean) and describe their yield_score."
]

# 3. RUNNER & RESULTS CSV GENERATOR
def main():
    results = []
    
    # Process Housing Data
    print("--- Processing housing.csv ---")
    for q in FIXED_QUESTIONS:
        res = run_agent(q, "housing.csv")
        results.append(["housing.csv", q, res["generated_code"], res["final_answer"]])
    
    # Process Custom Semiconductor Data
    print("--- Processing custom_dataset.csv ---")
    for q in CUSTOM_QUESTIONS:
        res = run_agent(q, "custom_dataset.csv")
        results.append(["custom_dataset.csv", q, res["generated_code"], res["final_answer"]])

    # Save to CSV in required format
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["dataset_name", "question", "generated_code", "final_answer"])
        writer.writerows(results)
    
    print("Successfully generated results.csv")

if __name__ == "__main__":
    main()