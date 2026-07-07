"""
Configuration for FarmGuard AI Backend
Loads configuration from .env
"""

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# ==================================================
# AI Configuration (Currently Azure - will migrate later)
# ==================================================

AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_BASE_URL = os.getenv("AZURE_BASE_URL", "")
AZURE_MODEL = os.getenv("AZURE_MODEL", "gpt-4")

# ==================================================
# Vision Configuration
# ==================================================

AZURE_VISION_ENDPOINT = os.getenv(
    "AZURE_VISION_ENDPOINT",
    "https://farmguard-vision.cognitiveservices.azure.com/"
)

AZURE_VISION_KEY = os.getenv(
    "AZURE_VISION_KEY",
    AZURE_API_KEY
)

# ==================================================
# Google APIs
# ==================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# ==================================================
# Sentinel Hub
# ==================================================

SENTINELHUB_CLIENT_ID = os.getenv(
    "SENTINELHUB_CLIENT_ID",
    "sentinel-demo-client"
)

SENTINELHUB_CLIENT_SECRET = os.getenv(
    "SENTINELHUB_CLIENT_SECRET",
    "sentinel-demo-secret"
)

SENTINELHUB_INSTANCE_ID = os.getenv(
    "SENTINELHUB_INSTANCE_ID",
    "default-instance"
)

# ==================================================
# Database
# ==================================================

DB_PATH = os.getenv("DB_PATH", "farmguard.db")

# ==================================================
# Status Display
# ==================================================

print("\n" + "=" * 50)
print("🔧 FARMGUARD AI CONFIGURATION")
print("=" * 50)

print(f"Azure OpenAI      : {'Configured' if AZURE_API_KEY else 'Not Configured'}")
print(f"Azure Vision      : {'Configured' if AZURE_VISION_KEY else 'Not Configured'}")
print(f"Google API        : {'Configured' if GOOGLE_API_KEY else 'Not Configured'}")
print("Sentinel Hub      : Demo Mode")
print(f"Database          : {DB_PATH}")

print("=" * 50 + "\n")