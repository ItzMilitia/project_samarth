from pathlib import Path
from ingestion.download_and_normalize import normalize_agriculture_table, normalize_climate_table

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

SAMPLE_AGRI = DATA_DIR / "agri_sample.csv"
SAMPLE_CLIMATE = DATA_DIR / "climate_sample.csv"

OUT_AGRI = DATA_DIR / "agri_canonical.parquet"
OUT_CLIMATE = DATA_DIR / "climate_canonical.parquet"

print("Normalizing sample agriculture and climate data")
normalize_agriculture_table(SAMPLE_AGRI, OUT_AGRI)
normalize_climate_table(SAMPLE_CLIMATE, OUT_CLIMATE)
print("Done. Parquet files are under data/.")
