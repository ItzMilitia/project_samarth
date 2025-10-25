from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import numpy as np
import re

# -------------------------------
# App and CORS setup
# -------------------------------
app = FastAPI(title="Project Samarth Q&A API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend from any origin
    allow_methods=["*"],
    allow_headers=["*"]
)

# -------------------------------
# Data loading
# -------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"

# Load canonical data (ensure ingestion script ran)
_agri_df = pd.read_parquet(DATA_DIR / "agri_canonical.parquet")
_clim_df = pd.read_parquet(DATA_DIR / "climate_canonical.parquet")

# -------------------------------
# Request model
# -------------------------------
class QueryRequest(BaseModel):
    question: str

# -------------------------------
# Health check
# -------------------------------
@app.get("/")
def home():
    return {"message": "Project Samarth API is running. Use /query POST for questions."}

@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------
# Main query route
# -------------------------------
@app.post("/query")
def query(q: QueryRequest):
    try:
        text = q.question.lower()

        # -------------------------------
        #Compare average annual rainfall between two states
        if "compare the average annual rainfall" in text:
            # Parse states
            try:
                parts = text.split("compare the average annual rainfall in")[-1]
                if "and" in parts:
                    left = parts.split("and")
                    s1 = left[0].strip().split()[0].title()
                    s2 = left[1].strip().split()[0].title()
                else:
                    return {"error": "Couldn't parse two states."}

                # Parse number of years
                m = re.search(r"last (\d+)", text)
                N = int(m.group(1)) if m else 2

                df = _clim_df[_clim_df['state'].isin([s1, s2])]
                years = sorted(df['year'].unique(), reverse=True)[:N]
                df = df[df['year'].isin(years)]
                res = df.groupby('state')['rainfall'].mean().reset_index()

                # Convert to JSON-safe types
                return {
                    "answer": res.to_dict(orient="records"),
                    "years": [int(y) for y in years],
                    "citation": {"source": str(DATA_DIR / "climate_canonical.parquet")}
                }
            except Exception as e:
                return {"error": f"Failed rainfall query: {str(e)}"}

        # -------------------------------
        #Identify district with highest crop production
        elif "identify the district" in text and "highest production" in text:
            try:
                state_match = re.search(r"in (\w+)", text)
                crop_match = re.search(r"of (\w+)", text)
                if not state_match or not crop_match:
                    return {"error": "Could not parse state or crop"}
                state = state_match.group(1).title()
                crop = crop_match.group(1).title()

                df = _agri_df[(_agri_df['state'] == state) & (_agri_df['crop'] == crop)]
                if df.empty:
                    return {"answer": [], "citation": str(DATA_DIR / "agri_canonical.parquet")}

                latest_year = int(df['year'].max())
                latest_df = df[df['year'] == latest_year]
                max_row = latest_df.loc[latest_df['production'].idxmax()]

                return {
                    "answer": {
                        "state": state,
                        "district": max_row['district'],
                        "crop": crop,
                        "production": float(max_row['production']),
                        "year": latest_year
                    },
                    "citation": {"source": str(DATA_DIR / "agri_canonical.parquet")}
                }
            except Exception as e:
                return {"error": f"Failed crop district query: {str(e)}"}

        # -------------------------------
        #Fallback for unsupported questions
        else:
            return {"error": "Unsupported question. Currently handles rainfall comparison and district crop queries."}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
