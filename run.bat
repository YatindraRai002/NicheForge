@echo off
if "%1"=="setup" (
    pip install -r requirements.txt
    goto :eof
)
if "%1"=="data" (
    python dataset_generation/scraper.py
    python dataset_generation/generator.py
    goto :eof
)
if "%1"=="eval" (
    python evaluation/evaluate.py
    python evaluation/judge.py
    goto :eof
)
if "%1"=="demo" (
    python -m streamlit run app.py
    goto :eof
)

echo Usage: run.bat [setup|data|eval|demo]
