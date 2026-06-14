"""Lead capture router for contact form submissions."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas import LeadCreate, LeadResponse
from app.models import Leads, ContactAttempts
from datetime import datetime, timezone

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/leads/submit", response_model=dict)
async def submit_lead(
    lead: LeadCreate,
    request: Request,
    session: Session = Depends(get_session),
):
    """Handle contact form submission."""
    client_ip = request.client.host if request.client else "unknown"

    # Rate limiting per IP (higher for testing)
    recent_count = session.query(ContactAttempts).filter(
        ContactAttempts.ip_address == client_ip,
    ).count()

    if recent_count > 100:
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    db_lead = Leads(
        name=lead.name.strip(),
        email=lead.email.strip().lower(),
        phone=lead.phone.strip() if lead.phone else "",
        assets_range=lead.assets_range.strip() if lead.assets_range else "",
        message=(lead.message.strip()[:2000] if lead.message else ""),
        source="landing_page_form",
        status="new",
    )
    session.add(db_lead)
    session.commit()
    session.refresh(db_lead)

    session.add(ContactAttempts(ip_address=client_ip, success=True, attempt_type="form_submit"))
    session.commit()

    logger.info(f"Lead created: {db_lead.id} - {db_lead.name}")
    return {"status": "success", "message": "Thank you! We will contact you within 24 hours.", "lead_id": db_lead.id}
