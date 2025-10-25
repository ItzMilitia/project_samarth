Project Samarth — Quick Run
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. python ingestion/ingest_sample_and_live.py
4. uvicorn api.main:app --reload --port 8000
5. open frontend/index.html in a browser and ask a sample question
