"""Seed logic for router data."""

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from router_agent.models import Router


def seed_routers_if_empty(session: Session, seed_path: Path) -> None:
    """Insert router rows from JSON when table is empty."""
    existing = session.scalar(select(Router.id).limit(1))
    if existing is not None:
        return

    payload = json.loads(seed_path.read_text(encoding="utf-8"))
    routers = [
        Router(
            name=item["name"],
            site=item["site"],
            management_ip=item["management_ip"],
            model=item["model"],
            os_version=item["os_version"],
            status=item["status"],
            uptime_days=item["uptime_days"],
            cpu_percent=item["cpu_percent"],
            memory_percent=item["memory_percent"],
            serial_number=item["serial_number"],
            config_text=item["config_text"],
        )
        for item in payload
    ]
    session.add_all(routers)
    session.commit()

