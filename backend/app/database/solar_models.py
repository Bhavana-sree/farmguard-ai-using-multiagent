from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SolarProducerRegistration(BaseModel):
    name: str
    phone: str
    village: str
    language: str
    plant_capacity_kw: float
    installation_date: str
    panel_type: str
    inverter_type: str
    grid_connected: bool

class SolarPlantData(BaseModel):
    producer_id: int
    plant_name: str
    latitude: float
    longitude: float
    total_area_sqm: float
    panel_count: Optional[int] = 0
    tilt_angle: Optional[float] = 0
    azimuth_angle: Optional[float] = 0

class SolarAnalysisResult(BaseModel):
    plant_id: int
    analysis_date: datetime
    energy_output: dict
    carbon_credits: float
    validation: dict

class SolarTransaction(BaseModel):
    producer_id: int
    buyer_company: str
    credits_sold: float
    price_per_credit: float
    total_amount: float
    status: str = "completed"