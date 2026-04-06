---
name: network-sql-skill
description: Rules for converting Cisco router questions into database lookups.
---

# Network SQL Skill

Use this skill for questions about Cisco routers, interfaces, status, CPU, memory, uptime, serials, and configuration.

## Steps

1. Detect the main network element in the prompt:
   - router name
   - management IP
   - site
   - model
   - metric (cpu, memory, uptime, config, serial)
2. Convert the user prompt to a SQL query string.
3. Table columns:
    - id	- router id from db
    - name - router name or network element nane, etc
    - site - the localtion/city/region where the router is integrated 
    - management_ip	- O&M or management IP address
    - model	- router model
    - os_version	- operating system version
    - status - whether the router is up or down
    - uptime_days	- uptime in dau
    - cpu_percent	- COU
    - memory_percent	- memory 
    - serial_number	- serial number of the router
    - config_text - config in text format

    Table name is always routers

4. Call `execute_router_sql` with that SQL string.
5. Read tool output and answer in concise English.
6. If no rows are returned, explain that no matching router data was found.

## SQL Format

- Read-only SQL only.
- Allowed query families:
  - `SELECT ...`
  - `SHOW ...`
  - `DESCRIBE ...` or `DESC ...`
  - `EXPLAIN ...`
  - `WITH ... SELECT ...`

## Constraints

- Do not invent router data.
- Use only tool output for facts.
- Keep the final answer short and clear.
- Never generate write or destructive SQL.
- Never generate multiple SQL statements.
- Do not use SQL comments.

