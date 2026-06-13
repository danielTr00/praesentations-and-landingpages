"""Database models for CLG Vermoegenschutz system.

7 Tables: users, content_sections, webhooks, webhook_events, leads, audit_log, contact_attempts
All tables support SQLite WAL mode with PRAGMA optimizations.
"""
from sqlalchemy import (
    Column, Integer, Text, Boolean, DateTime, ForeignKey, BigInteger
)
from sqlalchemy.dialects.sqlite import JSON
from app.database import Base
from datetime import datetime, timezone

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False, default="editor")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ContentSections(Base):
    """Flexible content storage for Landing Page sections."""
    __tablename__ = "content_sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_key = Column(Text, unique=True, nullable=False)
    section_name = Column(Text, nullable=False)
    content_type = Column(Text, nullable=False)
    field_data = Column(JSON, default=dict)
    order_index = Column(Integer, default=0)
    style_data = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

class Webhooks(Base):
    """Webhook configurations for n8n integration."""
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    endpoint_path = Column(Text, unique=True, nullable=False)
    secret_key_ref = Column(Text, default="")
    encryption_enabled = Column(Boolean, default=True)
    payload_template = Column(JSON, default=dict)
    max_payload_size_bytes = Column(BigInteger, default=5000000)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class WebhookEvents(Base):
    """Audit log for webhook deliveries."""
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id"))
    raw_payload_size_bytes = Column(BigInteger, default=0)
    encrypted_payload_size_bytes = Column(BigInteger, default=0)
    decrypted_record_size_bytes = Column(BigInteger, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Leads(Base):
    """Lead capture from contact forms and webhooks."""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, default="")
    email = Column(Text, default="")
    phone = Column(Text, default="")
    assets_range = Column(Text, default="")
    message = Column(Text, default="")
    source = Column(Text, default="landing_page_form")
    status = Column(Text, default="new")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AuditLog(Base):
    """Audit log for all admin actions."""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), default=None)
    action_type = Column(Text, nullable=False)
    target_table = Column(Text, default="")
    target_id = Column(Integer, default=0)
    old_values = Column(JSON, default=dict)
    new_values = Column(JSON, default=dict)
    ip_address = Column(Text, default="")
    user_agent = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ContactAttempts(Base):
    """Track contact form attempts for analytics."""
    __tablename__ = "contact_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Text, default="")
    ip_address = Column(Text, default="")
    success = Column(Boolean, default=False)
    attempt_type = Column(Text, default="form_submit")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
