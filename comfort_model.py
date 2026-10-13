import joblib
import pandas as pd
import os


class ComfortModel:
    def __init__(self, model_file="iaq_model.pkl"):
        if os.path.exists(model_file):
            self.agent = joblib.load(model_file)
        else:
            self.agent = None
            print(f"[WARNING] Modelul {model_file} lipseste. Ruleaza train_model.py")

    def analyze_environment(self, sensor_data):
        if not self.agent:
            return "UNKNOWN", "Model indisponibil"

        features = ['temperature', 'humidity', 'co2', 'oxygen', 'tvoc', 'pm2_5']
        input_row = pd.DataFrame([[
            sensor_data.get('temperature', 22),
            sensor_data.get('humidity', 45),
            sensor_data.get('co2', 400),
            sensor_data.get('oxygen', 20.9),
            sensor_data.get('tvoc', 10),
            sensor_data.get('pm2_5', 1)
        ]], columns=features)

        prediction = self.agent.predict(input_row)[0]

        if prediction == 1:
            if sensor_data.get('oxygen') < 19.5: return "MAX_VENT", "Oxigen scăzut"
            if sensor_data.get('co2') > 1000: return "VENTILATE", "CO2 ridicat"
            if sensor_data.get('pm2_5') > 35: return "PURIFY", "Praf/PM2.5 ridicat"
            if sensor_data.get('tvoc') > 500: return "MAX_VENT", "TVOC ridicat"
            if sensor_data.get('temperature') < 20: return "HEATING", "Frig"
            if sensor_data.get('temperature') > 25: return "COOLING", "Cald"

            return "ADJUSTING", "Anomalie ambientală detectată"

        return "IDLE", "Condiții optime"