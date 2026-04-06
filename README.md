# Cisco Router ADK Agent

Python project with a Google ADK agent that answers Cisco router questions using a text-to-SQL tool and a local MySQL database.

## What It Does

- Receives user prompt.
- Detects network element in prompt.
- Converts prompt to a SQL query.
- Executes query on local MySQL via SQLAlchemy.
- Returns concise answer in ADK dev UI.
- Uses ADK Skills (`SKILL.md`) to guide tool usage.

## Project Structure

- `router_agent/agent.py` - root ADK agent.
- `router_agent/tools.py` - ORM query executor tool.
- `router_agent/db.py` - DB creation and startup initialization.
- `router_agent/models.py` - SQLAlchemy models.
- `router_agent/seed.py` - initial seed loader.
- `router_agent/skills/` - ADK Skills files.
- `data/router_configs.json` - 50 seeded routers.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set values.
4. Ensure local MySQL is running.

## Run

- Start ADK dev UI:
  - `adk web`

In the ADK UI, open the `router_agent` agent and ask questions like:

- `Show CPU for Router-12`
- `What is the config for Router-03?`
- `How many routers are in inventory?`
- `List routers in Cluj`

## Notes

- Tables are created at startup.
- Data is seeded only if `routers` table is empty.

