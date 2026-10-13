import json
import paho.mqtt.client as mqtt
from comfort_model import ComfortModel

engine = ComfortModel()

def handle_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        action, info = engine.analyze_environment(payload)

        payload.update({
            "status": info,
            "hvac": action
        })

        with open("live_data.json", "w") as f:
            json.dump(payload, f)

        print(f"Log [{payload.get('measuretime')}]: {info}")

    except Exception as err:
        print(f"Eroare procesare pachet: {err}")


mqtt_client = mqtt.Client("Main_Controller")
mqtt_client.on_message = handle_message

print("--- Controller activ: Asteptare flux date MQTT ---")
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe("smartbuilding/iaq")
mqtt_client.loop_forever()