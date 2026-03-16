"""
Database models package
This file makes the database folder a Python package
"""

from .company_models import (
    CompanyRegistration,
    CompanyPreferences,
    CompanyDocument,
    CompanyPurchase,
    COMPANY_TABLES_SQL
)

from .solar_models import (
    SolarProducerRegistration,
    SolarPlantData,
    SolarAnalysisResult,
    SolarTransaction
)

__all__ = [
    # Company models
    'CompanyRegistration',
    'CompanyPreferences',
    'CompanyDocument',
    'CompanyPurchase',
    'COMPANY_TABLES_SQL',
    
    # Solar models
    'SolarProducerRegistration',
    'SolarPlantData',
    'SolarAnalysisResult',
    'SolarTransaction'
]