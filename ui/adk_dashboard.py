import streamlit as st
import sys
import os
import time
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from environment.parking_environment import ParkingEnvironment
from agents.monitoring_agent import MonitoringAgent
from agents.demand_agent import DemandAgent
from agents.bayesian_agent import BayesianAgent
from agents.policy_agent import PolicyAgent

from tools import get_tools
from llm_reasoning import create_llm_agent

# ZONES
zones = ['Mall', 'Hospital', 'Office', 'Residential', 'Commercial']

# INIT
environment = ParkingEnvironment(zones)
monitor = MonitoringAgent()
demand_agent = DemandAgent()
bayesian_agent = BayesianAgent()
policy_agent = PolicyAgent(zones)

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "trace" not in st.session_state:
    st.session_state.trace = []

if "events" not in st.session_state:
    st.session_state.events = []

if "state" not in st.session_state:
    st.session_state.state = {}

if "artifacts" not in st.session_state:
    st.session_state.artifacts = {}

if "auto_run" not in st.session_state:
    st.session_state.auto_run = False

if "agent" not in st.session_state:
    tools = get_tools(monitor, demand_agent, bayesian_agent, policy_agent, environment)
    st.session_state.agent = create_llm_agent(tools)

st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 3])

# ================= LEFT PANEL =================
with col1:
    st.title("⚙️ Controls")

    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.session_state.trace = []
        st.session_state.events = []
        st.session_state.state = {}
        st.session_state.artifacts = {}

    if st.button("▶ Start Auto Simulation"):
        st.session_state.auto_run = True

    if st.button("⏹ Stop Auto Simulation"):
        st.session_state.auto_run = False

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Trace", "Events", "State", "Artifacts"])

    # TRACE
    with tab1:
        for t in st.session_state.trace:
            st.success(t)

    # EVENTS
    with tab2:
        for e in st.session_state.events:
            st.info(e)

    # STATE
    with tab3:
        state = st.session_state.state

        st.write("DEBUG STATE:", state)

        if isinstance(state, dict):
            for zone, data in state.items():
                st.write(f"**{zone}**")
                st.write(f"Free Slots: {data.get('free_slots')}")
                st.write(f"Entry: {data.get('entry_count')}")
                st.write(f"Exit: {data.get('exit_count')}")
                st.markdown("---")

            df = pd.DataFrame(state).T
            if "free_slots" in df.columns:
                st.bar_chart(df["free_slots"])
        else:
            st.write("No state available")

    # ARTIFACTS
    with tab4:
        st.write(st.session_state.artifacts)

# ================= RIGHT PANEL =================
with col2:
    st.title("🚗 Agentic AI Smart Parking Assistant")
    st.markdown("### 🧠 Monitoring → Prediction → Decision → Optimization")

    # CHAT HISTORY
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # INPUT
    user_input = st.chat_input("Ask anything about parking...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):

                    # ✅ SMART ROUTING (FINAL FIX)
                    if any(word in user_input.lower() for word in [
                        "state", "parking", "slots", "simulate", "demand", "congestion"
                    ]):
                        response = st.session_state.agent.run(user_input)
                    else:
                        llm = create_llm_agent([])
                        response = llm.invoke(user_input).content

            except Exception as e:
                response = f"Error: {str(e)}"

            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# ================= AUTO SIMULATION =================
if st.session_state.auto_run:
    try:
        for _ in range(2):
            st.session_state.agent.run("simulate parking")
            time.sleep(1)
    except:
        pass

    st.rerun()