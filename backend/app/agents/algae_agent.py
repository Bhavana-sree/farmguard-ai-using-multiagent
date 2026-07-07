"""
Algae Agent - Calculates carbon credits from microalgae (Chlorella)
"""

class AlgaeAgent:
    def __init__(self):
        print("🧫 Algae Agent initialized")
        print("   Type: Chlorella Microalgae")
        print("   CO₂ capture: 2.6x more efficient than Spirulina")
    
    def calculate_credits(self, biomass_kg, days_between_harvest=7):
        """
        Calculate carbon credits from algae harvest
        
        SCIENTIFIC FORMULA:
        - 1 kg Chlorella biomass = 2.0 kg CO₂ captured (scientific average)
        - 1 carbon credit = 1000 kg CO₂
        
        Example: If you harvest 100 kg algae:
        CO₂ captured = 100 × 2.0 = 200 kg
        Credits = 200 ÷ 1000 = 0.2 credits
        """
        
        # STEP 1: Calculate CO₂ captured from this harvest
        # Chlorella captures 2.0 kg CO₂ per kg of biomass
        CO2_CAPTURE_FACTOR = 2.0
        co2_captured = biomass_kg * CO2_CAPTURE_FACTOR
        
        # STEP 2: Calculate annual CO₂ capture
        # Number of harvests per year
        harvests_per_year = 365 / days_between_harvest
        annual_co2 = co2_captured * harvests_per_year
        
        # STEP 3: Calculate carbon credits
        # 1 credit = 1000 kg CO₂
        carbon_credits = annual_co2 / 1000
        
        # STEP 4: Calculate tree equivalent (for farmer understanding)
        # 1 tree captures ~22.5 kg CO₂ per year
        trees_equivalent = annual_co2 / 22.5
        
        return {
            "source": "Chlorella Microalgae",
            "biomass_kg": biomass_kg,
            "harvest_interval_days": days_between_harvest,
            "co2_captured_this_harvest_kg": round(co2_captured, 2),
            "annual_co2_captured_kg": round(annual_co2, 2),
            "carbon_credits": round(carbon_credits, 2),
            "trees_equivalent": round(trees_equivalent, 0),
            "message": f"🌊 One harvest captures as much CO₂ as {round(trees_equivalent/10)} trees in one year!"
        }
    
    def calculate_from_pond(self, area_sqm, depth_m=0.3, density_g_per_l=2.0):
        """
        Calculate potential credits based on pond size
        
        Formula:
        Volume (L) = Area (m²) × Depth (m) × 1000
        Biomass (kg) = Volume × Density (g/L) ÷ 1000
        """
        
        # Calculate pond volume in liters
        volume_liters = area_sqm * depth_m * 1000
        
        # Calculate total biomass in pond
        total_biomass_kg = (volume_liters * density_g_per_l) / 1000
        
        # Farmers harvest ~30% of total biomass at a time
        harvest_biomass = total_biomass_kg * 0.3
        
        return self.calculate_credits(harvest_biomass)