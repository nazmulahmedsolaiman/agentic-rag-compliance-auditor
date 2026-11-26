from typing import List
from src.models import AuditReport, AuditRequest, ControlFinding


ICT_POLICY_BASELINE = {
    "IAM-01": "All privileged accounts must enforce Multi-Factor Authentication (MFA).",
    "IAM-02": "Least-privilege IAM must be enforced with zero wildcard (*) admin roles.",
    "BCP-01": "Multi-destination database backups must be verified within every 7 days.",
    "SEC-01": "Group Policy (GPO) password complexity and lockout rules must be active.",
}


def policy_retriever_agent() -> dict:
    """Agent 1: Retrieves relevant ICT security & compliance baseline controls."""
    return ICT_POLICY_BASELINE


def control_verifier_agent(req: AuditRequest, policies: dict) -> List[ControlFinding]:
    """Agent 2: Evaluates infrastructure state against retrieved ICT policy baselines."""
    findings: List[ControlFinding] = []

    if not req.iam_mfa_enforced:
        findings.append(
            ControlFinding(
                control_id="IAM-01",
                domain="Identity & Access Management",
                severity="High",
                finding=f"MFA is not enforced in {req.environment}. Policy: {policies['IAM-01']}",
                remediation="Enforce mandatory MFA across all IAM and SSO user groups.",
            )
        )

    if req.wildcard_admin_roles > 0:
        findings.append(
            ControlFinding(
                control_id="IAM-02",
                domain="Least-Privilege Access",
                severity="High",
                finding=f"Detected {req.wildcard_admin_roles} wildcard admin role(s). Policy: {policies['IAM-02']}",
                remediation="Scope IAM policies to explicit resource ARNs and required actions only.",
            )
        )

    if req.backup_verified_days_ago > 7:
        findings.append(
            ControlFinding(
                control_id="BCP-01",
                domain="Backup & Business Continuity",
                severity="Medium",
                finding=f"Last backup verification was {req.backup_verified_days_ago} days ago. Policy: {policies['BCP-01']}",
                remediation="Run automated restore verification to NAS and Cloud backup targets.",
            )
        )

    if not req.gpo_password_policy_enabled:
        findings.append(
            ControlFinding(
                control_id="SEC-01",
                domain="Endpoint & Directory Security",
                severity="Medium",
                finding=f"GPO password policy is disabled. Policy: {policies['SEC-01']}",
                remediation="Enable Active Directory GPO password complexity and account lockout.",
            )
        )

    return findings


def audit_report_writer_agent(req: AuditRequest, findings: List[ControlFinding]) -> AuditReport:
    """Agent 3: Synthesizes executive audit report and overall compliance status."""
    has_high = any(f.severity == "High" for f in findings)
    if has_high:
        status = "Critical Risk"
    elif findings:
        status = "Action Required"
    else:
        status = "Compliant"

    summary = (
        f"Audit completed for {req.organization} ({req.environment}): "
        f"{len(findings)} finding(s) identified. Status: {status}."
    )
    return AuditReport(
        organization=req.organization,
        environment=req.environment,
        overall_status=status,
        findings=findings,
        summary=summary,
    )


def run_compliance_crew(req: AuditRequest) -> AuditReport:
    policies = policy_retriever_agent()
    findings = control_verifier_agent(req, policies)
    return audit_report_writer_agent(req, findings)
