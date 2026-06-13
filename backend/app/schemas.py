"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field("", max_length=50)
    assets_range: Optional[str] = Field("", max_length=200)
    message: Optional[str] = Field("", max_length=2000)


class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    assets_range: str
    message: str
    source: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class WebhookCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    secret_key_ref: Optional[str] = ""
    encryption_enabled: bool = True
    payload_template: dict = {}
    max_payload_size_bytes: int = 5_000_000


class WebhookResponse(BaseModel):
    id: int
    name: str
    endpoint_path: str
    secret_key_ref: str
    encryption_enabled: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ContentSectionCreate(BaseModel):
    section_key: str = Field(..., min_length=2, max_length=100)
    section_name: str = Field(..., min_length=1, max_length=200)
    content_type: str = Field(..., pattern="^(heading|paragraph|table_row|list_item|callout)$")
    field_data: dict = {}
    order_index: int = 0
    style_data: dict = {}


class ContentSectionResponse(BaseModel):
    id: int
    section_key: str
    section_name: str
    content_type: str
    field_data: dict
    order_index: int
    style_data: dict
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900


class KPIMetrics(BaseModel):
    total_leads_7d: int = 0
    total_leads_30d: int = 0
    total_leads_all: int = 0
    leads_by_status: dict = {}
    form_submissions_7d: int = 0
    contact_form_success_rate: float = 0.0
    estimated_pipeline_value: int = 0


class HealthCheck(BaseModel):
    status: str = "healthy"
    database: str = "connected"
    cache: str = "connected"
