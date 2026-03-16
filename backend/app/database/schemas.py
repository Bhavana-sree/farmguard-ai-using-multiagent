from pydantic import BaseModel


class FarmerCreate(BaseModel):
    name: str
    phone: str
    village: str
    language: str


class LandCreate(BaseModel):
    farmer_id: int
    latitude: float
    longitude: float
    land_name: str | None = None


class CompanyCreate(BaseModel):
    name: str
    email: str
    industry: str


class PurchaseCreate(BaseModel):
    company_id: int
    analysis_id: int
    credits_bought: float