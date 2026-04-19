import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Solar Battery Optimizer", layout="wide")

st.title("🔋 Solar Battery Storage Optimization for Grid Integrated Solar Plants")

st.sidebar.header("Input Parameters")

battery_capacity = st.sidebar.slider("Battery Capacity (kWh)", 50, 500, 200)
initial_soc = st.sidebar.slider("Initial Battery Charge (%)", 10, 100, 50)
tariff = st.sidebar.slider("Grid Tariff ($/kWh)", 1, 20, 8)

hours = np.arange(24)

solar = np.array([0,0,0,0,5,15,30,45,60,75,85,95,100,95,80,60,40,20,10,0,0,0,0,0])
demand = np.array([30,28,26,25,24,30,40,50,55,60,65,70,75,72,68,66,70,80,85,78,65,55,45,35])

soc = initial_soc / 100 * battery_capacity
soc_list = []
grid_use = []
action = []
cost = 0

for i in range(24):
    net = solar[i] - demand[i]

    if net > 0:
        charge = min(net, battery_capacity - soc)
        soc += charge
        grid = 0
        act = "Charging"
    else:
        needed = abs(net)
        discharge = min(needed, soc)
        soc -= discharge
        grid = needed - discharge
        act = "Discharging" if discharge > 0 else "Grid Supply"

    cost += grid * tariff
    soc_list.append(soc)
    grid_use.append(grid)
    action.append(act)

df = pd.DataFrame({
    "Hour": hours,
    "Solar": solar,
    "Demand": demand,
    "Battery_SOC": soc_list,
    "Grid_Use": grid_use,
    "Action": action
})

st.subheader("Simulation Results")
st.dataframe(df)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.plot(df["Hour"], df["Solar"], label="Solar")
    ax.plot(df["Hour"], df["Demand"], label="Demand")
    ax.set_title("Solar vs Demand")
    ax.legend()
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Hour"], df["Battery_SOC"])
    ax2.set_title("Battery State of Charge")
    st.pyplot(fig2)

st.metric("Total Grid Cost", f"${cost:.2f}")
st.metric("Grid Energy Used", f"{sum(grid_use):.2f} kWh")

st.success("Optimization Goal: Maximize Solar Use, Minimize Grid Dependency, Protect Battery")
