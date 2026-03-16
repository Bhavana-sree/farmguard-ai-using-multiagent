"""
Simple test for Azure OpenAI connectivity
"""

import os
from dotenv import load_dotenv
import httpx

load_dotenv()

def test_connection():
    print("🔍 Testing Azure OpenAI connection...")
    
    api_key = os.environ.get("AZURE_API_KEY")
    base_url = os.environ.get("AZURE_BASE_URL")
    
    print(f"API Key exists: {bool(api_key)}")
    print(f"Base URL: {base_url}")
    
    if not api_key or not base_url:
        print("❌ Missing credentials in .env file")
        return False
    
    # Clean URL
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    
    # Test DNS resolution
    import socket
    try:
        from urllib.parse import urlparse
        hostname = urlparse(base_url).hostname
        if hostname:
            ip = socket.gethostbyname(hostname)
            print(f"✅ DNS resolution: {hostname} -> {ip}")
    except Exception as e:
        print(f"⚠️ DNS resolution failed: {e}")
    
    # Test HTTP connection
    try:
        response = httpx.get(
            f"{base_url}/openai/deployments",
            headers={"api-key": api_key},
            timeout=10
        )
        print(f"✅ HTTP connection successful (status: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()