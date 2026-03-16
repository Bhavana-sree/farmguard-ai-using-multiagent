from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import json
import os
from typing import Optional

# Import existing agents
from app.agents.orchestrator_agent import OrchestratorAgent
from app.agents.validation_agent import ValidationAgent
from app.services.report_service import ReportService

# Import solar agents
from app.agents.solar_orchestrator_agent import SolarOrchestratorAgent
from app.agents.solar_validation_agent import SolarValidationAgent

# Import from database folder
from app.database.solar_models import SolarProducerRegistration, SolarPlantData
from app.database.company_models import CompanyRegistration, CompanyPreferences, CompanyDocument, CompanyPurchase

# Import config
from app.config import AZURE_BASE_URL, AZURE_API_KEY, AZURE_MODEL

app = FastAPI(title="FarmGuard AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "farmguard.db"

# -----------------------------
# Azure / model config
# -----------------------------

# Farmer agents
validation_agent = ValidationAgent(
    base_url=AZURE_BASE_URL,
    api_key=AZURE_API_KEY,
    model=AZURE_MODEL
)

orchestrator_agent = OrchestratorAgent(validation_agent)
report_service = ReportService()

# Solar agents
solar_validation_agent = SolarValidationAgent(
    base_url=AZURE_BASE_URL,
    api_key=AZURE_API_KEY,
    model=AZURE_MODEL
)

solar_orchestrator = SolarOrchestratorAgent(solar_validation_agent)

# -----------------------------
# Database setup
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Farmer tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            village TEXT NOT NULL,
            language TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            land_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            land_id INTEGER NOT NULL,
            result_json TEXT NOT NULL,
            FOREIGN KEY (land_id) REFERENCES lands (id)
        )
    """)

    # Solar producer tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_producers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            village TEXT NOT NULL,
            language TEXT NOT NULL,
            plant_capacity_kw REAL,
            installation_date TEXT,
            panel_type TEXT,
            inverter_type TEXT,
            grid_connected BOOLEAN
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producer_id INTEGER NOT NULL,
            plant_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            total_area_sqm REAL,
            panel_count INTEGER,
            tilt_angle REAL,
            azimuth_angle REAL,
            FOREIGN KEY (producer_id) REFERENCES solar_producers (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER NOT NULL,
            analysis_date TEXT NOT NULL,
            energy_output_json TEXT NOT NULL,
            carbon_credits REAL,
            validation_json TEXT,
            FOREIGN KEY (plant_id) REFERENCES solar_plants (id)
        )
    """)

    # Company tables
    cursor.execute("""
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
    """)

    cursor.execute("""
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
    """)

    cursor.execute("""
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
    """)

    cursor.execute("""
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
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            description TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized successfully")
    print("🚀 Server running at http://127.0.0.1:8000")


# -----------------------------
# Request models (Farmer)
# -----------------------------
class FarmerRegistration(BaseModel):
    name: str
    phone: str
    village: str
    language: str


class LandCreate(BaseModel):
    farmer_id: int
    latitude: float
    longitude: float
    land_name: str


class FullReportRequest(BaseModel):
    farmer_data: dict
    land_data: dict
    crop_data: dict
    analysis_result: dict


# -----------------------------
# Routes - Farmer
# -----------------------------
@app.get("/")
def root():
    return {"message": "FarmGuard AI backend is running"}


@app.post("/register_farmer")
def register_farmer(data: FarmerRegistration):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO farmers (name, phone, village, language)
            VALUES (?, ?, ?, ?)
        """, (data.name, data.phone, data.village, data.language))

        farmer_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "message": "Farmer registered successfully",
            "farmer_id": farmer_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register farmer: {str(e)}")


@app.post("/add_land")
def add_land(data: LandCreate):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM farmers WHERE id = ?", (data.farmer_id,))
        farmer = cursor.fetchone()

        if not farmer:
            conn.close()
            raise HTTPException(status_code=404, detail="Farmer not found")

        cursor.execute("""
            INSERT INTO lands (farmer_id, land_name, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """, (data.farmer_id, data.land_name, data.latitude, data.longitude))

        land_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "message": "Land added successfully",
            "land_id": land_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add land: {str(e)}")


