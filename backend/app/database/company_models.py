"""
Company Database Models
Location: backend/app/database/company_models.py
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ===========================================
# Request/Response Models
# ===========================================

class CompanyRegistration(BaseModel):
    """Model for company registration request"""
    name: str
    phone: str
    email: Optional[str] = None
    village: str
    language: str
    registration_number: Optional[str] = None
    gst_number: Optional[str] = None
    company_type: Optional[str] = None
    industry: Optional[str] = None
    year_established: Optional[str] = None

class CompanyPreferences(BaseModel):
    """Model for company carbon credit preferences"""
    company_id: int
    carbon_goal: Optional[str] = None
    annual_requirement: Optional[str] = None
    price_range: Optional[str] = None
    preferred_location: Optional[str] = None
    additional_preferences: Optional[str] = None

class CompanyDocument(BaseModel):
    """Model for company document uploads"""
    company_id: int
    document_type: str  # 'pan', 'gst', 'incorporation', 'other'
    file_name: str
    file_path: Optional[str] = None

class CompanyPurchase(BaseModel):
    """Model for credit purchases"""
    company_id: int
    seller_type: str  # 'farmer' or 'solar'
    seller_id: int
    credits_purchased: float
    price_per_credit: float
    total_amount: float
    status: str = "completed"

# ===========================================
# Database Table Creation SQL
# ===========================================

COMPANY_TABLES_SQL = {
    "companies": """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            village TEXT NOT NULL,
            language TEXT NOT NULL,
            registration_number TEXT,
            gst_number TEXT,
            company_type TEXT,
            industry TEXT,
            year_established TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
    """,
    
    "company_preferences": """
        CREATE TABLE IF NOT EXISTS company_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            carbon_goal TEXT,
            annual_requirement TEXT,
            price_range TEXT,
            preferred_location TEXT,
            additional_preferences TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
        )
    """,
    
    "purchases": """
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            seller_type TEXT NOT NULL CHECK(seller_type IN ('farmer', 'solar')),
            seller_id INTEGER NOT NULL,
            credits_purchased REAL NOT NULL,
            price_per_credit REAL NOT NULL,
            total_amount REAL NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed' CHECK(status IN ('pending', 'completed', 'cancelled')),
            transaction_hash TEXT,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )
    """,
    
    "company_documents": """
        CREATE TABLE IF NOT EXISTS company_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            document_type TEXT NOT NULL CHECK(document_type IN ('pan', 'gst', 'incorporation', 'other')),
            file_name TEXT NOT NULL,
            file_path TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verified BOOLEAN DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
        )
    """,
    
    "company_activity_log": """
        CREATE TABLE IF NOT EXISTS company_activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            description TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
        )
    """
}