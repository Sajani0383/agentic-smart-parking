from agents.monitoring_agent import MonitoringAgent
from agents.demand_agent import DemandAgent
from agents.bayesian_agent import BayesianAgent
from agents.policy_agent import PolicyAgent
from agents.reward_agent import RewardAgent

from environment.parking_environment import ParkingEnvironment

from tools import get_tools
from llm_reasoning import create_llm_agent


def run_simulation():

    print("SMART PARKING AGENTIC AI SYSTEM")

    zones = ['Mall', 'Hospital', 'Office', 'Residential', 'Commercial']
    print("Parking Zones:", zones)

    # Initialize environment
    environment = ParkingEnvironment(zones)

    # Initialize agents
    monitoring_agent = MonitoringAgent()
    demand_agent = DemandAgent()
    bayesian_agent = BayesianAgent()
    policy_agent = PolicyAgent(zones)
    reward_agent = RewardAgent()

    # ---------------- LLM (RUN ONLY ONCE) ----------------
    print("\nLLM Strategic Analysis (One-Time)\n")

    tools = get_tools(
        monitoring_agent,
        demand_agent,
        bayesian_agent,
        environment
    )

    llm_agent = create_llm_agent(tools)

    query = "Find the best parking zone based on availability, demand and congestion"

    result = llm_agent.invoke(query)

    best_zone = result["output"]

    print("LLM Recommendation:", best_zone)

    # ---------------- SIMULATION (NO LLM HERE) ----------------
    print("\n--- SIMULATION START ---\n")

    environment.reset()

    for step in range(10):

        print(f"\nSTEP: {step}")

        # Get current state
        state = monitoring_agent.observe(environment)

        # Get demand
        demand = demand_agent.predict(state)

        # Choose action (NO LLM)
        action, mode = policy_agent.choose_zone(demand)

        # Step environment
        state, reward = environment.step(action)

        print("Chosen Zone:", action)
        print("Mode:", mode)
        print("Reward:", reward)

    print("\n--- SIMULATION END ---")


if __name__ == "__main__":
    run_simulation()