class SolarVisionAgent:
    """Simplified vision agent for solar panel detection"""
    
    async def analyze_solar_panels(self, latitude, longitude):
        return {
            "panel_count": 120,
            "total_area_sqm": 250,
            "panel_density": 0.48,
            "confidence_score": 92,
            "image_analysis": {
                "detected_objects": 120,
                "average_panel_size": "2.1 sqm",
                "layout": "grid_pattern"
            }
        }

class SolarEnergyAgent:
    """Calculates energy generation and carbon credits"""
    
    async def calculate_energy_potential(self, plant_data, vision_result):
        # Mock irradiance data
        irradiance = {
            "avg_daily": 5.2,
            "annual": 1898,
            "peak_hours": 5.2
        }
        
        # Handle both object and tuple plant_data
        if hasattr(plant_data, 'total_area_sqm'):
            panel_area = plant_data.total_area_sqm
        elif isinstance(plant_data, tuple) and len(plant_data) > 5:
            panel_area = plant_data[5]  # total_area_sqm is at index 5
        else:
            panel_area = vision_result["total_area_sqm"]
        
        efficiency = 0.75
        
        daily_kwh = panel_area * irradiance["avg_daily"] * efficiency
        annual_kwh = daily_kwh * 365
        annual_mwh = annual_kwh / 1000
        
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

class SolarOrchestratorAgent:
    """Orchestrates all solar agents"""
    
    def __init__(self, validation_agent):
        self.validation_agent = validation_agent
        self.vision_agent = SolarVisionAgent()
        self.energy_agent = SolarEnergyAgent()
    
    async def run_pipeline(self, plant_id, plant_data):
        """
        Run the complete solar analysis pipeline
        """
        try:
            # Extract coordinates based on data type
            if isinstance(plant_data, tuple):
                # Tuple format: (id, producer_id, plant_name, latitude, longitude, ...)
                latitude = plant_data[3]
                longitude = plant_data[4]
            else:
                # Object format
                latitude = plant_data.latitude
                longitude = plant_data.longitude
            
            # Step 1: Vision analysis
            print(f"Running solar vision analysis for plant {plant_id}...")
            vision_result = await self.vision_agent.analyze_solar_panels(
                latitude, longitude
            )
            
            # Step 2: Energy calculation
            print("Calculating energy potential...")
            energy_result = await self.energy_agent.calculate_energy_potential(
                plant_data, vision_result
            )
            
            # Step 3: Validation
            print("Validating results...")
            validation_result = await self.validation_agent.validate_solar_data(
                plant_data, energy_result, vision_result
            )
            
            # Step 4: Combine results
            return {
                "vision_analysis": vision_result,
                "energy_analysis": energy_result["energy_analysis"],
                "carbon_credits": energy_result["carbon_credits"],
                "validation_result": validation_result,
                "plant_id": plant_id,
                "orchestration_status": "completed"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "orchestration_status": "failed"
            }