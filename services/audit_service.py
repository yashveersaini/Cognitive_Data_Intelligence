from utils.file_utils import read_json, write_json, timestamp
from typing import Any, Dict
import os

AUDIT_RULES_PATH = "database/audit.json"
VALIDATION_LOGS_PATH = "database/validation_logs.json"
CURRENT_RULES_PATH = "database/current_rules.json"

def _append_to_array(path: str, entry: Dict[str, Any]) -> None:
    arr = read_json(path) or []
    arr.append(entry)
    write_json(path, arr)

def audit_rule_change(old_rules: Dict[str, Any], new_rules: Dict[str, Any], admin: str = "unknown", reason: str = "") -> None:
    entry = {
        "timestamp": timestamp(),
        "admin": admin,
        "reason": reason,
        "old_rules": old_rules,
        "new_rules": new_rules
    }
    _append_to_array(AUDIT_RULES_PATH, entry)

def log_validation(document: Dict[str, Any], result: Dict[str, Any]) -> None:
    entry = {
        "timestamp": timestamp(),
        "document": document,
        "result": result
    }
    _append_to_array(VALIDATION_LOGS_PATH, entry)

def read_audit_rules() -> Any:
    return read_json(AUDIT_RULES_PATH) or []

def read_validation_logs() -> Any:
    return read_json(VALIDATION_LOGS_PATH) or []
