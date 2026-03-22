import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

st.set_page_config(page_title="Smart Parking AI", layout="wide")

st.title("🚗 Smart Parking Agentic AI Dashboard")

# -----------------------------
# LOAD DATASET
# -----------------------------

dataset = pd.read_csv("dataset/parking_dataset.csv")

# create free slots column
dataset["free_slots"] = 100 - dataset["occupied_slots"]

zones = dataset["zone"].dropna().unique().tolist()

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------

st.sidebar.header("Simulation Controls")

vehicle_count = st.sidebar.slider("Vehicles", 10, 100, 40)
speed = st.sidebar.slider("Simulation Speed", 0.1, 1.0, 0.4)

start = st.sidebar.button("Start Simulation")

# -----------------------------
# SYSTEM METRICS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Parking Zones", len(zones))

with col2:
    st.metric("Vehicles", vehicle_count)

with col3:
    st.metric("AI Agent", "Active")

st.divider()

# -----------------------------
# PARKING AVAILABILITY GRAPH
# -----------------------------

st.subheader("Parking Availability")

zone_data = dataset.groupby("zone")["free_slots"].mean().reset_index()

fig = px.bar(
    zone_data,
    x="zone",
    y="free_slots",
    color="zone",
    title="Average Free Parking Slots"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SIMULATION
# -----------------------------

if start:

    st.divider()
    st.subheader("Live AI Decision")

    decision_box = st.empty()
    reward_box = st.empty()

    decision_history = []
    rewards = []

    for step in range(20):

        chosen_zone = random.choice(zones)

        reason = random.choice([
            "Low congestion",
            "High slot availability",
            "Balanced distribution"
        ])

        confidence = round(random.uniform(0.75, 0.95), 2)

        decision_box.markdown(f"""
### Step {step}

**Chosen Zone:** {chosen_zone}  
**Reason:** {reason}  
**Confidence:** {confidence}
""")

        reward = random.randint(-1, 3)

        rewards.append(reward)

        reward_box.metric("Latest Reward", reward)

        decision_history.append({
            "Step": step,
            "Zone": chosen_zone,
            "Reason": reason,
            "Confidence": confidence,
            "Reward": reward
        })

        time.sleep(speed)

    # -----------------------------
    # REWARD TREND GRAPH
    # -----------------------------

    st.divider()
    st.subheader("Reinforcement Learning Reward")

    reward_df = pd.DataFrame({
        "Step": range(len(rewards)),
        "Reward": rewards
    })

    fig2 = px.line(
        reward_df,
        x="Step",
        y="Reward",
        title="Reward Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # AGENT DECISION TABLE
    # -----------------------------

    st.divider()
    st.subheader("Agent Decision Summary")

    decision_df = pd.DataFrame(decision_history)

    st.dataframe(decision_df, use_container_width=True)

# -----------------------------
# ENTRY VS EXIT GRAPH
# -----------------------------

st.divider()
st.subheader("Vehicle Entry vs Exit")

entry_exit = dataset[["entry_count", "exit_count"]]

fig3 = px.line(
    entry_exit,
    title="Entry vs Exit Flow"
)

st.plotly_chart(fig3, use_container_width=True)