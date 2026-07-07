"""
Validation Agent - Local validation only (fast & reliable)
No Azure dependencies - uses scientific validation rules
"""

import json


class ValidationAgent:
    def __init__(self, base_url=None, api_key=None, model=None):
        """
        Initialize the validation agent (local only)
        """
        print(f"\n🔧 Initializing Validation Agent...")
        print(f"   Mode: Local scientific validation")
        print(f"   Status: Ready - No Azure dependency")

    def validate_data(self, trees, co2, iot_data):
        """
        Validate farm data using scientific rules
        """
        print(f"\n📡 Running scientific validation...")
        print(f"   Trees: {trees}, CO2: {co2}kg")
        
        return self._scientific_validation(trees, co2, iot_data)
    
    def _scientific_validation(self, trees, co2, iot_data):
        """
        Fast, reliable validation using IPCC scientific standards
        """
        
        issues = []
        warnings = []
        
        # ===========================================
        # 1. TREE COUNT VALIDATION
        # ===========================================
        if trees <= 0:
            issues.append("No trees detected")
        elif trees < 10:
            warnings.append("Very low tree density")
        elif trees > 10000:
            warnings.append(f"Unusually high tree count ({trees})")
        
        # ===========================================
        # 2. CO₂ VALIDATION (IPCC Standard)
        # Each healthy tree absorbs 20-25 kg CO₂ per year
        # ===========================================
        expected_co2_min = trees * 18  # Conservative estimate
        expected_co2_max = trees * 30  # Optimistic estimate
        
        if co2 <= 0:
            issues.append("Zero CO₂ removal detected")
        elif co2 < expected_co2_min * 0.5:
            warnings.append(f"CO₂ removal ({co2}kg) is lower than expected for {trees} trees")
        elif co2 > expected_co2_max * 2:
            warnings.append(f"CO₂ removal ({co2}kg) is higher than expected for {trees} trees")
        
        # ===========================================
        # 3. CARBON CREDIT CALCULATION
        # 1 credit = 1000 kg CO₂
        # ===========================================
        credits = co2 / 1000
        if credits > 0:
            if credits < 1:
                warnings.append(f"Small credit amount ({credits:.2f} credits)")
        
        # ===========================================
        # 4. IoT SENSOR VALIDATION
        # ===========================================
        soil_moisture = iot_data.get('soil_moisture_percent', 0)
        if soil_moisture > 100:
            issues.append("Soil moisture > 100% (invalid)")
        elif soil_moisture < 10:
            warnings.append("Very low soil moisture")
        
        temperature = iot_data.get('temperature_c', 0)
        if temperature > 60:
            issues.append(f"Temperature > 60°C (unrealistic)")
        elif temperature > 45:
            warnings.append("High temperature stress possible")
        
        humidity = iot_data.get('humidity_percent', 0)
        if humidity > 100:
            issues.append("Humidity > 100% (invalid)")
        
        soil_ph = iot_data.get('soil_ph', 7)
        if soil_ph < 4 or soil_ph > 10:
            issues.append(f"Soil pH {soil_ph} outside optimal range (4-10)")
        
        # ===========================================
        # 5. DETERMINE FINAL STATUS
        # ===========================================
        if len(issues) > 0:
            status = "Invalid"
            reason = "; ".join(issues[:3])
        elif len(warnings) > 0:
            status = "Valid with warnings"
            reason = "; ".join(warnings[:3])
        else:
            status = "Valid"
            reason = "All data passed scientific validation checks"
        
        return {
            "status": status,
            "reason": reason,
            "source": "IPCC Scientific Standards",
            "details": {
                "trees_validated": trees,
                "co2_validated": co2,
                "credits": round(credits, 2),
                "expected_co2_range": f"{expected_co2_min}-{expected_co2_max} kg",
                "soil_moisture": soil_moisture,
                "temperature": temperature,
                "soil_ph": soil_ph
            }
        }


# For testing
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 TESTING VALIDATION AGENT (Local Scientific)")
    print("="*60)
    
    agent = ValidationAgent()
    
    # Test Case 1: Valid farm data
    print("\n📊 TEST CASE 1: Valid Farm Data")
    test_data_1 = {
        "trees": 60,
        "co2": 2752.5,
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
    
    result = agent.validate_data(
        test_data_1["trees"],
        test_data_1["co2"],
        test_data_1["iot_data"]
    )
    
    print(f"\n✅ Result:")
    print(f"   Status: {result.get('status')}")
    print(f"   Reason: {result.get('reason')}")
    print(f"   Source: {result.get('source')}")
    
    # Test Case 2: Your actual data
    print("\n" + "="*60)
    print("📊 TEST CASE 2: Your Actual Farm Data")
    print("="*60)
    
    test_data_2 = {
        "trees": 60,
        "co2": 2752.5,
        "iot_data": {
            "soil_moisture_percent": 38.96,
            "temperature_c": 32.96,
            "humidity_percent": 73.77,
            "soil_ph": 7.24,
            "light_intensity_lux": 69773.54,
            "irrigation_status": "Moisture normal",
            "crop_stress": "Normal conditions"
        }
    }
    
    result2 = agent.validate_data(
        test_data_2["trees"],
        test_data_2["co2"],
        test_data_2["iot_data"]
    )
    
    print(f"\n✅ Result:")
    print(f"   Status: {result2.get('status')}")
    print(f"   Reason: {result2.get('reason')}")
    print(f"   Source: {result2.get('source')}")
    print(f"   Details:")
    for key, value in result2.get('details', {}).items():
        print(f"      {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ Validation Agent Ready!")
    print("   Mode: Local scientific validation")
    print("   Status: Fast & reliable")
    print("="*60)