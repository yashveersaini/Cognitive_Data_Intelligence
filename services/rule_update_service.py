from utils.file_utils import read_json, write_json, timestamp
from services.audit_service import audit_rule_change
from typing import Dict, Any
from models.schemas import RulesModel

CURRENT_RULES_PATH = "database/current_rules.json"

def read_current_rules() -> Dict[str, Any]:
    return read_json(CURRENT_RULES_PATH) or {}

def validate_new_rules_structure(new_rules: Dict[str, Any]) -> bool:
    """
    Basic structural validation: will attempt to parse using RulesModel.
    """
    try:
        RulesModel.parse_obj(new_rules)
        return True
    except Exception as e:
        return False

def apply_new_rules(new_rules: Dict[str, Any], admin: str = "unknown", reason: str = "") -> Dict[str, Any]:
    """
    Archive old rules and write new rules. Returns the applied new rules.
    """
    old = read_current_rules()
    if not validate_new_rules_structure(new_rules):
        raise ValueError("New rules structure invalid")

    nr = dict(new_rules)
    if "version" not in nr or not nr["version"]:
        nr["version"] = (old.get("version", "0.0")) + ".1"
    nr.setdefault("metadata", {})
    nr["metadata"]["applied_at"] = timestamp()
    nr["metadata"]["applied_by"] = admin

    audit_rule_change(old_rules=old, new_rules=nr, admin=admin, reason=reason)

    write_json(CURRENT_RULES_PATH, nr)
    return nr
