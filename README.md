# NicheForge ⚒️

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.30+-ff4b4b)
![Status](https://img.shields.io/badge/status-production--ready-success)

**NicheExpert** is an end-to-end MLOps pipeline for creating specialized Domain Expert LLMs. It demonstrates a complete lifecycle: from scraping documentation and generating synthetic training data (via prompt engineering), to fine-tuning a Llama-3 model using LoRA adapters, and serving it via a modern, containerized chat interface.

> **Current Specialization**: [Polars](https://pola.rs/) DataFrame Library (Rust/Python).

---

## 🌟 Key Features

*   **⚡ Automated Data Pipeline**: Scrapes raw text and uses an LLM (Ollama/Mistral) to generate high-quality "Instruction-Input-Output" training pairs (`dataset.json`).
*   **🧠 Efficient Fine-Tuning**: Uses **Unsloth** for 2x faster training and 60% less memory usage. Train Llama-3 8B on a free Google Colab Tesla T4 GPU.
*   **🎨 Production UI**: A clean, dark-mode Streamlit chat interface with typing effects, glassmorphism design, and real-time backend status.
*   **🛡️ Robust Inference Engine**:
    *   **Auto-Detection**: Automatically finds and loads your fine-tuned adapter.
    *   **Graceful Fallback**: Falls back to a local baseline model (Ollama) or a Mock mode if high-performance hardware is unavailable.
*   **🐳 Dockerized**: Deployment-ready with `docker-compose`.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Raw Docs] -->|Scraper| B[Text Files]
    B -->|Generator (Ollama)| C[dataset.json]
    C -->|Fine-Tuning (Colab/Unsloth)| D[LoRA Adapter]
    D -->|Download| E[Local App]
    E -->|Inference Engine| F[Streamlit UI]
    G[Ollama Baseline] -.->|Fallback| E
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)
The easiest way to run the application is using Docker Compose.

```bash
# Start the application
docker-compose up --build
```
Access the dashboard at **http://localhost:8501**.

### Option 2: Local Installation

**Prerequisites:**
*   Python 3.10+
*   [Ollama](https://ollama.com/) (installed and running `ollama serve`)

```bash
# 1. Clone & Install Dependencies
git clone https://github.com/your-repo/niche-expert.git
cd niche-expert
pip install -r requirements.txt

# 2. Run the App
python -m streamlit run app.py
```

---

## 🛠️ Workflow Guide

### 1. Data Generation 🧬
Create your own dataset from any text files placed in `raw_data/`.

```bash
python dataset_generation/generator.py
```
*   **How it works**: It iterates through files, chunks them, and prompts a local LLM (via Ollama) to valid QA pairs.
*   **Output**: A `dataset.json` file ready for training.

### 2. Fine-Tuning (Training) 🏋️
We use Google Colab for free GPU access.

1.  Open the provided notebook: `fine_tuning/FineTuning_Colab.ipynb` in [Google Colab](https://colab.research.google.com/).
2.  **Upload** your generated `dataset.json`.
3.  **Run All Cells**.
4.  The notebook will train the model and automatically download `lora_model.zip`.
5.  **Unzip** `lora_model.zip` into the root of this project directory.

### 3. Running Inference 🧠
Launch the app. The `InferenceEngine` will automatically switch modes:

| Mode | Condition | Indicator |
|------|-----------|-----------|
| **Local Adapter** | `lora_model/` folder exists | 🟢 Green Dot |
| **Ollama (Base)** | No adapter, but Ollama is running | 🔵 Blue Dot |
| **Mock** | No model, no Ollama | 🟠 Orange Dot |

---

## 📂 Project Structure

```text
niche-expert/
├── app.py                  # Streamlit Application (Frontend)
├── inference.py            # Backend Logic & Model Loading
├── Dockerfile              # Container definition
├── docker-compose.yml      # Orchestration
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── dataset.json            # Synthetic Training Data
├── lora_model/             # (Optional) Fine-tuned adapter
├── raw_data/               # Source txt files
├── dataset_generation/
│   └── generator.py        # Data pipeline script
├── fine_tuning/
│   ├── FineTuning_Colab.ipynb  # Training Notebook
│   └── train.py                # Local training script
└── evaluation/
    ├── evaluate.py         # Benchmark script
    ├── judge.py            # LLM-as-a-judge scorer
    └── test_set.json       # Ground truth QA
```

## 🤝 Contributing
Contributions are welcome! Please stick to the `Black` code style and ensure you update `requirements.txt` if adding libraries.

## 📄 License
MIT License. Free to use and modify.
