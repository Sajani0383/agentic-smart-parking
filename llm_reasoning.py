from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def create_llm_agent(tools):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )

    from langchain.agents import initialize_agent

    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": """
You are a smart parking AI assistant.

IMPORTANT:
- Use tools ONLY for parking data (state, demand, simulation)
- For general questions (why parking, benefits, etc), answer directly
- Always give clear, human-friendly answers
"""
        }
    )

    return agent