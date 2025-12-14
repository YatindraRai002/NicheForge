import os
import json
import glob
import time

import ollama

def query_llm(text_chunk):
    system_prompt = """You are an expert at creating training datasets for fine-tuning LLMs. 
    Your task is to analyze the provided text and generate comprehensive Q&A pairs.
    Output MUST be a raw JSON list of objects associated with the text.
    Each object must have "instruction" and "output" keys.
    Do not add markdown formatting or explanations outside the JSON."""
    
    user_prompt = f"""Analyze the following text from documentation and create 3-5 high-quality instruction/response pairs.
    Focus on "How to", "Explain", and code usage examples.
    
    TEXT:
    {text_chunk}
    
    RESPONSE JSON:"""
    
    try:
        # Use format='json' to force structured output
        response = ollama.chat(model='mistral', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ], format='json')
        
        content = response['message']['content']
        # Mistral sometimes returns a single object instead of a list, or wrapped in weird ways.
        # We try to parse it.
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Fallback regex
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
            else:
                return []

        if isinstance(data, dict):
            # If it returns a single object with "instruction" key, wrap it in list
            if "instruction" in data:
                return [data]
            # Sometimes it puts the list under a key like "pairs" or "qna"
            for key in data:
                if isinstance(data[key], list):
                    return data[key]
            return []
            
        return data if isinstance(data, list) else []

    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return []

def generate_dataset(input_dir, output_file):
    files = glob.glob(os.path.join(input_dir, "*.txt"))
    all_data = []
    
    # Check if file exists to resume? (Simplification: just Append mode if possible, or read-modify-write)
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        except:
            all_data = []

    print(f"Found {len(files)} files to process. Proceeding incrementally...")
    
    for file_idx, filepath in enumerate(files):
        print(f"[{file_idx+1}/{len(files)}] Processing {filepath}...")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue
            
        # Increase chunk size slightly to reduce number of calls? No, 2000 is okay.
        chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
        
        file_pairs = []
        for i, chunk in enumerate(chunks):
            if len(chunk) < 100: continue
            
            print(f"  - Chunk {i+1}/{len(chunks)}", end="\r") 
            pairs = query_llm(chunk)
            
            for pair in pairs:
                if "instruction" in pair and "output" in pair:
                    entry = {
                        "instruction": pair["instruction"],
                        "input": "", # Input is often empty for QA, or could be the chunk context
                        "output": pair["output"]
                    }
                    file_pairs.append(entry)
        
        print(f"  - Generated {len(file_pairs)} pairs.")
        all_data.extend(file_pairs)
        
        # Save after every file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2)
            
    print(f"Done! Saved {len(all_data)} examples to {output_file}")

if __name__ == "__main__":
    generate_dataset("raw_data", "dataset.json")
