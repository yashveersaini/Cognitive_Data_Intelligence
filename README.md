# Cognitive Data Intelligence & Autonomous Workflow System

This system provides  intelligently process arbitrary structured data dynamically interpret evolving rules, orchestrate autonomous workflows, support concurrent collaborationusing dynamic rules stored in JSON files (JSON is used as a database). Rules can be updated in real time, with full audit logs and validation history. The architecture is designed for resilience, extensibility, and autonomous workflow support.

------------------------------------------------------------------------

# Features

-   ✔ Dynamic rule-based validation (no static schemas required)
-   ✔ Autonomous rule evolution & audit trails
-   ✔ Validation logs for complete traceability
-   ✔ Detection of new/unknown fields
-   ✔ Hot-swappable JSON rule engine
-   ✔ API-first architecture based on FastAPI
-   ✔ Fault-tolerant, extendable, distributed-safe
-   ✔ *Future:* Email alerts for new rule proposals
-   ✔ *Future:* AI-assisted rule inference & auto-updating

------------------------------------------------------------------------

# 📂 Project Structure

    Cognitive_Data_Intelligence/
    │
    ├── app.py                    
    ├── models/
    │   └── schemas.py
    ├── services/
    │   └── validator.py
    ├── database/
    │   ├── current_rules.json
    │   ├── audit.json
    │   └── validation_logs.json
    └── README.md
    └── requirements.txt

------------------------------------------------------------------------

# 🛠️ Installation & Running Locally

## 1. Clone repo on local system

## 2. Create a virtual environment
 ``` bash
python -m venv .venv
```
## 3. Activate virtual environment
 ``` bash
.venv\Scripts\activate
```

## 3. Install dependencies
``` bash
pip install -r requirements.txt
```

## 4. Ensure JSON files exist for storing the data
`database/audit.json`

``` bash
[]
```

`database/validation_logs.json`

``` bash
[]
```

`database/current_rules.json`

``` bash
{
  "version": "1.0",
  "allowed_fields": ["name", "employee_no"],
  "constraints": {
    "name_max_length": 20,
    "employee_no_length": 6
  }
}
```

## 5. Start server

``` bash
uvicorn app:app --reload
```

------------------------------------------------------------------------

# 🔥 API Endpoints

## **GET /**

``` json
{ "message": "Cognitive Data Intelligence & Autonomous Workflow System",
  "Run locally": "http://127.0.0.1:8000/docs"}
```

## **GET /health**
``` json
{ "status": "ok" }
```

## **POST /validate**

Example payload:

``` json
{
  "name": "Yogesh",
  "employee_no": "EMP908"
}
```
Example valid response:

``` json
{
  "status": "valid",
  "message": "Successfully validated",
  "used_rule_version": "1.1"
}
```
## **GET /get_rules**
Example valid response:

``` json
{
  "version": "1.0",
  "allowed_fields": ["name", "employee_no", "salary"],
  "constraints": {
    "name_max_length": 20,
    "employee_no_length": 6
  }
}
```
## **POST /update_rules**
Example payload:\
Here we add a new extra variable salary 
``` json
{
  "new_rules": {
    "version": "1.2",
    "allowed_fields": ["name", "employee_no", "salary"],
    "constraints": {
      "name_max_length": 30,
      "employee_no_length": 6
    },
    "metadata": { "updated_by": "admin" }
  },
  "admin": "admin_user",
  "reason": "Added salary field support"
}
```
Example valid response:

``` json
{
  "status": "success",
  "message": "Rules updated successfully",
  "new_version": "1.2"
}
```
## **GET /audit_log**

Example payload:

Example valid response:

``` json
[
  {
    "timestamp": "2025-12-11T06:12:52.904410",
    "old_rules": { ... },
    "updated_by": "admin_user",
    "reason": "Added salary field"
  }
]
```

## **GET /validation_logs**
Example valid response:

``` json
[
  {
    "timestamp": "2025-12-11T06:30:10.115220",
    "payload": {
      "name": "Yogesh",
      "employee_no": "EMP908"
    },
    "status": "valid",
    "rule_version": "1.1"
  }
]
```


------------------------------------------------------------------------
# 💡 Advantages of This System
**✔ Hot-swappable dynamic rules**\
No need to redeploy or change backend code

**✔ Full auditability**\
Every rule update is recorded with:
- timestamp
- admin user
- reason
- old rule snapshot

**✔ Distributed-safe**
- Any instance can read the same rule files.

**✔ Enterprise-ready**
- Can be extended into:
- document workflows
- form validation systems
- compliance engines
- policy enforcement layers
------------------------------------------------------------------------

# 🔮 Future Enhancements
- **Email alert workflow**\
Automatically notify admins when unknown fields are detected\
rule updates are requested
-  **AI‑assisted rule inference**
Predict rule updates\
Auto-generate constraints from sample data\
Identify invalid patterns\
Suggest schema improvements
-   **Multi-admin approval system**
-   **Validation plugins**
-   **Distributed rule replication**

------------------------------------------------------------------------

# 🎯 Conclusion

This system delivers a strong foundation for intelligent, dynamic document validation. It is flexible, extendable, and future-ready for AI-driven automation and enterprise workflows.