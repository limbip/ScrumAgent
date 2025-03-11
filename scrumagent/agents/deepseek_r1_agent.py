import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

load_dotenv()

"""
Open Source Reasoning and Coding Agent
Download models from: https://ollama.com/library/deepseek-r1
Check what size fits in your gpu
Very slow ... but very powerful
"""
ACTIVATE_DEEPSEEK = os.getenv("ACTIVATE_DEEPSEEK", "").lower() in ("true", "1", "yes", "on")

if ACTIVATE_DEEPSEEK:
    llm = ChatOllama(model="deepseek-r1:8b")

    llm_agent = create_react_agent(llm, tools=[], state_modifier="Large Language Model for Reasoning and Coding.")
else:
    llm_agent = None
