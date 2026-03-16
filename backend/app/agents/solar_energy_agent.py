# Create this file at: C:\AI_Hackathon\FarmGuard\backend\app\agents\solar_energy_agent.py

class SolarEnergyAgent:
    """Calculates energy generation and carbon credits"""
    
    def __init__(self):
        pass
    
    async def calculate_energy_potential(self, plant_data, vision_result):
        """
        Calculate solar energy generation and carbon credits
        """
        # Mock irradiance data (in production, from Sentinel Hub)
        irradiance = {
            "avg_daily": 5.2,  # kWh/m²/day
            "annual": 1898,     # kWh/m²/year
            "peak_hours": 5.2
        }
        
        # Calculate energy
        panel_area = plant_data.total_area_sqm or vision_result["total_area_sqm"]
        efficiency = 0.75  # System efficiency
        
        daily_kwh = panel_area * irradiance["avg_daily"] * efficiency
        annual_kwh = daily_kwh * 365
        annual_mwh = annual_kwh / 1000
        
        # Carbon credits (1 MWh = 0.85 tonnes CO2)
        tonnes_co2 = annual_mwh * 0.85
        credits = round(tonnes_co2, 2)
        
        energy = {
            "daily_kwh": round(daily_kwh, 2),
            "annual_kwh": round(annual_kwh, 2),
            "annual_mwh": round(annual_mwh, 2)
        }
        
        carbon = {
            "carbon_credits": credits,
            "tonnes_co2_avoided": round(tonnes_co2, 2),
            "equivalent_trees": round(tonnes_co2 * 16.5, 0)
        }
        
        return {
            "energy_analysis": energy,
            "carbon_credits": carbon,
            "irradiance_data": irradiance
        }