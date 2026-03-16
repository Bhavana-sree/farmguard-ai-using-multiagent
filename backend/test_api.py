"""
FarmGuard AI - Complete API Test Script
Run this to test all your endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def print_separator(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def test_root():
    print_separator("TESTING ROOT ENDPOINT")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server. Make sure it's running!")
        print("   Run: python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_farmer_registration():
    print_separator("TESTING FARMER REGISTRATION")
    
    data = {
        "name": "Test Farmer",
        "phone": "9876543210",
        "village": "Green Village",
        "language": "English"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register_farmer", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            farmer_id = response.json().get("farmer_id")
            print(f"✅ Farmer registered with ID: {farmer_id}")
            return farmer_id
        else:
            print(f"❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_add_land(farmer_id):
    print_separator("TESTING ADD LAND")
    
    if not farmer_id:
        print("❌ No farmer ID available")
        return None
    
    data = {
        "farmer_id": farmer_id,
        "land_name": "Green Farm",
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    try:
        response = requests.post(f"{BASE_URL}/add_land", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            land_id = response.json().get("land_id")
            print(f"✅ Land added with ID: {land_id}")
            return land_id
        else:
            print(f"❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_solar_registration():
    print_separator("TESTING SOLAR PRODUCER REGISTRATION")
    
    data = {
        "name": "Test Solar Farm",
        "phone": "9876543210",
        "village": "Solar Village",
        "language": "English",
        "plant_capacity_kw": 100.5,
        "installation_date": "2024-01-15",
        "panel_type": "Monocrystalline",
        "inverter_type": "Grid-Tie",
        "grid_connected": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register_solar_producer", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            producer_id = response.json().get("producer_id")
            print(f"✅ Solar producer registered with ID: {producer_id}")
            return producer_id
        else:
            print(f"❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_add_solar_plant(producer_id):
    print_separator("TESTING ADD SOLAR PLANT")
    
    if not producer_id:
        print("❌ No producer ID available")
        return None
    
    data = {
        "producer_id": producer_id,
        "plant_name": "Solar Array 1",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "total_area_sqm": 500,
        "panel_count": 100,
        "tilt_angle": 30,
        "azimuth_angle": 180
    }
    
    try:
        response = requests.post(f"{BASE_URL}/add_solar_plant", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            plant_id = response.json().get("plant_id")
            print(f"✅ Solar plant added with ID: {plant_id}")
            return plant_id
        else:
            print(f"❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_company_registration():
    print_separator("TESTING COMPANY REGISTRATION")
    
    data = {
        "name": "Test Company",
        "phone": "9876543210",
        "email": "test@company.com",
        "village": "Mumbai",
        "language": "English",
        "registration_number": "U12345MH2020PTC123",
        "gst_number": "27AABCU1234E1Z5",
        "company_type": "Private Limited",
        "industry": "Technology",
        "year_established": "2020"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register_company", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            company_id = response.json().get("company_id")
            print(f"✅ Company registered with ID: {company_id}")
            return company_id
        else:
            print(f"❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_company_preferences(company_id):
    print_separator("TESTING COMPANY PREFERENCES")
    
    if not company_id:
        print("❌ No company ID available")
        return
    
    data = {
        "company_id": company_id,
        "carbon_goal": "Offset entire carbon footprint",
        "annual_requirement": "1000-5000 credits",
        "price_range": "₹850-900",
        "preferred_location": "India - All regions",
        "additional_preferences": "Prefer solar credits"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/company_preferences", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_list_companies():
    print_separator("TESTING LIST COMPANIES")
    
    try:
        response = requests.get(f"{BASE_URL}/companies")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_list_solar_producers():
    print_separator("TESTING LIST SOLAR PRODUCERS")
    
    try:
        response = requests.get(f"{BASE_URL}/solar_producers")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_company(company_id):
    print_separator("TESTING GET COMPANY DETAILS")
    
    if not company_id:
        print("❌ No company ID available")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/company/{company_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_solar_credits(producer_id):
    print_separator("TESTING GET SOLAR CREDITS")
    
    if not producer_id:
        print("❌ No producer ID available")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/solar_credits/{producer_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("\n" + "=" * 60)
    print(" 🚀 FARMGUARD AI - COMPLETE API TEST SUITE")
    print("=" * 60)
    
    # Step 1: Test server connection
    if not test_root():
        print("\n❌ Cannot proceed. Make sure server is running!")
        print("   Open a new terminal and run:")
        print("   cd C:\\AI_Hackathon\\FarmGuard\\backend")
        print("   python -m uvicorn app.main:app --reload")
        return
    
    # Step 2: Test Farmer endpoints
    print("\n📋 STEP 2: Testing Farmer Module")
    farmer_id = test_farmer_registration()
    if farmer_id:
        time.sleep(0.5)
        test_add_land(farmer_id)
    
    # Step 3: Test Solar endpoints
    print("\n📋 STEP 3: Testing Solar Module")
    producer_id = test_solar_registration()
    if producer_id:
        time.sleep(0.5)
        plant_id = test_add_solar_plant(producer_id)
        if plant_id:
            time.sleep(0.5)
            test_get_solar_credits(producer_id)
    
    # Step 4: Test Company endpoints
    print("\n📋 STEP 4: Testing Company Module")
    company_id = test_company_registration()
    if company_id:
        time.sleep(0.5)
        test_company_preferences(company_id)
        time.sleep(0.5)
        test_get_company(company_id)
    
    # Step 5: List all
    print("\n📋 STEP 5: Listing All Records")
    time.sleep(0.5)
    test_list_companies()
    time.sleep(0.5)
    test_list_solar_producers()
    
    print("\n" + "=" * 60)
    print(" ✅ ALL TESTS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()