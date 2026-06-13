"""KPI Dashboard router for analytics and metrics.

Provides real-time metrics for the admin dashboard including:
- Lead Generation (7d, 30d, all-time)
- Contact Form success rates
- Estimated pipeline value
- Performance metrics (if Redis available)
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Leads, ContactAttempts
from datetime import datetime, timezone, timedelta
from typing import Dict

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/kpi/dashboard", response_model=dict)
async def get_kpi_dashboard(session: Session = Depends(get_session)):
    """Get all KPI metrics for the dashboard."""
       # Get date thresholds (UTC times as strings for SQLite)
    now = datetime.now(timezone.utc)
    seven_days_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    thirty_days_ago = (now - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    
       # Total leads by period
    total_all = session.query(Leads).count()
    total_7d = session.query(Leads).filter(
        Leads.created_at > seven_days_ago
     ).count()
    total_30d = session.query(Leads).filter(
        Leads.created_at > thirty_days_ago
     ).count()
    
         # Leads by status
     leads_by_status: Dict[str, int] = {}
      for status in ["new", "contacted", "qualified", "lost"]:
           count = session.query(Leads).filter(Leads.status == status).count()
          leads_by_status[status] = count
    
         # Form submission success rate (from contact_attempts)
     total_attempts = session.query(ContactAttempts).count()
     successful_attempts = session.query(ContactAttempts).filter(
         ContactAttempts.success == True
      ).count()
    
    success_rate = (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0.0
    
       # Estimated pipeline value (lead count * average deal size €5,000)
     avg_lead_value = 5000
     estimated_pipeline = total_all * avg_lead_value
    
    return {
         "total_leads_7d": total_7d,
         "total_leads_30d": total_30d,
         "total_leads_all": total_all,
         "leads_by_status": leads_by_status,
         "form_submissions_7d": total_7d,
         "contact_form_success_rate": round(success_rate, 2),
         "estimated_pipeline_value": estimated_pipeline,
     }


@router.get("/kpi/leads-by-period", response_model=list)
async def get_leads_by_period(session: Session = Depends(get_session)):
    """Get lead counts by day for the last 7 days."""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    
    results = []
    for i in range(7):
         day = (now - timedelta(days=6-i)).strftime("%Y-%m-%d")
        count = session.query(Leads).filter(
            Leads.created_at > day,
            Leads.created_at < f"{day} 23:59:59"
         ).count()
        
          results.append({
               "date": day,
              "leads": count,
           })
    
    return results
