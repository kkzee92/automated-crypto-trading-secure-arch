"""Audit logging for trading actions. Secrets are never logged."""
import logging
import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = Path("audit.log")

logger = logging.getLogger("audit")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(AUDIT_LOG_PATH)
handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
logger.addHandler(handler)

def log_action(action: str, details: dict):
    """Log an action with redacted sensitive fields."""
    safe_details = {k: ("***REDACTED***" if "key" in k.lower() or "secret" in k.lower() else v)
                    for k, v in details.items()}
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": safe_details
    }
    logger.info(json.dumps(entry))
    print(f"[AUDIT] {action}: {safe_details}")
