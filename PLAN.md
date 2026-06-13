# CLG Vermögensschutz — Technical Plan & Analysis

## 1. PROJEKT-ZUSAMMENFASSUNG

Eine Landing Page für DACH-Mandanten zum Thema UK CLG (Company Limited by Guarantee) als Vermögensschutz-Struktur.
Ziel: Kunden generieren, Transparenz schaffen, Vertrauen aufbauen.

**System:** Full-Stack mit Docker — FastAPI Backend + Admin Panel + KPI Dashboard.

---

## 2. COMPETITIVE ANALYSIS

### Benchmark-Anbieter

| # | Anbieter | URL | Fokus |
|---|---|---|---|
| 🥇 | Stripe Atlas | stripe.com/atlas | US-Firmengründung, All-in-One |
| 🥈 | Firstbase | firstbase.io | Startup Operating System (Formation + Compliance + Bookkeeping) |
| 🥉 | Doola | doola.com | LLC Formation, Bookkeeping, Tax Filings |

### Hero Headline Patterns

| Company | Hero H1 | Subheadline | CTA Text |
|---|---|---|---|
| Stripe Atlas | "Firma gründen in den USA mit Stripe" | "in nur wenigen Klicks... wir kümmern uns um die Papiere" | "Get Started" |
| Firstbase | "The all-in-one startup operating system" | "Incorporation, compliance, bookkeeping, and taxes – all in one place." | "Start my business/company" |
| Doola | "Do the Business Side of Things, Better." | Section-specific subheads (Bookkeeping, Tax Filings, etc.) | Multiple CTAs |

### Social Proof & Trust Signals

| Company | Reviews/Trust Mentions | Social Proof Type |
|---|---|---|
| Firstbase | 34+ review mentions | "30,000+ companies started", Customer Logos |
| Doola | 7 reviews/ratings | Testimonial Cards, Rating Badges |
| Stripe Atlas | Heavy | Client Carousel, Trustpilot Integration |

### CTA Patterns

- **Firstbase**: Action-oriented CTAs ("Start my business/company")
- **Stripe Atlas**: Multiple CTAs im Flow (Get Started / Learn More)
- **Doola**: Secondary per-Section CTAs + Primary Hero CTA

### Content Architecture Patterns

| Element | Stripe Atlas | Firstbase | Doola |
|---|---|---|---|
| Hero mit H1 + Subheadline | ✅ | ✅ | ✅ |
| Social Proof direkt unter Hero | ✅ | "30K+ Companies" | ✅ |
| Feature Cards (4–10) | ✅ | ✅ | ✅ |
| Transparente Pricing Section | ✅ Grid | ✅ Tiered Plans | ✅ 3 Tiers |
| FAQ mit Accordion | Teilweise | ✅ | ✅ |
| Testimonials / Case Studies | Carousel | Einzelne Cards | Multiple Cards |
| Trust Badges / Partner Logos | Ja | "As seen in" | Review Badges |

### Navigation Patterns

- **Mobile**: Hamburger Menu, 5–7 Hauptsektionen
- **Desktop**: Sticky Topbar mit klaren Links (Product, Pricing, Resources, Login)
- Alle 3 Anbieter haben klare Content-Hierarchie und fokussieren auf Conversion

---

## 3. EMPFEHLUNGEN FÜR DIE CLG LANDING PAGE

Basierend auf der Analyse:

### A) Hero Section (Priority 1 — Critical)
```
H1:          "Vermögensschutz für DACH-Mandanten"
Subheadline: "Die UK CLG-Struktur – transparent, rechtssicher, umsetzbar."
Primary CTA:      "Jetzt Beratung anfragen →"
Secondary CTA:    "Mehr erfahren"
Trust Bar:        "UK Registered" | "DACH-kompatibel" | "Transparent"
```

### B) Content Structure (Priority 2 — Must Have)
1. **Hero** → mit Trust Signals direkt darunter
2. **CLG Erklärung** → Was ist eine CLG?
3. **Vorteile der UK CLG** → Cards mit Icons (ähnlich Firstbase Feature Grid)
4. **Risikoliste / Gefahrenampel** → Unique Differentiator
5. **Immobilien & Assets** → Asset Protection
6. **Steuerrecht** → Transparenz schafft Vertrauen
7. **FAQ** → Mit Accordion (wie Doola/Firstbase)
8. **Checkliste** → Interaktiver CTA-Funnel

