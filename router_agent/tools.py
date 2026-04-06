"""ADK tools used by the router agent."""

from __future__ import annotations

import csv
import io
import re

import google.genai.types as types
from google.adk.tools import ToolContext
from sqlalchemy import text

from router_agent.db import get_session

FORBIDDEN_SQL_KEYWORDS = (
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "replace",
    "rename",
    "grant",
    "revoke",
    "lock",
    "unlock",
    "commit",
    "rollback",
    "set",
    "use",
    "call",
    "execute",
    "exec",
)
ALLOWED_QUERY_PREFIXES = ("select", "show", "describe", "desc", "explain", "with")
INLINE_ROWS_LIMIT = 5


async def execute_router_sql(sql_query: str, tool_context: ToolContext) -> dict:
    """Execute LLM-generated read-only SQL and return rows."""
    normalized = _normalize_sql(sql_query)
    error = _validate_read_only_sql(normalized)
    if error:
        return {"ok": False, "error": error}

    with get_session() as session:
        result = session.execute(text(normalized))
        if not result.returns_rows:
            return {"ok": True, "sql_received": normalized, "rows": []}
        rows = [dict(row) for row in result.mappings().all()]

    response = {
        "ok": True,
        "sql_received": normalized,
        "rows": rows[:INLINE_ROWS_LIMIT],
        "total_rows": len(rows),
    }
    if len(rows) <= INLINE_ROWS_LIMIT:
        return response

    csv_bytes = _rows_to_csv_bytes(rows)
    artifact = types.Part.from_bytes(data=csv_bytes, mime_type="text/csv")
    filename = "router-query-results.csv"
    try:
        version = await tool_context.save_artifact(filename=filename, artifact=artifact)
        response["artifact"] = {"filename": filename, "version": version, "mime_type": "text/csv"}
    except Exception:
        response["artifact"] = {"error": "Artifact could not be saved."}
    return response


def _normalize_sql(sql_query: str) -> str:
    """Normalize SQL query whitespace and semicolon."""
    compact = " ".join(sql_query.strip().split())
    return compact.rstrip(";")


def _validate_read_only_sql(sql_query: str) -> str | None:
    """Return an error message when SQL is not safe read-only."""
    if not sql_query:
        return "SQL query is empty."
    lowered = sql_query.lower().strip()
    if not lowered.startswith(ALLOWED_QUERY_PREFIXES):
        return "Only read-only SQL is allowed (SELECT, SHOW, DESCRIBE, EXPLAIN, WITH)."
    if ";" in lowered:
        return "Multiple SQL statements are not allowed."
    if "--" in lowered or "/*" in lowered or "*/" in lowered:
        return "SQL comments are not allowed."
    for keyword in FORBIDDEN_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lowered):
            return f"Forbidden SQL keyword detected: {keyword}"
    return None


def _rows_to_csv_bytes(rows: list[dict]) -> bytes:
    """Convert query result rows to UTF-8 CSV bytes."""
    output = io.StringIO()
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")

