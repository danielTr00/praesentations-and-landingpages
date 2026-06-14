# CLG Vermögenerschutz - SSLIP Testing Guide

**Stand:** 14. Juni 2026  
**Branch:** `clg-vermoegensschutz`  
**Status:** ✅ Phase 1 Complete

---

## Schnellzugriff SSLIP

| Dienst | URL | Status |
|--------|-----|--------|
| **Landing Page** | http://192.168.178.87.sslip.io:8081/ | ✅ Running |
| **Backend API** | http://192.168.178.87:8000/api/health | ✅ Running |
| **Contact Form** | POST `http://192.168.178.87:8000/api/leads/submit` | ✅ Working |

---

## Systeme im Detail

### 1. Landing Page (Frontend)
- **Port:** 8081
- **Technologie:** Python HTTP Server (einfach, stabil)
- **SSLIP Zugang:** http://192.168.178.87.sslip.io:8081/
- **Features:** Mobile-first Design, Schema.org JSON-LD, FAQ Accordion, Contact Form mit SSLIP-Detection

### 2. Backend API (FastAPI)
- **Port:** 8000
- **Technologie:** FastAPI + SQLAlchemy + SQLite WAL Mode
- **SSLIP Zugang:** http://192.168.178.87:8000/api/*
- **Endpunkte:**
    - `GET /api/health` - Health Check
    - `POST /api/leads/submit` - Contact Form Submit
    - `GET /api/admin/leads` - Leads List (Admin)
    - `GET /api/kpi/dashboard` - KPI Dashboard
    - `POST /webhooks/clg-lead` - n8n Webhook

### 3. Kontaktformular
- **Status:** ✅ Alle Tests bestanden
- **SSLIP Detection:** Automatische API-URL-Erkennung in contact.js
- **Rate Limiting:** 20 Submissions pro IP (für Testing ausgiebig)
- **Erfassungsdaten:** Name, Email, Telefon, Vermögensbereich, Nachricht

---

## SSLIP Konfiguration

### Wie funktioniert SSLIP?
SSLIP.io ist ein DNS-Dienst, der automatisch IPs auflöst:
```
192.168.178.87.sslip.io → 192.168.178.87
```
Dies ermöglicht Testing über das lokale Netzwerk ohne echte Domain/SSL.

### Zugriff auf SSLIP
- **Vom Laptop:** http://192.168.178.87.sslip.io:8081/
- **Vom Handy (im selben WLAN):** http://192.168.178.87.sslip.io:8081/
- **Vom Tablet:** http://192.168.178.87.sslip.io:8081/

### SSLIP im Kontaktformular
Das Contact Form (contact.js) erkennt automatisch die SSLIP-Domain und leitet API-Anfragen an `http://192.168.178.87:8000/api/*` weiter.

---

## Testing Checklist

- [x] Backend Health Check (`GET /api/health`)
- [x] Contact Form Submit (`POST /api/leads/submit`)  
- [x] Leads Storage (SQLite, WAL Mode)
- [x] Admin Leads List (`GET /api/admin/leads`)
- [x] KPI Dashboard (`GET /api/kpi/dashboard`)
- [x] Frontend Serving (`index.html` auf Port 8081)
- [x] SSLIP DNS Resolution (`192.168.178.87.sslip.io`)
- [ ] Landing Page im Browser testen (Mobil/Desktop)
- [ ] SSLIP Kontaktformular testen

---

## Troubleshooting

### Backend startet nicht
```bash
pkill -9 -f uvicorn
cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend nicht erreichbar
```bash
pkill -9 -f "http.server"  
cd frontend && python3 -m http.server 8081 --bind 0.0.0.0
```

### SSLIP Domain löst nicht auf
- Stelle sicher, dass du im selben WLAN bist wie der Server
- Prüfe die lokale IP: `ifconfig | grep "inet "`
- DNS von sslip.io ist öffentlich und immer erreichbar

---

## Nächste Schritte

1. **Landing Page im Browser testen** (Mobil/Desktop)
2. **SSLIP Kontaktformular ausfüllen** und Leads prüfen
3. **Webhooks für n8n konfigurieren**  
4. **Admin Panel weiter entwickeln**

