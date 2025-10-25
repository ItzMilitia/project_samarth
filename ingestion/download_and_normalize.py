import os
import requests
import pandas as pd
from pathlib import Path
from ingestion.ckan_client import search_packages, find_best_resource_for_package

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)

def download_resource(resource, target_name=None):
    url = resource.get("url") or resource.get("download_url")
    if not url:
        raise ValueError("Resource has no URL")
    if not target_name:
        target_name = os.path.basename(url.split("?")[0])
    out = DATA_DIR / target_name
    print("Downloading", url, "->", out)
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(out, "wb") as f:
        for chunk in r.iter_content(1024 * 32):
            f.write(chunk)
    return str(out)

def normalize_agriculture_table(path_in, path_out):
    print("Normalizing agriculture file:", path_in)
    if str(path_in).lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(path_in)
    else:
        df = pd.read_csv(path_in)

    col_map = {}
    lower = {c.lower(): c for c in df.columns}
    if 'year' in lower: col_map[lower['year']] = 'year'
    for key in ['state', 'state_name', 'st_name']:
        if key in lower: col_map[lower[key]] = 'state'; break
    for key in ['district', 'district_name']:
        if key in lower: col_map[lower[key]] = 'district'; break
    for key in ['crop', 'crop_name', 'crop_category']:
        if key in lower: col_map[lower[key]] = 'crop'; break
    for key in ['production', 'production_tonnes', 'production_quantity']:
        if key in lower: col_map[lower[key]] = 'production'; break

    df = df.rename(columns=col_map)
    keep = [c for c in ['year','state','district','crop','production'] if c in df.columns]
    df = df[keep]
    df.to_parquet(path_out, index=False)
    print("Wrote canonical agriculture to", path_out)
    return path_out

def normalize_climate_table(path_in, path_out):
    print("Normalizing climate file:", path_in)
    if str(path_in).lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(path_in)
    else:
        df = pd.read_csv(path_in)
    lower = {c.lower(): c for c in df.columns}
    col_map = {}
    if 'year' in lower: col_map[lower['year']] = 'year'
    for key in ['state', 'state_name', 'st_name']:
        if key in lower: col_map[lower[key]] = 'state'; break
    for key in ['district', 'district_name']:
        if key in lower: col_map[lower[key]] = 'district'; break
    for key in ['rainfall', 'rain', 'annual_rainfall']:
        if key in lower: col_map[lower[key]] = 'rainfall'; break
    for key in ['temp', 'temperature', 'avg_temp']:
        if key in lower: col_map[lower[key]] = 'temperature'; break

    df = df.rename(columns=col_map)
    keep = [c for c in ['year','state','district','rainfall','temperature'] if c in df.columns]
    df = df[keep]
    df.to_parquet(path_out, index=False)
    print("Wrote canonical climate to", path_out)
    return path_out
