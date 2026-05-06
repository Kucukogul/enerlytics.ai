from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from requests import exceptions as requests_exceptions

from enerlytics_ai.services.solar_data_service import fetch_historical_monthly_ghi_kwh_m2
from enerlytics_ai.services.solar_model_service import analyze_site

router = APIRouter()


class AnalyzeRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class AnalyzeResponse(BaseModel):
    data_source: str
    annual_energy_kwh: float
    estimated_lcoe: float
    lcoe_try_kwh: float
    simple_payback_years: float | None
    summary: str


class HistoricalSolarRequest(BaseModel):
    latitude: float = Field(..., ge=35.0, le=43.0)
    longitude: float = Field(..., ge=25.0, le=46.0)
    start_year: int = Field(..., ge=1984, le=2100)
    end_year: int = Field(..., ge=1984, le=2100)


class HistoricalMonthlyPoint(BaseModel):
    year: int
    month: int
    ghi_kwh_m2_day: float


class HistoricalAnnualSummaryPoint(BaseModel):
    year: int
    total_ghi_kwh_m2_day: float
    average_ghi_kwh_m2_day: float


class HistoricalSolarResponse(BaseModel):
    data_source: str
    parameter: str
    latitude: float
    longitude: float
    start_year: int
    end_year: int
    monthly_series: list[HistoricalMonthlyPoint]
    annual_summary: list[HistoricalAnnualSummaryPoint]


@router.post("/api/v1/analyze-site", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    try:
        result = analyze_site(payload.latitude, payload.longitude)
    except requests_exceptions.Timeout as exc:
        raise HTTPException(status_code=504, detail="Upstream solar data request timed out.") from exc
    except requests_exceptions.ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Could not connect to upstream solar data provider.") from exc
    except requests_exceptions.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Upstream solar data provider returned an error.") from exc
    except requests_exceptions.RequestException as exc:
        raise HTTPException(status_code=502, detail="Unexpected upstream request error during analysis.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"Analysis validation failed: {exc}") from exc
    return AnalyzeResponse(**result)


@router.post("/api/v1/historical-solar", response_model=HistoricalSolarResponse)
def historical_solar(payload: HistoricalSolarRequest) -> HistoricalSolarResponse:
    try:
        result = fetch_historical_monthly_ghi_kwh_m2(
            latitude=payload.latitude,
            longitude=payload.longitude,
            start_year=payload.start_year,
            end_year=payload.end_year,
        )
    except requests_exceptions.Timeout as exc:
        raise HTTPException(status_code=504, detail="Upstream solar data request timed out.") from exc
    except requests_exceptions.ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Could not connect to upstream solar data provider.") from exc
    except requests_exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        raise HTTPException(
            status_code=502,
            detail=f"Upstream solar data provider returned an error (status: {status_code}).",
        ) from exc
    except requests_exceptions.RequestException as exc:
        raise HTTPException(status_code=502, detail="Unexpected upstream request error during historical fetch.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"Historical solar validation failed: {exc}") from exc

    return HistoricalSolarResponse(
        data_source=result["source"],
        parameter=result["parameter"],
        latitude=result["latitude"],
        longitude=result["longitude"],
        start_year=result["start_year"],
        end_year=result["end_year"],
        monthly_series=result["monthly_series"],
        annual_summary=result["annual_summary"],
    )
