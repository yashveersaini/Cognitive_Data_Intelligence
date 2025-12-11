from fastapi import FastAPI, HTTPException
from models.schemas import DocumentInput, RuleUpdateRequest
from services.rule_engine import load_rules
from services.rule_update_service import read_current_rules
from services.audit_service import read_audit_rules, read_validation_logs
import json
from pathlib import Path
from datetime import datetime


app = FastAPI(title="Cognitive Data Intelligence & Autonomous Workflow System", version="0.1")
RULES_FILE = Path("database/current_rules.json")

def load_rules():
    with open(RULES_FILE, "r") as f:
        return json.load(f)
    
@app.get("/")
def home():
    return {"message":"Cognitive Data Intelligence & Autonomous Workflow System is running", 
            "Run locally":"http://127.0.0.1:8000/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

RULES_PATH = Path("database/current_rules.json")


def load_rules():
    with RULES_PATH.open("r") as f:
        return json.load(f)

@app.post("/validate")
def validate_endpoint(payload: DocumentInput):
    payload_dict = payload.model_dump()

    rules = load_rules()
    allowed_fields = rules.get("allowed_fields", [])
    constraints = rules.get("constraints", {})
    version = rules.get("version", "unknown")

    violations = []
    unexpected = []

    for field in payload_dict.keys():
        if field not in allowed_fields:
            unexpected.append(field)


    if "name_max_length" in constraints:
        if "name" in payload_dict:
            if len(payload_dict["name"]) > constraints["name_max_length"]:
                violations.append(
                    f"name length exceeds max limit ({constraints['name_max_length']})"
                )

    if "employee_no_length" in constraints:
        if "employee_no" in payload_dict:
            if len(payload_dict["employee_no"]) != constraints["employee_no_length"]:
                violations.append(
                    f"employee_no length must be {constraints['employee_no_length']}"
                )

    for key, value in constraints.items():
        if key.startswith("min_"):
            field = key.replace("min_", "")
            if field in payload_dict:
                if payload_dict[field] < value:
                    violations.append(f"{field} is below minimum allowed value ({value})")

        if key.startswith("max_"):
            field = key.replace("max_", "")
            if field in payload_dict:
                if payload_dict[field] > value:
                    violations.append(f"{field} is above maximum allowed value ({value})")

    if violations or unexpected:
        return {
            "status": "invalid",
            "message": "Validation failed due to dynamic rules",
            "details": {
                "violations": violations,
                "unexpected_fields": unexpected,
                "used_rule_version": version
            }
        }

    return {
        "status": "successfully received",
        "used_rule_version": version
    }


@app.get("/get_rules")
def get_rules():
    rules = read_current_rules()
    return {"current_rules": rules}

@app.post("/update_rules")
def update_rules(payload: RuleUpdateRequest):
    new_rules_data = payload.new_rules.model_dump()

    with open("database/current_rules.json", "r") as f:
        old_rules = json.load(f)

    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "old_rules": old_rules,
        "updated_by": payload.admin,
        "reason": payload.reason
    }

    audit_path = Path("database/audit.json")
    if audit_path.exists():
        audits = json.loads(audit_path.read_text())
    else:
        audits = []

    audits.append(audit_entry)
    audit_path.write_text(json.dumps(audits, indent=2))

    with open("database/current_rules.json", "w") as f:
        json.dump(new_rules_data, f, indent=2)

    return {"status": "rules_updated", "message": "Rules saved successfully"}

@app.get("/audit_log")
def audit_log():
    return {"audit": read_audit_rules()}

@app.get("/validation_logs")
def validation_logs():
    return {"validation_logs": read_validation_logs()}
