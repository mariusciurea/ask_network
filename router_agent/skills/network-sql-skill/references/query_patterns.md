# Query Patterns

- "Show CPU for Router-12"
- "What is the config for Router-03?"
- "How many routers do we have?"
- "List routers in Cluj"
- "Show details for 10.10.20.14"
- "Show all config for all routers"

# SQL Examples

- `SELECT name, cpu_percent FROM routers WHERE name = 'Router-12' LIMIT 20`
- `SELECT name, config_text FROM routers WHERE name = 'Router-03' LIMIT 20`
- `SELECT COUNT(*) FROM routers`
- `SELECT name, management_ip, status FROM routers WHERE site = 'Cluj' ORDER BY name ASC LIMIT 20`
- `SHOW TABLES`
- `DESCRIBE routers`

# Forbidden SQL

- `DROP TABLE routers`
- `DELETE FROM routers`
- `UPDATE routers SET status = 'down' WHERE name = 'Router-01'`

