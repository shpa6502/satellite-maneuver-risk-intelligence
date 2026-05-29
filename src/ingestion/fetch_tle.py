import requests
import os
import json
from datetime import datetime, timezone

BASE_URL = "https://celestrak.org/NORAD/elements/gp.php"

GROUPS = {
    "active": "active",
    "starlink": "starlink",
    "stations": "stations",
    "weather": "weather",
    "resource": "resource"
}

def fetch_group(group_key: str = "active", save: bool = True) -> list:
    if group_key not in GROUPS:
        raise ValueError(
            f"Invalid group key '{group_key}'. "
            f"Valid options are: {', '.join(GROUPS.keys())}"
        )

    group_name = GROUPS[group_key]
    params = {"GROUP": group_name, "FORMAT": "json"}

    print(f"[fetch] Requesting group='{group_name}'...")
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    print(f"[fetch] Received {len(data)} objects.")

    if save:
        os.makedirs("data/raw", exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = f"data/raw/tle_{group_key}_{ts}.json"

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"[fetch] Saved → {path}")

    return data


if __name__ == "__main__":
    data = fetch_group("active")
    first = data[0]
    print(f"\nFirst object : {first.get('OBJECT_NAME')}")
    print(f"NORAD ID     : {first.get('NORAD_CAT_ID')}")
    print(f"Epoch        : {first.get('EPOCH')}")
    print(f"Inclination  : {first.get('INCLINATION')}")
    print(f"Eccentricity : {first.get('ECCENTRICITY')}")