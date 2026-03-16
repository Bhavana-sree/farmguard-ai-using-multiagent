"""
Configuration for FarmGuard AI Backend
Loads from .env file automatically
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===========================================
# Azure OpenAI Configuration
# ===========================================
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")
AZURE_BASE_URL = os.environ.get("AZURE_BASE_URL")
AZURE_MODEL = os.environ.get("AZURE_MODEL", "gpt-4")

# ===========================================
# Azure Vision Configuration (ADD THIS)
# ===========================================
AZURE_VISION_ENDPOINT = os.environ.get("AZURE_VISION_ENDPOINT", "https://farmguard-vision.cognitiveservices.azure.com/")
AZURE_VISION_KEY = os.environ.get("AZURE_VISION_KEY", AZURE_API_KEY)  # Use same key if not specified

# ===========================================
# Google API Configuration (Maps & Solar)
# ===========================================
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# ===========================================
# Sentinel Hub Configuration (for satellite imagery)
# ===========================================
SENTINELHUB_CLIENT_ID = os.environ.get("SENTINELHUB_CLIENT_ID", "sentinel-demo-client")
SENTINELHUB_CLIENT_SECRET = os.environ.get("SENTINELHUB_CLIENT_SECRET", "sentinel-demo-secret")
SENTINELHUB_INSTANCE_ID = os.environ.get("SENTINELHUB_INSTANCE_ID", "default-instance")

# ===========================================
# Database Configuration
# ===========================================
DB_PATH = os.environ.get("DB_PATH", "farmguard.db")

# ===========================================
# Validation - Check required variables
# ===========================================
print("\n" + "="*50)
print("🔧 FARMGUARD AI CONFIGURATION")
print("="*50)

missing_vars = []
if not AZURE_API_KEY:
    missing_vars.append("AZURE_API_KEY")
if not AZURE_BASE_URL:
    missing_vars.append("AZURE_BASE_URL")

if missing_vars:
    print("⚠️  Warning: Missing required Azure variables:", ", ".join(missing_vars))
else:
    print("✅ Azure OpenAI: Configured")

# Vision config status
print(f"✅ Azure Vision: {'Using default endpoint' if AZURE_VISION_ENDPOINT else 'Not configured'}")

# Google config status
print(f"✅ Google API: {'Configured' if GOOGLE_API_KEY else 'Not configured'}")

# Sentinel config status
print(f"✅ Sentinel Hub: Demo mode enabled")

print("="*50 + "\n")