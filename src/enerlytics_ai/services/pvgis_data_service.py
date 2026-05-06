from typing import Any, Dict

import requests

from enerlytics_ai.app.config import settings
from enerlytics_ai.utils.helpers import monthly_to_annual_irradiance


def fetch_annual_ghi_kwh_m2(latitude: float, longitude: float) -> Dict[str, Any]:
    """Fetch location-based solar data from PVGIS and normalize output shape.

    This is a minimal first-step provider implementation so the project can switch
    data sources by configuration without changing API/service contracts.
    """
    params = {
        "lat": latitude,
        "lon": longitude,
        "outputformat": "json",
    }

    response = requests.get(
        settings.pvgis_base_url,
        params=params,
        timeout=settings.request_timeout_seconds,
    )
    response.raise_for_status()
    payload = response.json()

    monthly_entries = payload.get("outputs", {}).get("monthly", [])
    if not isinstance(monthly_entries, list) or len(monthly_entries) < 12:
        raise ValueError("Incomplete monthly data returned by PVGIS.")

    month_keys = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    monthly_daily_ghi: Dict[str, float] = {}
    for index, month_key in enumerate(month_keys, start=1):
        entry = next((m for m in monthly_entries if int(m.get("month", -1)) == index), None)
        if entry is None:
            raise ValueError("Missing one or more monthly records in PVGIS response.")
        monthly_daily_ghi[month_key] = float(entry.get("H(h)_m"))

    annual_ghi = monthly_to_annual_irradiance(monthly_daily_ghi)
    return {
        "source": "PVGIS",
        "annual_irradiance_kwh_m2": round(annual_ghi, 2),
        "monthly_daily_ghi": monthly_daily_ghi,
    }