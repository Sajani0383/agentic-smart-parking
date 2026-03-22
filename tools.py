from langchain.tools import Tool
import streamlit as st

def get_tools(monitoring_agent, demand_agent, bayesian_agent, policy_agent, environment):

    def get_parking_state(_input=None):
        state = monitoring_agent.observe(environment)

        st.session_state.state = state
        st.session_state.trace.append("Fetched parking state")

        return f"""Parking Status:
{format_state(state)}"""

    def predict_demand(_input=None):
        state = monitoring_agent.observe(environment)
        demand = demand_agent.predict(state)

        st.session_state.trace.append("Predicted demand")
        st.session_state.artifacts["demand"] = demand

        return f"""Predicted Demand:
{demand}"""

    def compute_congestion(_input=None):
        state = monitoring_agent.observe(environment)
        congestion = bayesian_agent.compute_probability(state)

        st.session_state.events.append("Computed congestion")
        st.session_state.artifacts["congestion"] = congestion

        return f"""Congestion Probability:
{congestion}"""

    def simulate_step(_input=None):
        state = monitoring_agent.observe(environment)
        demand = demand_agent.predict(state)

        zone, mode = policy_agent.choose_zone(demand)
        reward = environment.step(zone)

        st.session_state.events.append(f"Simulated: {zone}")
        st.session_state.trace.append("Simulation step executed")

        st.session_state.state = monitoring_agent.observe(environment)

        return f"""Simulation Result:
Zone: {zone}
Mode: {mode}
Reward: {reward}"""

    def format_state(state):
        text = ""
        for zone, data in state.items():
            text += f"{zone}: {data['free_slots']} free, {data['entry_count']} entry, {data['exit_count']} exit\n"
        return text

    tools = [
        Tool(
            name="Parking State",
            func=get_parking_state,
            description="Use this to get current parking status"
        ),
        Tool(
            name="Demand Prediction",
            func=predict_demand,
            description="Use this to predict parking demand"
        ),
        Tool(
            name="Congestion Probability",
            func=compute_congestion,
            description="Use this to compute congestion"
        ),
        Tool(
            name="Simulate Parking",
            func=simulate_step,
            description="Use this to simulate parking changes"
        )
    ]

    return tools