# CLG Vermögensschutz - Landing Page & Admin System

## Overview
A complete landing page system for UK CLG (Company Limited by Guarantee) wealth protection targeting DACH market. Built with maximum security, performance optimization, and conversion focus.

## Architecture
```
┌───────────┐     ┌──────────────┐     ┌──────────┐
│  Browser   │────▶│   Nginx      │────▶│  FastAPI │
│ (Landing   │     │  (SSL, Rate  │     │  (SQLite │
│   Page +   │◀────│   Limiting)  │◀────│   WAL +   │
│  Admin)    │     └──────────────┘     │   Redis) │
└───────────┘                          └──────────┘
                                              │
                                         ┌────┴────┐
                                         │ n8n     │
                                         │ Webhook │
                                         └─────────┘
```

## Components

### 1. Landing Page (`/frontend`)
- **Mobile-first responsive** design with dark theme
- **SEO optimized** (Schema.org JSON-LD, OpenGraph, Twitter Cards)
- **Conversion-focused** with trust signals, FAQ accordion, contact form
- **Performance target**: <80KB total, LCP < 1.2s on 3G

### 2. Admin Panel (`/admin-panel`)
- **KPI Dashboard**: Lead counts, quality distribution, pipeline value
- **Webhook Config**: n8n integration settings, AES-256-GCM encryption
- **Content Editor**: Edit landing page text content dynamically
- **Leads Management**: View, filter, update lead status

### 3. Backend API (`/backend`)
- **FastAPI** with SQLite WAL mode (fastest SQLite option)
- **Health check**: `/api/health` for Docker monitoring
- **Lead submission**: `POST /api/leads/submit`
- **Admin leads**: `GET /api/admin/leads`
- **KPI Dashboard**: `GET /api/kpi/dashboard`

### 4. Docker Stack (`docker-compose.yml`)
```bash
# Start everything
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check (Docker) |
| POST | `/api/leads/submit` | Submit contact form lead |
| GET | `/api/admin/leads` | Get all leads for admin |
| GET | `/api/kpi/dashboard` | KPI dashboard data |

## Development

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_db.py  # Initialize database
uvicorn app.main:app --reload  # Run with hot reload
```

### Frontend Testing
```bash
cd frontend
python3 -m http.server 8080
# Visit http://localhost:8080
```

### Admin Panel
```bash
cd admin-panel
python3 -m http.server 8081
# Visit http://localhost:8081/admin/ (redirect)
# Or open admin-panel/index.html directly
```

## Research & Strategy
- `seo-visual-research.md` — Deep SEO keywords, visual patterns, conversion tactics
- `research-summary.md` — Competitor analysis (Stripe Atlas, Firstbase, Doola)
- `PLAN.md` — Full technical plan with DB schema and security details

## Docker Compose Services
| Service | Port | Description |
|---------|------|-------------|
| nginx | 80/443 | SSL termination, rate limiting, static files |
| fastapi | 8000 | FastAPI backend with SQLite WAL + Redis cache |
| redis | 6379 | KPI caching, session storage |

## Security Features
- JWT authentication (15min access + 7day refresh)
- Rate limiting per IP (10 req/min for API, 5/min for admin)
- AES-256-GCM webhook encryption
- CSP headers (Strict-Mode)
- HSTS with 365-day max-age
- SQLite WAL mode for concurrent read safety

## Performance Targets
- **Page Size**: <80KB total
- **LCP**: <1.2s on 3G network
- **FID/INP**: <80ms
- **CLS**: <0.05
- **Cache Hit Rate**: >80% (Redis)

---
*Built for maximum security, conversion optimization, and DACH-market SEO dominance.*
