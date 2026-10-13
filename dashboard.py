import streamlit as st
import json
import os
import time

st.set_page_config(page_title="IAQ Monitoring", layout="wide")

def fetch_live_data():
    if os.path.exists("live_data.json"):
        try:
            with open("live_data.json", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = fetch_live_data()

LIMITS = {
    "t_range": (20.0, 25.0),
    "h_range": (30.0, 60.0),
    "co2_max": 1000,
    "o2_min": 19.8,
    "pm25_max": 25.0,
    "tvoc_max": 500,
    "sound_max": 60.0
}

st.title("🏙️ Indoor Air Quality Monitoring and Control System in Smart Buildings")

st.divider()
status = data.get('status', 'Așteptare date...')
hvac_mode = data.get('hvac', 'OFF')

st.header("😌 Comfort")
c1, c2, c3, c4 = st.columns(4)

temp = data.get('temperature', 0)
t_lbl = "OK" if LIMITS["t_range"][0] <= temp <= LIMITS["t_range"][1] else "Adjusting"
c1.metric("Temperature", f"{temp} °C", delta=t_lbl, delta_color="normal" if t_lbl == "OK" else "inverse")

hum = data.get('humidity', 0)
h_lbl = "OK" if LIMITS["h_range"][0] <= hum <= LIMITS["h_range"][1] else "Adjusting"
c2.metric("Humidity", f"{hum} %", delta=h_lbl, delta_color="normal" if h_lbl == "OK" else "inverse")

c3.metric("Pressure", f"{data.get('pressure', 0)} hPa", delta="Stable")

snd = data.get('sound', 0)
s_lbl = "Quiet" if snd <= LIMITS["sound_max"] else "Noisy"
c4.metric("Sound", f"{snd} dB", delta=s_lbl, delta_color="normal" if s_lbl == "Quiet" else "inverse")

st.divider()

st.header("🌬️ Air Quality")
a1, a2, a3, a4 = st.columns(4)

o2 = data.get('oxygen', 0)
o2_lbl = "Safe" if o2 >= LIMITS["o2_min"] else "LOW"
a1.metric("Oxygen (O2)", f"{o2} %", delta=o2_lbl, delta_color="normal" if o2_lbl == "Safe" else "inverse")

co2 = data.get('co2', 0)
co2_lbl = "Fresh" if co2 <= LIMITS["co2_max"] else "Stale"
a2.metric("Carbon Dioxide (CO2)", f"{int(co2)} ppm", delta=co2_lbl, delta_color="normal" if co2_lbl == "Fresh" else "inverse")

tvoc = data.get('tvoc', 0)
tvoc_lbl = "Clean" if tvoc <= LIMITS["tvoc_max"] else "High"
a3.metric("Total Volatile Organic Compounds (TVOC)", f"{tvoc} ppb", delta=tvoc_lbl, delta_color="normal" if tvoc_lbl == "Clean" else "inverse")

pm = data.get('pm2_5', 0)
pm_lbl = "Pure" if pm <= LIMITS["pm25_max"] else "Dusty"
a4.metric("Particulate Matter (PM2.5)", f"{pm} µg/m³", delta=pm_lbl, delta_color="normal" if pm_lbl == "Pure" else "inverse")

st.divider()
st.caption(f"🕒 Measure time: {data.get('measuretime', 'N/A')}")

if "ML:" in status and "optime" not in status.lower():
    st.error(f"**DECISION:** {status} | **Sistem HVAC:** {hvac_mode}")
else:
    st.success(f"**DECISION:** {status}")

time.sleep(1)
st.rerun()