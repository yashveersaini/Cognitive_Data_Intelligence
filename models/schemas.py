from pydantic import BaseModel, Field
from pydantic import StringConstraints
from typing import List, Optional, Dict, Any, Annotated
from typing import Annotated

class DocumentInput(BaseModel):
    class Config:
        extra = "allow"

class RuleConstraints(BaseModel):
    name_max_length: Optional[int] = None
    employee_no_length: Optional[int] = None

class RulesModel(BaseModel):
    version: str
    allowed_fields: List[str]
    constraints: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class RuleUpdateRequest(BaseModel):
    new_rules: RulesModel
    admin: Optional[str] = None
    reason: Optional[str] = None