### C) Conversion-Optimierung (Priority 3 — High Impact)
1. Sticky CTA Button auf Mobile (fixiert am unteren Rand)
2. Fortlaufende CTA-Punkte alle 2–3 Sektionen
3. Social Proof: z.B. "Seit 2024 umgesetzt für DACH-Mandanten"
4. Trust Badges neben jedem CTA

### D) Navigation (Priority 4 — Medium Impact)
- Mobile: Hamburger Menu mit klaren Sektionen
- Desktop: Sticky Topbar mit 5–7 Links
   - Übersicht | Vorteile | CLG DE/AT | Risikoliste | FAQ | Kontakt

---

## 4. ARCHITEKTUR-ÜBERSICHT

```
┌─────────────────────────────────────────────────────┐
│                    KPI DASHBOARD                         │
│    [Leads] [Kontakte] [Konversionen] [Webhook Events]      │
│    [Einnahmen-Schätzung] [Performance-Metriken]            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                     ADMIN PANEL                          │
│    ┌──────────┬──────────────┬───────────────┬───────────┐   │
│    │ CONTENT    │ WEBHOOKS       │ USER MGT        │ AUDIT LOG │   │
│    │ Editor     │ Config/Tests │ Roles/Perms     │ Viewer      │   │
│    └──────────┴──────────────┴───────────────┴───────────┘   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                        │
│   JWT Auth   │  Content API     │  Webhook Receiver │ KPI │
└──────────────────────────┬──────────────────────────┘
                             │      /api/v1/*
                      ┌──────▼───────┐
                      │   Nginx        │
                      │  Port 443/80   │
                      │  TLS + Brotli│
                      │  Rate Limit   │
                      └──────────────┘
```

---

## 5. DOCKER STRUKTUR (docker-compose.yml)

### Three Containers:
1. **`nginx`** — Reverse proxy, static file server, TLS termination, gzip/brotli compression
2. **`backend`** (FastAPI + Uvicorn via Gunicorn workers) — All business logic, API endpoints, webhook receiver, encryption service
3. **`redis`** (optional, fallback to in-memory LRU) — Caching layer, rate limiting store, session storage

---

## 6. DATENBANK SCHEMA (SQLite mit WAL + PRAGMA Optimierungen)

### Table: `users`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| username | TEXT UNIQUE | Admin login name |
| password_hash | TEXT | bcrypt $2b$14... |
| role | TEXT | 'superadmin' or 'editor' |
| created_at | DATETIME | Default CURRENT_TIMESTAMP |

### Table: `content_sections`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| section_key | TEXT UNIQUE | e.g. 'hero', 'faq_1', 'risk_red_1' |
| section_name | TEXT | Display name for admin UI |
| content_type | TEXT | 'heading', 'paragraph', 'table_row', 'list_item', 'callout' |
| field_data | JSONB | Flexible storage: {"title": "...", "body": "..."} |
| order_index | INTEGER | For sorting list items |
| style_data | JSONB | Optional color/alignment overrides |
| updated_at | DATETIME | Auto timestamp |

### Table: `webhooks`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| name | TEXT | e.g. 'n8n_clg_inquiry' |
| endpoint_path | TEXT UNIQUE | e.g. '/webhooks/clg-form-submitted' |
| secret_key_ref | TEXT | env var name containing AES-256 key |
| encryption_enabled | BOOLEAN | Default true |
| payload_template | JSONB | Schema for n8n to follow |
| max_payload_size_bytes | INTEGER | Default 5MB |
| is_active | BOOLEAN | Default true |
| created_at | DATETIME | Auto timestamp |

### Table: `webhook_events`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| webhook_id | INTEGER FK | References webhooks.id |
| raw_payload_size_bytes | INTEGER | Pre-decryption size |
| encrypted_payload_size_bytes | INTEGER | Encrypted payload size |
| decrypted_record_size_bytes | INTEGER | Decrypted record size |
| created_at | DATETIME | Auto timestamp |

