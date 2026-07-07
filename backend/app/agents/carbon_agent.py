"""
Carbon Agent - Calculates carbon credits from tree and vegetation data
"""

class CarbonAgent:
    def calculate_carbon(self, tree_count, avg_height=10):
        """Calculate carbon credits from tree count"""
        biomass_per_tree = 0.25 * (avg_height ** 2)
        total_biomass = biomass_per_tree * tree_count
        carbon = total_biomass * 0.5
        co2 = carbon * 3.67
        credits = round(co2 / 1000, 2)

        return {
            "trees": tree_count,
            "avg_height_m": avg_height,
            "biomass_kg": round(total_biomass, 2),
            "carbon_kg": round(carbon, 2),
            "co2_kg": round(co2, 2),
            "carbon_credits": credits
        }

    def calculate_from_ndvi(self, ndvi, area_hectares=1):
        """Calculate carbon credits based on NDVI"""
        
        # NDVI validation
        if ndvi <= 0:
            return {
                "trees": 0,
                "co2_kg": 0,
                "carbon_credits": 0,
                "value_inr": 0,
                "status": "NO_VEGETATION",
                "message": "No vegetation detected. Please select a location with trees."
            }
        
        if ndvi < 0.2:
            # Sparse vegetation
            tree_density = ndvi * 200  # Very low
            trees = int(tree_density * area_hectares)
            co2 = trees * 22.5
            credits = co2 / 1000
            value = credits * 83  # ₹83 per credit (in dollars, but we use INR)
            return {
                "trees": trees,
                "co2_kg": round(co2, 2),
                "carbon_credits": round(credits, 2),
                "value_inr": round(value, 2),
                "status": "LOW_VEGETATION",
                "message": "Low vegetation detected. Consider planting more trees."
            }
        
        # Normal NDVI calculation (ndvi >= 0.2)
        tree_density = 150 + (ndvi - 0.2) * 300
        trees = int(tree_density * area_hectares)
        co2 = trees * 22.5
        credits = co2 / 1000
        value = credits * 83
        
        return {
            "trees": trees,
            "co2_kg": round(co2, 2),
            "carbon_credits": round(credits, 2),
            "value_inr": round(value, 2),
            "status": "VALID",
            "message": "Analysis complete."
        }

    def calculate_from_trees(self, trees, avg_height=10):
        """Alias for calculate_carbon"""
        return self.calculate_carbon(trees, avg_height)



"""
Carbon Agent - Calculates carbon credits from trees, solar, and microalgae
"""

from app.agents.algae_agent import AlgaeAgent

class CarbonAgent:
    def __init__(self):
        self.algae_agent = AlgaeAgent()
    
    # Your existing tree calculation
    def calculate_from_trees(self, tree_count, avg_height=10):
        """Calculate credits from trees (existing code)"""
        biomass_per_tree = 0.25 * (avg_height ** 2)
        total_biomass = biomass_per_tree * tree_count
        carbon = total_biomass * 0.5
        co2 = carbon * 3.67
        credits = co2 / 1000
        
        return {
            "type": "Trees",
            "co2_kg": round(co2, 2),
            "carbon_credits": round(credits, 2)
        }
    
    # Your existing solar calculation
    def calculate_from_solar(self, energy_kwh, grid_factor=0.82):
        """Calculate credits from solar (existing code)"""
        co2_avoided = energy_kwh * grid_factor / 1000
        credits = co2_avoided / 1000
        
        return {
            "type": "Solar",
            "co2_kg": round(co2_avoided, 2),
            "carbon_credits": round(credits, 2)
        }
    
    # NEW: Calculate from microalgae
    def calculate_from_algae(self, biomass_kg, days_between_harvest=7):
        """Calculate credits from microalgae"""
        return self.algae_agent.calculate_credits(biomass_kg, days_between_harvest)
    
    # NEW: Combined calculation (all three types)
    def calculate_total(self, trees, solar_kwh, algae_biomass_kg):
        """Calculate total credits from all sources"""
        
        tree_result = self.calculate_from_trees(trees)
        solar_result = self.calculate_from_solar(solar_kwh)
        algae_result = self.calculate_from_algae(algae_biomass_kg)
        
        total_credits = (
            tree_result["carbon_credits"] +
            solar_result["carbon_credits"] +
            algae_result["carbon_credits"]
        )
        
        total_co2 = (
            tree_result["co2_kg"] +
            solar_result["co2_kg"] +
            algae_result["co2_kg"]
        )
        
        return {
            "trees": tree_result,
            "solar": solar_result,
            "microalgae": algae_result,
            "total_co2_kg": round(total_co2, 2),
            "total_carbon_credits": round(total_credits, 2),
            "message": f"🌳 + ☀️ + 🧫 = {round(total_credits, 2)} total credits!"
        }