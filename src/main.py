from fastapi import FastAPI
from src.agents import run_compliance_crew
from src.config import settings
from src.models import AuditReport, AuditRequest

app = FastAPI(
    title="Agentic RAG Compliance & IT Audit Assistant",
    version="1.0.0",
    description="CrewAI + PostgreSQL multi-agent ICT compliance auditing API",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}


@app.post("/api/v1/audit", response_model=AuditReport)
def run_audit(request: AuditRequest):
    return run_compliance_crew(request)