### Table: `leads`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| name | TEXT | Contact person |
| email | TEXT | Email address |
| phone | TEXT | Optional |
| assets_range | TEXT | e.g. '100k-500k EUR' |
| message | TEXT | User inquiry text |
| source | TEXT | 'landing_page_form' or 'webhook' |
| status | TEXT | 'new', 'contacted', 'qualified', 'lost' |
| created_at | DATETIME | Auto timestamp |

### Table: `audit_log`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| user_id | INTEGER FK | Who made the change |
| action_type | TEXT | 'create', 'update', 'delete', 'login' |
| target_table | TEXT | Which table was affected |
| target_id | INTEGER | Record ID that changed |
| old_values | JSONB | Previous state |
| new_values | JSONB | New state |
| ip_address | TEXT | Request IP |
| user_agent | TEXT | Browser/client info |
| created_at | DATETIME | Auto timestamp |

---

## 7. KPI DASHBOARD SPEC

### A) Lead Generation Metrics
- Total leads (last 7d, 30d, all-time)
- Leads by status (new, contacted, qualified, lost)
- Leads by source (landing_page_form, webhook)
- Weekly trend line chart

### B) Contact Metrics
- Total contacts reached out
- Response rate (%)
- Average response time
- Most active contact days

### C) Revenue Estimation
- Estimated fees per lead tier (Low: 500€, Mid: 1500€, High: 3000€+)
- Pipeline value based on lead status
- Monthly recurring potential (based on qualified leads)

### D) Performance Metrics
- API response times (P50, P90, P99)
- Webhook delivery success rate
- Error rate by endpoint

---

## 8. FASTAPI ENDPOINTS

### Auth Module (`/api/auth/*`)
```python
POST     /api/auth/login             → {access_token, refresh_token}
POST     /api/auth/refresh            → New access token
POST     /api/auth/logout             → Invalidate refresh token
GET      /api/auth/me                 → Current user info
```

### Content Module (`/api/content/*`)
```python
GET      /api/content/sections        → Get all content sections
GET      /api/content/sections/{key}  → Get specific section
POST     /api/content/sections        → Create new section
PUT      /api/content/sections/{key}  → Update existing section
DELETE   /api/content/sections/{key}  → Delete section

# Bulk operations:
POST     /api/content/batch/update    → Update multiple sections at once
POST     /api/content/export          → Export all content as JSON
POST     /api/content/import          → Import content from JSON
```

### Webhooks Module (`/api/webhooks/*`)
```python
# Configuring webhooks:
GET      /api/admin/webhooks            → List all configured webhooks
POST     /api/admin/webhooks            → Create webhook config
PUT      /api/admin/webhooks/{id}       → Update webhook config
DELETE   /api/admin/webhooks/{id}       → Delete webhook

# Receiving n8n payloads:
POST     /webhooks/{endpoint_path}      → Receive encrypted payload
                                         decrypt and process
                                         log event
                                         return 200 OK

# Testing webhooks:
POST     /api/admin/webhooks/{id}/test  → Send test payload to endpoint
```

### KPI / Analytics (`/api/kpi/*`)
```python
GET      /api/kpi/overview              → All KPI summary metrics
GET      /api/kpi/leads                 → Lead-specific metrics
GET      /api/kpi/funnel                → Conversion funnel data
GET      /api/kpi/revenue               → Revenue estimates
GET      /api/kpi/performance           → Performance metrics
GET      /api/kpi/trend/{days}          → Trend data for charts
```

---

## 9. N8N WEBHOOK SPECIFICATION

### Webhook URL Pattern:
```
https://yourdomain.com/webhooks/clg-inquiry
```

### Request Format (from n8n to our server):
```http
POST /webhooks/clg-inquiry
Content-Type: application/json
X-Webhook-Source: n8n-workflow
X-Timestamp: 2024-06-13T15:30:00Z

{
    "encrypted_payload": "base64-encoded-aes-gcm-output...",
    "iv": "base64-initialization-vector",
    "tag": "base64-authentication-tag",
    "version": 1,
    "metadata": {
      "workflow_id": "n8n-clg-inquiry-01",
      "timestamp": "2024-06-13T15:30:00Z",
      "source_ip": "192.168.1.100"
    }
}
```

