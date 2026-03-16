from app.agents.vision_agent import VisionAgent
from app.agents.carbon_agent import CarbonAgent
from app.agents.validation_agent import ValidationAgent
from app.agents.market_agent import MarketAgent
from app.agents.blockchain_agent import BlockchainAgent
from app.agents.iot_agent import IoTAgent


class OrchestratorAgent:
    def __init__(self, validation_agent: ValidationAgent):
        self.vision_agent = VisionAgent()
        self.carbon_agent = CarbonAgent()
        self.iot_agent = IoTAgent()
        self.validation_agent = validation_agent
        self.market_agent = MarketAgent()
        self.blockchain_agent = BlockchainAgent()

    def run_pipeline(self, latitude: float, longitude: float):
        vision_result = self.vision_agent.analyze_farm(latitude, longitude)
        tree_count = vision_result["estimated_trees"]

        carbon_result = self.carbon_agent.calculate_carbon(tree_count)
        co2_value = carbon_result["co2_kg"]
        credits = carbon_result["carbon_credits"]

        iot_result = self.iot_agent.collect_sensor_data(latitude, longitude)

        validation_result = self.validation_agent.validate_data(
            tree_count,
            co2_value,
            iot_result
        )

        blockchain_result = self.blockchain_agent.create_block({
            "latitude": latitude,
            "longitude": longitude,
            "trees": tree_count,
            "co2_removed": co2_value,
            "credits": credits,
            "iot_summary": {
                "soil_moisture_percent": iot_result["soil_moisture_percent"],
                "temperature_c": iot_result["temperature_c"],
                "humidity_percent": iot_result["humidity_percent"]
            },
            "validation_status": validation_result["status"]
        })

        market_result = self.market_agent.estimate_market_value(credits)

        return {
            "vision_analysis": vision_result,
            "carbon_analysis": carbon_result,
            "iot_analysis": iot_result,
            "validation_result": validation_result,
            "blockchain_record": blockchain_result,
            "market_analysis": market_result
        }