"""
Validation Agent - Connects to Azure AI Foundry/OpenAI
With better error handling and timeout management
"""

import json
import os
import time
import socket
import urllib.parse
from openai import AzureOpenAI
from openai import APIConnectionError, APIError, RateLimitError


class ValidationAgent:
    def __init__(self, base_url=None, api_key=None, model=None):
        """
        Initialize the validation agent with Azure OpenAI connection
        """
        
        # Get values from parameters or environment variables
        self.base_url = base_url or os.environ.get("AZURE_BASE_URL")
        self.api_key = api_key or os.environ.get("AZURE_API_KEY")
        self.model = model or os.environ.get("AZURE_MODEL", "gpt-4")
        
        # IMPORTANT FIX: Remove /openai/v1 if present (Azure SDK adds it automatically)
        if self.base_url and '/openai/' in self.base_url:
            # Extract just the base resource URL
            import re
            match = re.match(r'(https?://[^/]+)', self.base_url)
            if match:
                self.base_url = match.group(1)
                print(f"   Fixed URL (removed path): {self.base_url}")
        
        # Clean up the URL (remove trailing slash)
        if self.base_url and self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
        
        print(f"\n🔧 Initializing Validation Agent...")
        print(f"   Model: {self.model}")
        print(f"   Endpoint: {self.base_url}")
        print(f"   API Key exists: {bool(self.api_key)}")
        
        # Validate URL format
        if self.base_url and not self.base_url.startswith(('http://', 'https://')):
            self.base_url = f"https://{self.base_url}"
            print(f"   Fixed URL: {self.base_url}")
        
        # Initialize client with timeout
        try:
            self.client = AzureOpenAI(
                azure_endpoint=self.base_url,
                api_key=self.api_key,
                api_version="2024-02-15-preview",
                timeout=30.0,  # 30 second timeout
                max_retries=2
            )
            print("✅ Client initialized successfully")
        except Exception as e:
            print(f"❌ Client initialization error: {e}")
            self.client = None

    def validate_data(self, trees, co2, iot_data):
        """
        Validate farm data using Azure AI Foundry with fallback
        """
        
        print(f"\n📡 Calling Azure AI Foundry for validation...")
        print(f"   Trees: {trees}, CO2: {co2}kg")
        
        # Check if client is available
        if not self.client:
            print("⚠️ Azure client not initialized, using fallback")
            return self._fallback_validation(trees, co2, iot_data)
        
        # Check network connectivity first
        if not self._check_connectivity():
            print("⚠️ Network connectivity issue, using fallback")
            return self._fallback_validation(trees, co2, iot_data)
        
        # Create prompt
        prompt = self._create_prompt(trees, co2, iot_data)

        try:
            # Call Azure OpenAI with timeout
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert carbon verification AI. Always return JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=180,
                timeout=25  # 25 second timeout for this specific call
            )
            
            elapsed = time.time() - start_time
            print(f"✅ Azure AI responded in {elapsed:.1f}s")

            # Extract and parse response
            return self._parse_response(response)

        except APIConnectionError as e:
            print(f"❌ Connection error: {e}")
            return self._fallback_validation(trees, co2, iot_data)
            
        except RateLimitError as e:
            print(f"❌ Rate limit exceeded: {e}")
            return {
                "status": "Suspicious",
                "reason": "Rate limit exceeded, using basic validation",
                "source": "Rate limit fallback"
            }
            
        except APIError as e:
            print(f"❌ API error: {e}")
            return self._fallback_validation(trees, co2, iot_data)
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return self._fallback_validation(trees, co2, iot_data)
    
    def _create_prompt(self, trees, co2, iot_data):
        """Create the validation prompt"""
        
        return f"""
You are a carbon credit verification AI.

Check if the following farm data looks realistic and internally consistent.

Trees detected: {trees}
CO2 removed (kg): {co2}

IoT sensor data:
Soil moisture (%): {iot_data.get('soil_moisture_percent', 'N/A')}
Temperature (C): {iot_data.get('temperature_c', 'N/A')}
Humidity (%): {iot_data.get('humidity_percent', 'N/A')}
Soil pH: {iot_data.get('soil_ph', 'N/A')}
Light intensity (lux): {iot_data.get('light_intensity_lux', 'N/A')}
Irrigation status: {iot_data.get('irrigation_status', 'N/A')}
Crop stress: {iot_data.get('crop_stress', 'N/A')}

Return ONLY valid JSON in this format:
{{
  "status": "Valid or Suspicious",
  "reason": "short explanation"
}}
"""
    
    def _parse_response(self, response):
        """Parse the AI response and extract JSON"""
        
        try:
            content = response.choices[0].message.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()

            # Try to parse as JSON
            try:
                result = json.loads(content)
                result["source"] = "Azure AI Foundry"
                return result
                
            except json.JSONDecodeError:
                # Try to extract JSON from text
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1 and end > start:
                    result = json.loads(content[start:end + 1])
                    result["source"] = "Azure AI Foundry (extracted)"
                    return result
                
                # If all else fails
                return {
                    "status": "Suspicious",
                    "reason": f"Could not parse AI response: {content[:100]}",
                    "source": "Parse error"
                }
                
        except Exception as e:
            return {
                "status": "Error",
                "reason": f"Parse error: {str(e)}",
                "source": "Error"
            }
    
    def _check_connectivity(self):
        """Check if we can connect to Azure"""
        try:
            if not self.base_url:
                return False
            
            # Extract hostname from URL
            parsed = urllib.parse.urlparse(self.base_url)
            hostname = parsed.hostname or "api.openai.com"
            
            # Try to resolve DNS
            socket.gethostbyname(hostname)
            return True
            
        except Exception as e:
            print(f"   Network check failed: {e}")
            return False
    
    def _fallback_validation(self, trees, co2, iot_data):
        """Fallback when Azure AI is unavailable"""
        
        print("⚠️ Using fallback validation (AI unavailable)")
        
        issues = []
        
        # Check tree count
        if trees <= 0:
            issues.append("No trees detected")
        elif trees > 10000:
            issues.append(f"Very high tree count ({trees})")
        
        # Check CO2 (rough estimate: each tree absorbs 20-25kg CO2/year)
        expected_co2_low = trees * 15
        expected_co2_high = trees * 30
        
        if co2 <= 0:
            issues.append("Zero CO2 removal")
        elif co2 < expected_co2_low * 0.5:
            issues.append(f"CO2 removal ({co2}kg) seems low for {trees} trees")
        elif co2 > expected_co2_high * 2:
            issues.append(f"CO2 removal ({co2}kg) seems high for {trees} trees")
        else:
            # CO2 seems reasonable
            pass
        
        # Quick IoT checks
        if iot_data.get('soil_moisture_percent', 0) > 100:
            issues.append("Soil moisture > 100%")
        
        if iot_data.get('temperature_c', 0) > 60:
            issues.append("Temperature > 60°C unrealistic")
        
        if iot_data.get('humidity_percent', 0) > 100:
            issues.append("Humidity > 100%")
        
        # Determine status
        if len(issues) == 0:
            return {
                "status": "Valid",
                "reason": "All data passed basic validation checks",
                "source": "Fallback rules"
            }
        else:
            return {
                "status": "Suspicious",
                "reason": "; ".join(issues[:2]),
                "source": "Fallback rules"
            }


# For testing
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("\n" + "="*50)
    print("🧪 TESTING VALIDATION AGENT")
    print("="*50)
    
    agent = ValidationAgent()
    
    # Test with valid data
    test_data = {
        "trees": 382,
        "co2": 17524.25,
        "iot_data": {
            "soil_moisture_percent": 45,
            "temperature_c": 28,
            "humidity_percent": 65,
            "soil_ph": 6.8,
            "light_intensity_lux": 45000,
            "irrigation_status": "active",
            "crop_stress": "low"
        }
    }
    
    print("\n📊 Test Data:")
    print(f"   Trees: {test_data['trees']}")
    print(f"   CO2: {test_data['co2']} kg")
    
    result = agent.validate_data(
        test_data["trees"],
        test_data["co2"],
        test_data["iot_data"]
    )
    
    print(f"\n✅ Result:")
    print(f"   Status: {result.get('status')}")
    print(f"   Reason: {result.get('reason')}")
    print(f"   Source: {result.get('source', 'Unknown')}")
    
    print("\n" + "="*50)