### Binary Data Support:
The `encrypted_payload` can contain base64-encoded binary data alongside the JSON form data. The server decrypts everything, then extracts both the JSON payload and any attached files (PDF forms, signature scans, etc.).

---

## 10. SECURITY IMPLEMENTATION DETAIL

### Encryption Service (`encryption_service.py`)
- Uses `cryptography` library (Fernet/AES-GCM)
- Keys stored in environment variables ONLY (never DB)
- AES-256-GCM for authenticated encryption with nonce
- Automatic key rotation support (rotate every 90 days)

### Rate Limiting (`rate_limit.py`)
```python
# Per-IP rate limits (Redis or LRU fallback):
Standard API:      100 req/min
Content API:        30 req/min  
Webhook endpoint: 60 req/min
Admin endpoints:     5 req/min
Login attempts:      3 req/10min
```

### JWT Configuration:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
```

---

## 11. ADMIN PANEL UI SPECIFICATION

### Layout:
```
┌─────────────────────────────────────────────┐
│ [Logo] CLG Admin        [Dashboard] [Content] │
│                             [Webhooks] [KPIs]    │
│                                     [Logout]      │
├─────────────────────────────────────────────┤
│                                              │
│  Main Content Area (SPA-style routing)         │
│                                              │
│   ┌──────────────────────────────────────┐     │
│   │ KPI Overview Cards                   │     │
│   │ [Leads] [Contacts] [Conversion]       │     │
│   ├──────────────────────────────────────┤     │
│   │ Charts:                                 │     │
│   │ [Trend Line] [Funnel] [Sources Pie]    │     │
│   └──────────────────────────────────────┘     │
│                                              │
└─────────────────────────────────────────────┘
```

### Content Editor Features:
- Visual Form Builder for sections
- Live Preview of changes on the landing page
- Version History (30-day retention)
- Export/Import (JSON-based backup and restore)
- Field Types: Text, Rich Text, Number, Color Picker, URL, Select

### Webhook Configuration UI:
- Form fields for endpoint path, secret key reference
- Toggle switches for encryption and binary support
- Test button (sends test payload to endpoint)
- Event log viewer

---

## 12. IMPLEMENTATION PHASES

### Phase 1: Foundation (Day 1–2)
- [ ] Docker Compose structure with nginx + backend containers
- [ ] FastAPI skeleton with proper project structure
- [ ] SQLite database setup with WAL mode
- [ ] Basic models and migration scripts

### Phase 2: Core API (Day 3–5)
- [ ] Authentication system (JWT login/refresh/logout)
- [ ] Content CRUD endpoints (fully tested)
- [ ] Admin panel basic UI (content editing interface)
- [ ] Audit logging for all changes

### Phase 3: Webhooks + Encryption (Day 6–7)
- [ ] AES-256-GCM encryption service
- [ ] Webhook receiver endpoint with automatic decryption
- [ ] n8n payload format specification and examples
- [ ] Binary data support in webhook payloads

### Phase 4: KPI Dashboard (Day 8–10)
- [ ] Lead tracking and status management
- [ ] Analytics aggregation endpoints
- [ ] KPI dashboard UI with charts
- [ ] Revenue estimation calculations

### Phase 5: Polish & Deployment (Day 11–12)
- [ ] Rate limiting implementation
- [ ] Security hardening (CSP, HSTS, CORS)
- [ ] Performance optimization (caching, connection pooling)
- [ ] Documentation and deployment guide

---

## 13. TECHNICAL DEPENDENCIES

### Python Backend:
```text
fastapi==0.115.*
uvicorn[standard]==0.34.*
gunicorn==23.*
sqlalchemy==2.0.*
pydantic==2.*
python-jose[cryptography]==3.*
bcrypt==4.*
cryptography==44.*
python-dotenv==1.*
aiosqlite==0.*
```

### Docker Services:
- nginx:1.25-alpine (with brotli compiled in)
- python:3.12-slim (backend image base)
- redis:7-alpine (optional, for production rate limiting)
