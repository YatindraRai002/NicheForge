<div align="center">

# ⚒️ NicheForge

### *Forge Your Own Domain Expert AI in Minutes*

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)](https://fastapi.tiangolo.com/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/Groq-Powered-f55036)](https://groq.com/)

**Transform any documentation into a specialized AI assistant with automated data generation, efficient fine-tuning, and production-ready deployment.**

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [API](#-api-documentation)

</div>

---

## 🎯 What is NicheForge?

NicheForge is a complete **end-to-end MLOps pipeline** that democratizes the creation of domain-specific AI experts. It combines a modern **Next.js** frontend with a robust **FastAPI** backend to handle the entire lifecycle:

```
📄 Raw Docs → 🤖 Synthetic Data → 🧠 Fine-Tuned Model → 💬 Production Chat UI
```

---

## ✨ Features

### 🎨 **Premium UI/UX**
- **Next.js Powered**: Fast, responsive, and SEO-friendly frontend.
- **Glassmorphism Design**: Modern dark theme with animated backgrounds and fluid interactions.
- **Real-Time Chat**: Smooth streaming responses and "thinking" states.

### 🔄 **Intelligent Data Pipeline**
- **Synthetic Data Generation**: Upload text files and automatically generate instruction-response pairs using local or cloud LLMs.
- **Smart Chunking**: Optimally splits documents for context retention.

### 🧠 **Efficient Fine-Tuning**
- **Unsloth Integration**: Fine-tune Llama-3 models 2x faster with 60% less memory.
- **Background Jobs**: Trigger training via API without blocking the UI.
- **Adapter Management**: Auto-loading of fine-tuned LoRA adapters.

### 🛡️ **Robust Backend**
- **FastAPI**: specialized endpoints for Chat, Data Generation, Training, and Evaluation.
- **LLM Agnostic**: Supports **Groq** (Cloud) and **Ollama** (Local) with automatic fallback.
- **Graceful Error Handling**: Detailed feedback for debugging.

---

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Next.js 14, TailwindCSS, Framer Motion, Lucide Icons.
- **Backend**: FastAPI, Uvicorn, Python 3.10+.
- **AI/ML**: Unsloth (Fine-tuning), LangChain/Groq (Inference), Ollama (Data Gen).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com/) (Optional, for local inference)
- Groq API Key (Recommended for speed)

### Installation (Windows)

1.  **Clone the repository**
    ```bash
    git clone https://github.com/YatindraRai002/NicheForge.git
    cd NicheForge
    ```

2.  **Environment Setup**
    Create a `.env` file in the root:
    ```env
    GROQ_API_KEY=your_key_here
    MODEL_NAME=llama-3.1-8b-instant
    ```

3.  **Install Backend**
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Install Frontend**
    ```bash
    cd frontend
    npm install
    cd ..
    ```

5.  **Run Everything**
    Double-click `start_dev.bat` or run:
    ```bash
    start_dev.bat
    ```

    - **Frontend**: http://localhost:3000
    - **Backend API**: http://localhost:8000/docs

---

## 📖 API Documentation

The FastAPI backend exposes the following endpoints:

- `POST /chat`: Send a message to the AI.
- `POST /generate`: Upload files (`.txt`) to generate a dataset.
- `POST /train`: Trigger a background fine-tuning job.
- `POST /evaluate`: Run the evaluation suite.
- `GET /health`: Check system status.

---

## 📂 Project Structure

```
NicheForge/
├── 📂 backend/               # FastAPI Application
│   ├── 📂 dataset_generation/ # Data synth logic
│   ├── 📂 fine_tuning/        # Unsloth training scripts
│   ├── 📂 evaluation/         # Eval/Benchmarking
│   ├── main.py                # API Entry point
│   ├── inference.py           # LLM Engine
│   └── requirements.txt
│
├── 📂 frontend/              # Next.js Application
│   ├── 📂 app/                # Pages and Layouts
│   ├── 📂 components/         # UI Components (Chat, Hero, etc.)
│   └── public/
│
├── start_dev.bat             # Launcher script
└── README.md                 # This file
```

---

<div align="center">

**Built with ❤️ by the NicheForge Community**

</div>
