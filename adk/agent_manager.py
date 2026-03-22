from tools import get_tools
from llm_reasoning import create_llm_agent

trace_log = []

def run_agent(user_input):

    from agents.monitoring_agent import MonitoringAgent
    from agents.demand_agent import DemandAgent
    from agents.bayesian_agent import BayesianAgent
    from environment.parking_environment import ParkingEnvironment

    environment = ParkingEnvironment()
    monitoring_agent = MonitoringAgent()
    demand_agent = DemandAgent()
    bayesian_agent = BayesianAgent()

    tools = get_tools(monitoring_agent, demand_agent, bayesian_agent, environment)

    agent = create_llm_agent(tools)

    result = agent.run(user_input)

    trace_log.append(result)

    return result


def get_trace():
    return trace_log