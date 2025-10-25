import requests

DATA_GOV_BASE = "https://data.gov.in/"
CKAN_SEARCH = "https://data.gov.in/api/3/action/package_search"

def search_packages(q, rows=20):
    params = {"q": q, "rows": rows}
    try:
        r = requests.get(CKAN_SEARCH, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        if data.get("success"):
            return data["result"]["results"]
        return []
    except Exception as e:
        print("CKAN search failed:", e)
        return []

def find_best_resource_for_package(pkg, accept_formats=("CSV", "XLS", "XLSX")):
    resources = pkg.get("resources", [])
    for r in resources:
        fmt = (r.get("format") or "").upper()
        if any(a in fmt for a in accept_formats):
            return r
    return resources[0] if resources else None

if __name__ == "__main__":
    pkgs = search_packages("agriculture production state district crop")
    for p in pkgs[:5]:
        print(p.get("title"))