@app.post("/analyze_land/{land_id}")
def analyze_land(land_id: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, farmer_id, land_name, latitude, longitude
            FROM lands
            WHERE id = ?
        """, (land_id,))
        land = cursor.fetchone()

        if not land:
            conn.close()
            raise HTTPException(status_code=404, detail="Land not found")

        _, farmer_id, land_name, latitude, longitude = land

        result = orchestrator_agent.run_pipeline(latitude, longitude)

        result_json = json.dumps(result)

        cursor.execute("""
            INSERT INTO analyses (land_id, result_json)
            VALUES (?, ?)
        """, (land_id, result_json))

        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "message": "Analysis completed successfully",
            "analysis_id": analysis_id,
            "land_id": land_id,
            "land_name": land_name,
            "result": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze land: {str(e)}")


@app.post("/generate_full_report")
def generate_full_report(request: FullReportRequest):
    try:
        report_payload = {
            **request.analysis_result,
            "farmer_data": request.farmer_data,
            "land_data": request.land_data,
            "crop_data": request.crop_data,
        }

        filepath = report_service.generate_pdf_report(report_payload)

        return FileResponse(
            path=filepath,
            media_type="application/pdf",
            filename="FarmGuard_AI_Report.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@app.get("/generate_report")
def generate_report(latitude: float, longitude: float):
    try:
        result = orchestrator_agent.run_pipeline(latitude, longitude)

        report_payload = {
            **result,
            "farmer_data": {},
            "land_data": {
                "latitude": latitude,
                "longitude": longitude
            },
            "crop_data": {},
        }

        filepath = report_service.generate_pdf_report(report_payload)

        return FileResponse(
            path=filepath,
            media_type="application/pdf",
            filename="FarmGuard_AI_Report.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


# -----------------------------
# Routes - Solar Producer
# -----------------------------
@app.post("/register_solar_producer")
def register_solar_producer(data: SolarProducerRegistration):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO solar_producers 
            (name, phone, village, language, plant_capacity_kw, installation_date, panel_type, inverter_type, grid_connected)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data.name, data.phone, data.village, data.language, 
              data.plant_capacity_kw, data.installation_date, 
              data.panel_type, data.inverter_type, data.grid_connected))
        
        producer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "message": "Solar producer registered successfully",
            "producer_id": producer_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register solar producer: {str(e)}")


@app.post("/add_solar_plant")
def add_solar_plant(data: SolarPlantData):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verify producer exists
        cursor.execute("SELECT id FROM solar_producers WHERE id = ?", (data.producer_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Solar producer not found")
        
        cursor.execute("""
            INSERT INTO solar_plants 
            (producer_id, plant_name, latitude, longitude, total_area_sqm, panel_count, tilt_angle, azimuth_angle)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (data.producer_id, data.plant_name, data.latitude, data.longitude,
              data.total_area_sqm, data.panel_count, data.tilt_angle, data.azimuth_angle))
        
        plant_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "message": "Solar plant added successfully",
            "plant_id": plant_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add solar plant: {str(e)}")


