from src.agents import run_compliance_crew
from src.models import AuditRequest


def test_compliant_environment():
    req = AuditRequest(
        organization="Demo Bank",
        environment="prod",
        iam_mfa_enforced=True,
        wildcard_admin_roles=0,
        backup_verified_days_ago=2,
        gpo_password_policy_enabled=True,
    )
    report = run_compliance_crew(req)
    assert report.overall_status == "Compliant"
    assert len(report.findings) == 0


def test_critical_iam_findings():
    req = AuditRequest(
        organization="Demo Bank",
        environment="prod",
        iam_mfa_enforced=False,
        wildcard_admin_roles=2,
        backup_verified_days_ago=10,
        gpo_password_policy_enabled=True,
    )
    report = run_compliance_crew(req)
    assert report.overall_status == "Critical Risk"
    assert len(report.findings) == 3
