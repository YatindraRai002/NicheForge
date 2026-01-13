# NicheForge

**Turn any documentation into a fine-tuned domain expert AI.**

## What It Does

NicheForge is an end-to-end pipeline that takes raw text/docs, generates synthetic training data, fine-tunes a Llama-3 model with LoRA adapters, and serves it via a chat interface. Upload docs → get a specialized AI assistant.

## Key Features

- **Synthetic Data Generation** — Upload `.txt` files, auto-generate instruction/response pairs via LLM
- **LoRA Fine-Tuning** — Train Llama-3 using Unsloth (2x faster, 60% less VRAM)
- **Multi-Backend Inference** — Automatic fallback: Local Adapter → Groq → Ollama → Mock
- **Background Training Jobs** — Trigger fine-tuning via API without blocking
- **Built-in Evaluation** — Run benchmarks against a test set
- **Modern Chat UI** — Next.js frontend with real-time responses

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, TailwindCSS, Framer Motion |
| Backend | FastAPI, Uvicorn, Python 3.10+ |
| LLM Inference | Groq API, Ollama (local) |
| Fine-Tuning | Unsloth, LoRA, TRL, HuggingFace Datasets |
| Data Pipeline | Custom scraper + LLM-based data generator |

## Architecture

```
Raw Docs (.txt) → Data Generator (Groq/Ollama) → Synthetic Dataset (.json)
                                                        ↓
Chat UI (Next.js) ← FastAPI Backend ← Fine-Tuned Model (Unsloth + LoRA)
                                                        ↓
                                              Evaluation Pipeline
```

## Setup (Local)

**Prerequisites:** Python 3.10+, Node.js 18+, Groq API key (or Ollama installed)

```bash
# Clone
git clone https://github.com/YatindraRai002/NicheForge.git
cd NicheForge

# Backend
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install && cd ..

# Run
# Terminal 1: Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

- Frontend: http://localhost:3000
- Backend Docs: http://localhost:8000/docs

## Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=gsk_your_api_key_here
MODEL_NAME=llama-3.1-8b-instant
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send message, get AI response |
| `POST` | `/generate` | Upload .txt files → generate training dataset |
| `POST` | `/train` | Trigger LoRA fine-tuning (background job) |
| `POST` | `/evaluate` | Run evaluation on test set |
| `GET` | `/health` | Check backend status + active LLM backend |

## Deployment

**Render (Backend)**
```bash
# Set build command
pip install -r backend/requirements.txt

# Set start command
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Docker**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend/ ./backend/
RUN pip install -r backend/requirements.txt
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Future Improvements

- [ ] Add streaming responses for chat endpoint
- [ ] Support PDF/Markdown file uploads for data generation
- [ ] Implement model versioning and A/B testing

## License

MIT
