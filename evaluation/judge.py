import json
import ollama
import os
import mlflow

EVAL_FILE = "evaluation_results.json"
JUDGE_MODEL = "mistral" # Use the one user has pulled

def judge_answers():
    if not os.path.exists(EVAL_FILE):
        print(f"File {EVAL_FILE} not found. Run evaluate.py first.")
        return

    with open(EVAL_FILE, "r") as f:
        results = json.load(f)

    print(f"Judging {len(results)} answers using {JUDGE_MODEL}...")
    
    scored_results = []
    
    for item in results:
        question = item["question"]
        reference = item["reference"]
        prediction = item.get("model_prediction", "")
        
        prompt = f"""You are an impartial judge evaluating the quality of an AI model's answer.
        
        Question: {question}
        
        Reference Answer (Correct): {reference}
        
        Model Prediction: {prediction}
        
        Task:
        Rate the Model Prediction on a scale of 1 to 5 based on accuracy and helpfulness compared to the Reference Answer.
        Provide a short explanation.
        
        Format your response as JSON:
        {{
            "score": <int>,
            "explanation": "<string>"
        }}
        """
        
        try:
            response = ollama.chat(model=JUDGE_MODEL, messages=[{'role': 'user', 'content': prompt}])
            content = response['message']['content']
            
            # Simple cleanup to find JSON
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = content[start:end]
                evaluation = json.loads(json_str)
                
                item["judge_score"] = evaluation.get("score")
                item["judge_explanation"] = evaluation.get("explanation")
            else:
                item["judge_score"] = 1
                item["judge_explanation"] = "Failed to parse judge output."
                
        except Exception as e:
            print(f"Error judging item: {e}")
            item["judge_score"] = 0
            
        scored_results.append(item)
        print(f"Reviewed Q: '{question[:30]}...' -> Score: {item['judge_score']}/5")

    # Calculate average
    scores = [r["judge_score"] for r in scored_results if r["judge_score"] is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"\nAverage Quality Score: {avg_score:.2f}/5")
    
    # Save detailed report
    with open("evaluation/judge_report.json", "w") as f:
        json.dump(scored_results, f, indent=2)
    print("Full report saved to evaluation/judge_report.json")

    # MLOps: Track with MLflow
    try:
        mlflow.set_experiment("niche_model_eval")
        with mlflow.start_run():
            mlflow.log_metric("avg_quality_score", avg_score)
            mlflow.log_param("judge_model", JUDGE_MODEL)
            mlflow.log_artifact("evaluation/judge_report.json")
        print("Logged metrics to MLflow.")
    except Exception as e:
        print(f"MLflow logging failed: {e}")

if __name__ == "__main__":
    judge_answers()
