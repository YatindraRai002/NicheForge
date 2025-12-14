setup:
	pip install -r requirements.txt

data:
	python dataset_generation/scraper.py
	python dataset_generation/generator.py

eval:
	python evaluation/evaluate.py
	python evaluation/judge.py

demo:
	python -m streamlit run app.py
