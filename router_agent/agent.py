"""Root ADK agent definition."""

from pathlib import Path
from router_agent.config import load_settings

from google.adk import Agent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset


from router_agent.db import initialize_database
from router_agent.tools import execute_router_sql

settings = load_settings()

SKILL_PATH = Path(__file__).resolve().parent / "skills" / "network-sql-skill"
network_skill = load_skill_from_dir(SKILL_PATH)
network_skill_toolset = skill_toolset.SkillToolset(skills=[network_skill])

initialize_database()

root_agent = Agent(
    model=settings.adk_model,
    name="cisco_router_agent",
    description="Answers user questions about Cisco router inventory.",
    instruction=(
        "You are a Cisco router assistant. "
        "For inventory questions, first generate a read-only SQL query from the user prompt. "
        "Use SELECT, SHOW, DESCRIBE, EXPLAIN, or WITH queries only. "
        "Never generate write or destructive SQL commands. "
        "Then call execute_router_sql with that SQL string. "
        "Summarize results clearly in user language."
    ),
    tools=[execute_router_sql, network_skill_toolset],
)

