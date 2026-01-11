import os
import shutil
import logging
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our existing logic (now in basic relative imports since we are in backend dir)
from backend.inference import engine
# We need to make sure python path finds 'backend' or we handle imports carefully.
# Since we will run uvicorn from root as `uvicorn backend.main:app`, relative imports like `.inference` might be needed
# OR absolute imports `backend.inference`. Let's assume running from root.

# Actually, if we moved fields INTO backend, we might need to adjust imports inside inference.py too if it imports other things.
# inference.py imports dotenv and groq, which is fine.

app = FastAPI(title="NicheForge API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

# Request Models
class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str

# Endpoints

@app.get("/health")
def health_check():
    return {"status": "ok", "backend": engine.active_backend}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response_text = engine.generate(request.message, temperature=request.temperature)
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
def generate_data(files: List[UploadFile] = File(...)):
    # Save files
    upload_dir = os.path.join("backend", "raw_data_uploaded")
    os.makedirs(upload_dir, exist_ok=True)
    
    saved_files = []
    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_path)
    
    # Trigger generation
    # We import here to avoid circular deps or top level issues
    from backend.dataset_generation.generator import generate_dataset
    
    output_file = os.path.join("backend", "dataset_uploaded.json")
    
    try:
        # Synchrounous for now, but could be background task
        generate_dataset(upload_dir, output_file)
        
        # Read result preview
        import json
        with open(output_file, "r") as f:
            data = json.load(f)
            
        return {
            "status": "success", 
            "message": f"Generated {len(data)} pairs.",
            "preview": data[:5],
            "total": len(data)
        }
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
