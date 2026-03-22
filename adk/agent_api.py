from fastapi import FastAPI
from adk.agent_manager import run_agent, get_trace

app = FastAPI()


@app.post("/run")
def run(query: dict):
    result = run_agent(query["input"])
    return {"response": result}


@app.get("/trace")
def trace():
    return {"trace": get_trace()}