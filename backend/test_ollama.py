import ollama
try:
    print("Sending request...")
    resp = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': 'hi'}])
    print("Response:", resp['message']['content'])
except Exception as e:
    print("Error:", e)
