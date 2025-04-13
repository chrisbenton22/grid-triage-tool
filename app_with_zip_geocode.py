
import streamlit as st
import random
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Grid Triage Tool with Map", layout="wide")

st.title("Grid Triage Tool")
st.write("Quick pre-screening tool for energy project interconnection feasibility with interactive grid stress map.")

# Inputs
project_type = st.selectbox("Select Project Type", ["Solar", "Wind", "Battery Storage", "Hybrid"])
location = st.text_input("Enter Project Location (ZIP Code or Region)")
capacity = st.number_input("Expected Capacity (kW)", min_value=1, step=1)

# Session state for persistence
if "feasibility_checked" not in st.session_state:
    st.session_state.feasibility_checked = False

if st.button("Check Feasibility"):
    st.session_state.feasibility_checked = True

if st.session_state.feasibility_checked:
    queue_time = random.randint(6, 36)
    stress_zone = random.choice(["Low", "Medium", "High"])

    if stress_zone == "Low":
        score = "Green - Likely Feasible"
        color = "green"
    elif stress_zone == "Medium":
        score = "Yellow - Moderate Risk"
        color = "orange"
    else:
        score = "Red - Likely Delayed"
        color = "red"

    st.subheader("Analysis Results")
    st.write(f"**Estimated Queue Time:** {queue_time} months")
    st.write(f"**Regional Grid Stress:** {stress_zone}")
    st.write(f"**Preliminary Feasibility Score:** {score}")

    # Geocode ZIP code to coordinates
    geolocator = Nominatim(user_agent="grid_triage_tool")
    try:
        location_obj = geolocator.geocode(location)
        lat, lon = location_obj.latitude, location_obj.longitude
    except:
        lat, lon = 35.486, -80.860  # fallback to Cornelius, NC
        st.warning("Could not geocode the location. Using default coordinates.")

    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker(
        [lat, lon],
        tooltip="Project Location",
        popup=f"Stress: {stress_zone}",
        icon=folium.Icon(color=color)
    ).add_to(m)

    st.subheader("Regional Stress Map")
    st_folium(m, width=700, height=500)
