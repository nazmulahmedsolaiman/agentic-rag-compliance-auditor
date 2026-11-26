from typing import List, Literal
from pydantic import BaseModel, Field


Severity = Literal["High", "Medium", "Low"]


class AuditRequest(BaseModel):
    organization: str = Field(..., examples=["Enterprise FinTech Corp"])
    environment: str = Field(..., examples=["production-cloud"])
    iam_mfa_enforced: bool = True
    wildcard_admin_roles: int = Field(0, ge=0)
    backup_verified_days_ago: int = Field(1, ge=0)
    gpo_password_policy_enabled: bool = True


class ControlFinding(BaseModel):
    control_id: str
    domain: str
    severity: Severity
    finding: str
    remediation: str


class AuditReport(BaseModel):
    organization: str
    environment: str
    overall_status: Literal["Compliant", "Action Required", "Critical Risk"]
    findings: List[ControlFinding]
    summary: str
