Project Samarth — Intelligent Q&A on Indian Agriculture & Climate Data

Overview

Project Samarth is an end-to-end prototype of an intelligent question-answering system over India's open government datasets. Using data from data.gov.in
, this system allows users to query agricultural production and climate patterns across Indian states and districts, providing data-backed insights in real time.

The project demonstrates:

Cross-domain data integration (agriculture + climate)

Natural language querying via a simple Q&A interface

Traceable, JSON-safe responses citing the original data sources

This project is ideal for policymakers, researchers, or data enthusiasts who want insights from Indian government data without manually processing raw datasets.

Features

Compare average annual rainfall between any two Indian states

Identify districts with the highest/lowest crop production for specific crops

Trend analysis of crop production over multiple years

JSON responses with data source citations

Frontend interface for interactive querying

Demo

You can run a live prototype locally using your browser.

Sample Questions:

"Compare the average annual rainfall in Karnataka and Maharashtra for the last 2 available years."

"Identify the district in Karnataka with the highest production of Rice in the most recent year available."

Project Structure
project_samarth/
│
├─ api/                  # FastAPI backend
│   └─ main.py
│
├─ frontend/             # HTML frontend for asking questions
│   └─ index.html
│
├─ ingestion/            # Scripts to download, clean, and canonicalize datasets
│   └─ ingest_sample_and_live.py
│
├─ data/                 # Canonical parquet datasets (generated after ingestion)
│   ├─ agri_canonical.parquet
│   └─ climate_canonical.parquet
│
├─ requirements.txt      # Python dependencies
└─ README.md

Setup & Usage
1. Clone the repository
git clone https://github.com/ItzMilitia/project_samarth.git
cd project_samarth

2. Create a virtual environment
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Ingest datasets
python -m ingestion.ingest_sample_and_live


This generates canonical parquet files in the data/ folder.

5. Run backend server
uvicorn api.main:app --reload --port 8000

6. Open frontend

Navigate to frontend/index.html in your browser OR run a simple HTTP server:

cd frontend
python -m http.server 5500


Open http://127.0.0.1:5500 in your browser

7. Ask a question

Type your question in the text area and click Ask Question. The answer will appear below.

Technology Stack

Python 3.12

FastAPI — backend API

Pandas & NumPy — data processing

Frontend — HTML, CSS, JavaScript

Open Government Data — data.gov.in

Key Design Principles

Accuracy & Traceability: All responses include citations for the data sources.

JSON-safe responses: Ensures frontend receives consistent, serializable data.

CORS-enabled: Frontend works from any origin for local testing or live demos.

Extensible: Easy to add new datasets or question types in future.
