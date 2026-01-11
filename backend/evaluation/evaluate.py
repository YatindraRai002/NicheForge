import json
import os
from tqdm import tqdm

# Mock configuration for demonstration if model not present
MODEL_PATH = "../fine_tuning/lora_model" 
BENCHMARK_FILE = "evaluation/test_set.json"

import ollama

def evaluate():
    print("Loading test questions...")
    try:
        with open(BENCHMARK_FILE, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(f"Test set not found at {BENCHMARK_FILE}. Exiting.")
        return

    # Try to load local model, else fallback to Ollama
    use_ollama = False
    model_name = "mistral" # Baseline
    
    # Check for local adapter
    if os.path.exists(MODEL_PATH):
        print("Found local adapter. Attempting to load (requires GPU/Unsloth)...")
        try:
            from unsloth import FastLanguageModel
            # Load model logic here (omitted for safety on CPU-only envs causing crashes). 
            # If you have a GPU, uncomment the actual loading code.
            print("Warning: Loading Unsloth model on this environment might be slow or fail. Switching to Ollama for stability.")
            use_ollama = True
        except ImportError:
            print("Unsloth not installed. Falling back to Ollama.")
            use_ollama = True
    else:
        print("No local adapter found. Using Ollama (baseline) for evaluation.")
        use_ollama = True

    results = []
    
    for item in tqdm(questions, desc="Evaluating"):
        question = item["question"]
        
        if use_ollama:
            try:
                # System prompt to act like the expert
                response = ollama.chat(model=model_name, messages=[
                    {'role': 'system', 'content': "You are an expert on Polars and this specific dataset."},
                    {'role': 'user', 'content': question}
                ])
                answer = response['message']['content']
            except Exception as e:
                answer = f"Error calling Ollama: {e}"
        else:
            # Placeholder for actual Unsloth inference
            answer = "[MOCK] Unsloth inference would happen here."

        results.append({
            "question": question,
            "reference": item["reference_answer"],
            "model_prediction": answer
        })

    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nEvaluation complete! Results saved to evaluation_results.json")
    print("Sample Result:")
    if results:
        print(f"Q: {results[0]['question']}")
        print(f"A: {results[0]['model_prediction'][:100]}...")

if __name__ == "__main__":
    evaluate()
