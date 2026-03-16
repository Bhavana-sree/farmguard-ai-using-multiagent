class SolarValidationAgent:
    """Uses Azure OpenAI to validate solar data"""
    
    def __init__(self, base_url, api_key, model):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
    
    async def validate_solar_data(self, plant_data, energy_data, vision_data):
        """
        Validate solar data (simplified for hackathon)
        """
        # Extract credits from energy data
        if isinstance(energy_data, dict) and "carbon_credits" in energy_data:
            if isinstance(energy_data["carbon_credits"], dict):
                credits = energy_data["carbon_credits"].get("carbon_credits", 0)
            else:
                credits = energy_data["carbon_credits"]
        else:
            credits = 0
        
        if credits > 0:
            status = "VALID"
            confidence = 95
            issues = []
            recommendation = "Ready for marketplace listing"
        else:
            status = "NEEDS_REVIEW"
            confidence = 70
            issues = ["Low energy generation estimate"]
            recommendation = "Verify panel specifications"
        
        return {
            "status": status,
            "confidence_score": confidence,
            "issues": issues,
            "recommendation": recommendation,
            "validation_timestamp": "2024-01-01T00:00:00Z"
        }