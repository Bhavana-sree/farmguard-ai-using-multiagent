import random


class IoTAgent:
    def collect_sensor_data(self, latitude: float, longitude: float):
        soil_moisture = round(random.uniform(25, 55), 2)
        temperature_c = round(random.uniform(24, 36), 2)
        humidity_percent = round(random.uniform(45, 85), 2)
        soil_ph = round(random.uniform(5.8, 7.5), 2)
        light_intensity_lux = round(random.uniform(20000, 70000), 2)

        if soil_moisture < 30:
            irrigation_status = "Low moisture - irrigation recommended"
        elif soil_moisture > 50:
            irrigation_status = "High moisture - no irrigation needed"
        else:
            irrigation_status = "Moisture normal"

        if temperature_c > 34:
            crop_stress = "High temperature stress possible"
        elif humidity_percent < 50:
            crop_stress = "Low humidity stress possible"
        else:
            crop_stress = "Normal conditions"

        return {
            "latitude": latitude,
            "longitude": longitude,
            "soil_moisture_percent": soil_moisture,
            "temperature_c": temperature_c,
            "humidity_percent": humidity_percent,
            "soil_ph": soil_ph,
            "light_intensity_lux": light_intensity_lux,
            "irrigation_status": irrigation_status,
            "crop_stress": crop_stress
        }