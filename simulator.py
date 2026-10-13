import pandas as pd
import time
import json
import paho.mqtt.client as mqtt


def start_sim():
    df = pd.read_csv("laboratory.csv")
    client = mqtt.Client("iaq_monitoring")

    try:
        client.connect("localhost", 1883)
        print("Simulator pornit: Transmisie in curs...")

        for _, row in df.iterrows():
            payload = row.to_dict()
            client.publish("smartbuilding/iaq", json.dumps(payload))
            print(f"Data Push: {payload.get('measuretime')}")
            time.sleep(1)

    except Exception as e:
        print(f"Conexiune esuata: {e}")


if __name__ == "__main__":
    start_sim()