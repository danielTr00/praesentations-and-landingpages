"""Admin router for content management and admin panel.

This router handles all admin operations including:
- Content section CRUD (text editing)
- Webhook configuration
- KPI dashboard data
- Audit log viewing
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_session
from app.models import ContentSections, Webhooks, Leads, Users, AuditLog, ContactAttempts
from datetime import datetime, timezone
from typing import Optional

router = APIRouter()
logger = logging.getLogger(__name__)


class AdminLoginRequest(BaseModel):
    username: str
    password: str


@router.get("/admin/leads", response_model=list)
async def admin_leads(session: Session = Depends(get_session)):
    """Get all leads for admin dashboard."""
    leads = session.query(Leads).order_by(Leads.created_at.desc()).limit(100).all()
    
    return [
         {
              "id": lead.id,
              "name": lead.name,
              "email": lead.email,
              "phone": lead.phone or "",
              "assets_range": lead.assets_range or "",
              "message": (lead.message or "")[:100],    # Truncate for preview
              "source": lead.source,
              "status": lead.status,
              "created_at": lead.created_at.isoformat() if lead.created_at else None,
          }
         for lead in leads
     ]


@router.get("/admin/content", response_model=list)
async def admin_content(session: Session = Depends(get_session)):
    """Get all content sections for admin CMS."""
    sections = session.query(ContentSections).all()
    
    return [
         {
              "id": s.id,
              "section_key": s.section_key,
              "section_name": s.section_name,
              "content_type": s.content_type,
              "field_data": s.field_data or {},
              "order_index": s.order_index,
              "style_data": s.style_data or {},
          }
         for s in sections
     ]


@router.post("/admin/content/{section_key}", response_model=dict)
async def admin_update_content(
    section_key: str,
    data: dict,
    session: Session = Depends(get_session),
):
    """Update a content section (admin CMS)."""
    section = session.query(ContentSections).filter(
        ContentSections.section_key == section_key
     ).first()
    
       if not section:
         raise HTTPException(status_code=404, detail="Content section not found")
    
        # Update fields
    for key, value in data.items():
           if hasattr(section, key):
               setattr(section, key, value)
    
    session.commit()
    return {"status": "success", "section_key": section_key}


@router.get("/admin/webhooks", response_model=list)
async def admin_webhooks(session: Session = Depends(get_session)):
    """Get all webhook configurations."""
    webhooks = session.query(Webhooks).all()
    
    return [
          {
              "id": w.id,
              "name": w.name,
              "endpoint_path": w.endpoint_path,
              "encryption_enabled": w.encryption_enabled,
              "is_active": w.is_active,
              "created_at": w.created_at.isoformat() if w.created_at else None,
          }
         for w in webhooks
     ]


@router.get("/admin/audit-log", response_model=list)
async def admin_audit_log(session: Session = Depends(get_session)):
    """Get audit log entries."""
    logs = session.query(AuditLog).order_by(
        AuditLog.created_at.desc()
     ).limit(50).all()
    
    return [
          {
              "id": log.id,
              "user_id": log.user_id,
              "action_type": log.action_type,
              "target_table": log.target_table,
              "target_id": log.target_id,
              "ip_address": log.ip_address,
              "created_at": log.created_at.isoformat() if log.created_at else None,
          }
         for log in logs
     ]
