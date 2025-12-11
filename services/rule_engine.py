from typing import Tuple, Dict, Any, List
from utils.file_utils import read_json
from models.schemas import RulesModel
import json

RULES_PATH = "database/current_rules.json"

def load_rules() -> RulesModel:
    data = read_json(RULES_PATH)
    if not data:
        default = {
            "version": "1.0",
            "allowed_fields": ["name", "employee_no"],
            "constraints": {
                "name_max_length": 50,
                "employee_no_length": 6
            }
        }
        return RulesModel.parse_obj(default)
    return RulesModel.parse_obj(data)

def validate_document(doc: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Returns (is_valid, details)
    details includes: violations list, unexpected_fields list, used_rule_version
    """
    rules = load_rules()
    violations: List[str] = []
    unexpected_fields: List[str] = []

    for k in doc.keys():
        if k not in rules.allowed_fields:
            unexpected_fields.append(k)

    name = doc.get("name")
    if name is not None and rules.constraints.name_max_length:
        if len(str(name)) > rules.constraints.name_max_length:
            violations.append(f"name length > {rules.constraints.name_max_length}")

    emp = doc.get("employee_no")
    if emp is not None and rules.constraints.employee_no_length:
        if len(str(emp)) != rules.constraints.employee_no_length:
            violations.append(f"employee_no length != {rules.constraints.employee_no_length}")

    is_valid = (len(violations) == 0 and len(unexpected_fields) == 0)
    details = {
        "violations": violations,
        "unexpected_fields": unexpected_fields,
        "used_rule_version": rules.version
    }

    return is_valid, details

def propose_new_rules_for_unexpected_fields(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a proposed rules object that includes any new fields detected
    (keeps other constraints same as current rules)
    """
    current = load_rules()
    new_allowed = list(current.allowed_fields)
    for k in doc.keys():
        if k not in new_allowed:
            new_allowed.append(k)

    proposed = {
        "version": current.version + ".1", 
        "allowed_fields": new_allowed,
        "constraints": current.constraints.dict(),
        "metadata": {
            "proposed_by": "system",
            "note": "Automatically proposed to include unexpected fields"
        }
    }
    return proposed
