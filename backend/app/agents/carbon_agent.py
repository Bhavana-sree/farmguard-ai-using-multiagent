class CarbonAgent:
    def calculate_carbon(self, tree_count, avg_height=10):
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