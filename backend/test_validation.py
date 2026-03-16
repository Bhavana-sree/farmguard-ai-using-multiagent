"""
Test the Validation Agent with Azure AI Foundry
"""

import os
from dotenv import load_dotenv
from app.agents.validation_agent import ValidationAgent

# Load environment variables
load_dotenv()

def test_validation():
    print("🧪 Testing Validation Agent with Azure AI Foundry...")
    
    # Create validation agent
    agent = ValidationAgent()
    
    # Sample analysis data
    test_data = {
        "ndvi": 0.73,
        "estimated_trees": 382,
        "co2_kg": 17524.25,
        "carbon_credits": 17.52,
        "land_area": 2.5
    }
    
    print(f"\n📊 Test Data: {test_data}")
    
    # Validate with Azure AI
    result = agent.validate_analysis(test_data)
    
    print(f"\n✅ Validation Result:")
    print(f"   Status: {result['status']}")
    print(f"   Reason: {result['reason']}")
    print(f"   Source: {result.get('source', 'Unknown')}")
    
    return result

if __name__ == "__main__":
    test_validation()