@app.post("/analyze_solar_plant/{plant_id}")
async def analyze_solar_plant(plant_id: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get plant data
        cursor.execute("""
            SELECT id, producer_id, plant_name, latitude, longitude, 
                   total_area_sqm, panel_count, tilt_angle, azimuth_angle
            FROM solar_plants 
            WHERE id = ?
        """, (plant_id,))
        
        plant = cursor.fetchone()
        if not plant:
            conn.close()
            raise HTTPException(status_code=404, detail="Solar plant not found")
        
        # Run solar analysis pipeline
        result = await solar_orchestrator.run_pipeline(plant_id, plant)
        
        if result["orchestration_status"] == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Solar analysis failed"))
        
        # Save analysis
        cursor.execute("""
            INSERT INTO solar_analyses 
            (plant_id, analysis_date, energy_output_json, carbon_credits, validation_json)
            VALUES (?, datetime('now'), ?, ?, ?)
        """, (plant_id, 
              json.dumps(result["energy_analysis"]),
              result["carbon_credits"]["carbon_credits"],
              json.dumps(result["validation_result"])))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "message": "Solar analysis completed successfully",
            "analysis_id": analysis_id,
            "plant_id": plant_id,
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze solar plant: {str(e)}")


@app.get("/solar_credits/{producer_id}")
def get_solar_credits(producer_id: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COALESCE(SUM(sa.carbon_credits), 0) as total_credits,
                COUNT(DISTINCT sp.id) as plant_count,
                COALESCE(AVG(sa.carbon_credits), 0) as avg_credits
            FROM solar_producers p
            LEFT JOIN solar_plants sp ON p.id = sp.producer_id
            LEFT JOIN solar_analyses sa ON sp.id = sa.plant_id
            WHERE p.id = ?
        """, (producer_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            "producer_id": producer_id,
            "total_credits": round(result[0] or 0, 2),
            "plant_count": result[1] or 0,
            "average_credits_per_plant": round(result[2] or 0, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get solar credits: {str(e)}")


@app.get("/solar_producers")
def list_solar_producers():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, village, plant_capacity_kw, panel_type
            FROM solar_producers
            ORDER BY id DESC
        """)
        
        producers = cursor.fetchall()
        conn.close()
        
        return {
            "producers": [
                {
                    "id": p[0],
                    "name": p[1],
                    "village": p[2],
                    "capacity_kw": p[3],
                    "panel_type": p[4]
                }
                for p in producers
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list solar producers: {str(e)}")


@app.get("/solar_plants/{producer_id}")
def list_solar_plants(producer_id: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, plant_name, latitude, longitude, total_area_sqm, panel_count
            FROM solar_plants
            WHERE producer_id = ?
        """, (producer_id,))
        
        plants = cursor.fetchall()
        conn.close()
        
        return {
            "producer_id": producer_id,
            "plants": [
                {
                    "id": p[0],
                    "plant_name": p[1],
                    "latitude": p[2],
                    "longitude": p[3],
                    "area_sqm": p[4],
                    "panel_count": p[5]
                }
                for p in plants
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list solar plants: {str(e)}")


# -----------------------------
# COMPANY ENDPOINTS
# -----------------------------

@app.post("/register_company")
def register_company(data: CompanyRegistration):
    """Register a new company"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insert company data
        cursor.execute("""
            INSERT INTO companies 
            (name, phone, email, village, language, registration_number, gst_number, company_type, industry, year_established)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.name,
            data.phone,
            data.email,
            data.village,
            data.language,
            data.registration_number,
            data.gst_number,
            data.company_type,
            data.industry,
            data.year_established
        ))
        
        company_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Log activity
        log_company_activity(company_id, "registration", "Company registered successfully")
        
        return {
            "message": "Company registered successfully",
            "company_id": company_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register company: {str(e)}")


@app.post("/company_preferences")
def save_company_preferences(data: CompanyPreferences):
    """Save company carbon credit preferences"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if company exists
        cursor.execute("SELECT id FROM companies WHERE id = ?", (data.company_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Insert preferences
        cursor.execute("""
            INSERT INTO company_preferences 
            (company_id, carbon_goal, annual_requirement, price_range, preferred_location, additional_preferences)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.company_id,
            data.carbon_goal,
            data.annual_requirement,
            data.price_range,
            data.preferred_location,
            data.additional_preferences
        ))
        
        conn.commit()
        conn.close()
        
        log_company_activity(data.company_id, "preferences", "Carbon credit preferences saved")
        
        return {"message": "Preferences saved successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/company_document")
def upload_company_document(data: CompanyDocument):
    """Upload company verification document"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO company_documents 
            (company_id, document_type, file_name, file_path)
            VALUES (?, ?, ?, ?)
        """, (
            data.company_id,
            data.document_type,
            data.file_name,
            data.file_path
        ))
        
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_company_activity(data.company_id, "document_upload", f"Uploaded {data.document_type} document")
        
        return {"message": "Document uploaded", "document_id": doc_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/company/{company_id}")
def get_company_details(company_id: int):
    """Get complete company details with preferences and documents"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get company details
        cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
        company = cursor.fetchone()
        
        if not company:
            conn.close()
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Get company preferences
        cursor.execute("SELECT * FROM company_preferences WHERE company_id = ? ORDER BY id DESC LIMIT 1", (company_id,))
        preferences = cursor.fetchone()
        
        # Get company documents
        cursor.execute("SELECT document_type, file_name, uploaded_at, verified FROM company_documents WHERE company_id = ?", (company_id,))
        documents = cursor.fetchall()
        
        # Get recent purchases
        cursor.execute("""
            SELECT id, seller_type, seller_id, credits_purchased, price_per_credit, total_amount, purchase_date, status 
            FROM purchases 
            WHERE company_id = ? 
            ORDER BY purchase_date DESC 
            LIMIT 5
        """, (company_id,))
        purchases = cursor.fetchall()
        
        conn.close()
        
        return {
            "company": {
                "id": company[0],
                "name": company[1],
                "phone": company[2],
                "email": company[3],
                "village": company[4],
                "language": company[5],
                "registration_number": company[6],
                "gst_number": company[7],
                "company_type": company[8],
                "industry": company[9],
                "year_established": company[10],
                "registered_at": company[11],
                "status": company[12]
            },
            "preferences": {
                "carbon_goal": preferences[2] if preferences else None,
                "annual_requirement": preferences[3] if preferences else None,
                "price_range": preferences[4] if preferences else None,
                "preferred_location": preferences[5] if preferences else None
            } if preferences else None,
            "documents": [
                {
                    "type": d[0],
                    "file_name": d[1],
                    "uploaded_at": d[2],
                    "verified": bool(d[3])
                } for d in documents
            ],
            "recent_purchases": [
                {
                    "id": p[0],
                    "seller_type": p[1],
                    "seller_id": p[2],
                    "credits": p[3],
                    "price": p[4],
                    "total": p[5],
                    "date": p[6],
                    "status": p[7]
                } for p in purchases
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# FIXED COMPANIES ENDPOINT
# ===========================================
@app.get("/companies")
def list_companies():
    """List all registered companies - FIXED VERSION"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # First try the full query with purchases
        try:
            cursor.execute("""
                SELECT c.id, c.name, c.village, c.company_type, c.industry, 
                       COUNT(DISTINCT p.id) as purchase_count,
                       COALESCE(SUM(p.credits_purchased), 0) as total_credits
                FROM companies c
                LEFT JOIN purchases p ON c.id = p.company_id
                GROUP BY c.id
                ORDER BY c.registered_at DESC
            """)
            
            companies = cursor.fetchall()
            
            return {
                "companies": [
                    {
                        "id": c[0],
                        "name": c[1],
                        "village": c[2] if c[2] else "Unknown",
                        "type": c[3] if c[3] else "N/A",
                        "industry": c[4] if c[4] else "N/A",
                        "purchases": c[5] if c[5] else 0,
                        "total_credits": c[6] if c[6] else 0
                    } for c in companies
                ]
            }
        except Exception as e:
            # If the full query fails, return a simplified version
            print(f"⚠️ Full companies query failed, using simplified version: {e}")
            cursor.execute("""
                SELECT id, name, village, company_type, industry 
                FROM companies
                ORDER BY registered_at DESC
            """)
            
            companies = cursor.fetchall()
            conn.close()
            
            return {
                "companies": [
                    {
                        "id": c[0],
                        "name": c[1],
                        "village": c[2] if c[2] else "Unknown",
                        "type": c[3] if c[3] else "N/A",
                        "industry": c[4] if c[4] else "N/A",
                        "purchases": 0,
                        "total_credits": 0
                    } for c in companies
                ],
                "note": "Purchase data temporarily unavailable"
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# SIMPLE COMPANIES ENDPOINT (Backup)
# ===========================================
@app.get("/companies_simple")
def list_companies_simple():
    """Simple company list without purchase data"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, village, company_type, industry FROM companies ORDER BY registered_at DESC")
        companies = cursor.fetchall()
        conn.close()
        
        return {
            "companies": [
                {
                    "id": c[0],
                    "name": c[1],
                    "village": c[2] if c[2] else "Unknown",
                    "type": c[3] if c[3] else "N/A",
                    "industry": c[4] if c[4] else "N/A"
                } for c in companies
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/company_purchase")
def create_purchase(data: CompanyPurchase):
    """Record a credit purchase by company"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO purchases 
            (company_id, seller_type, seller_id, credits_purchased, price_per_credit, total_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.company_id,
            data.seller_type,
            data.seller_id,
            data.credits_purchased,
            data.price_per_credit,
            data.total_amount,
            data.status
        ))
        
        purchase_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_company_activity(data.company_id, "purchase", f"Purchased {data.credits_purchased} credits")
        
        return {
            "message": "Purchase recorded successfully",
            "purchase_id": purchase_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def log_company_activity(company_id, activity_type, description):
    """Helper function to log company activities"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO company_activity_log (company_id, activity_type, description)
            VALUES (?, ?, ?)
        """, (company_id, activity_type, description))
        conn.commit()
        conn.close()
    except:
        pass  # Don't fail if logging fails