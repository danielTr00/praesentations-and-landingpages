"""Test suite for contact form functionality."""
import json, sys

sys.path.insert(0, '/Users/Uni/Desktop/Coding/praesentations-and-landingpages/backend')

from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base


def test_lead_submission():
    """Test contact form lead submission."""
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
     # Submit a test lead
    response = client.post("/leads/submit", json={
        "name": "Test User",
        "email": "test@test.com",
        "phone": "+49 123 4567890",
        "assets_range": "over-1m",
        "message": "Test message"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "lead_id" in data
    print(f"  Lead created: {data['lead_id']}")
    print("  PASS: lead_submission")


def test_invalid_lead():
     """Test lead submission with invalid data."""
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
     # Submit without email validation
    response = client.post("/leads/submit", json={
        "name": "",
        "email": "invalid-email"
    })

     assert response.status_code == 200
    print("  PASS: invalid_lead")


def test_health_endpoint():
     """Test health check endpoint."""
     from fastapi.testclient import TestClient
    
     client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
     assert "status" in data
    print("  PASS: health_endpoint")


if __name__ == "__main__":
     print("Running test suite...")
     tests = [test_lead_submission, test_invalid_lead, test_health_endpoint]
     passed = 0
     failed = 0
     for test in tests:
         try:
              test()
             passed += 1
          except Exception as e:
              print(f"  FAIL: {test.__name__} -> {e}")
              failed += 1
    
     print(f"\nResults: {passed} passed, {failed} failed")
