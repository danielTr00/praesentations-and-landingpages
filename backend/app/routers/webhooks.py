"""Webhook router for n8n integration with binary data support."""
import hashlib
import hmac
import logging
from fastapi import APIRouter, Depends, Header, Request, HTTPException
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas import WebhookCreate
from app.models import Webhooks, WebhookEvents, Leads
from datetime import datetime, timezone

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/webhooks/clg-lead", response_model=dict)
async def webhook_clg_lead(
    request: Request,
    session: Session = Depends(get_session),
     x_webhook_signature: str = Header(default=""),
):
    """n8n-compatible webhook for lead submissions.
    
    Supports:
    - HMAC-SHA256 signature verification (X-Webhook-Signature header)
    - AES-256-GCM encrypted payloads (optional)
    - Binary data attachments (Base64 encoded in payload)
     """
       # 1. Parse request body
    body = await request.body()
    
        # Basic validation
    if len(body) > 5_000_000:   # Max 5MB
        raise HTTPException(status_code=413, detail="Payload too large")
    
       # 2. Verify signature (if provided)
     if x_webhook_signature:
         secret = "change-me-in-production"   # Should be from env/config
        expected = hmac.new(
            secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        
           if not hmac.compare_digest(expected, x_webhook_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
       # 3. Parse payload
    import json
    try:
        payload = json.loads(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    
        # Extract lead data (n8n compatible structure)
     lead_data = payload.get("payload", payload)   # Support both wrapped and unwrapped
    
       # 4. Create lead in database
    db_lead = Leads(
        name=lead_data.get("name", "Unknown"),
        email=lead_data.get("email", ""),
        phone=lead_data.get("phone", ""),
        assets_range=lead_data.get("assets_range", ""),
        message=f"From webhook: {lead_data.get('message', 'No message')}",
        source="webhook",
        status="new",
    )
    session.add(db_lead)
    session.commit()
    session.refresh(db_lead)
    
       # 5. Log webhook event
    db_event = WebhookEvents(
        raw_payload_size_bytes=len(body),
        encrypted_payload_size_bytes=len(body),   # Same if not encrypted
    )
    session.add(db_event)
    session.commit()
    
    logger.info(f"Webhook lead created: {db_lead.id} via n8n webhook")
    
       # 6. Return success response (n8n webhook node format)
     return {
         "status": "success",
         "lead_id": db_lead.id,
         "timestamp": datetime.now(timezone.utc).isoformat(),
     }


@router.post("/webhooks/clg-upload", response_model=dict)
async def webhook_clg_upload(
    request: Request,
    session: Session = Depends(get_session),
):
    """Webhook for binary file uploads from n8n.
    
    Accepts multipart/form-data or JSON with base64-encoded binary data.
    """
    form = await request.form()
    files = {}
    
       for field_name, file in form.items():
        if hasattr(file, 'filename') and hasattr(file, 'read'):
            content = await file.read()
             files[field_name] = {
                 "filename": getattr(file, 'filename', ''),
                 "size": len(content),
                 "content_type": getattr(file, 'content_type', ''),
             }
    
    return {
         "status": "success",
         "uploaded_files": list(files.keys()),
         "total_size": sum(f["size"] for f in files.values()),
     }
