"""Database initialization for CLG Vermögenerschutz system.

Creates SQLite DB with WAL mode and PRAGMA optimizations, then seeds data.

Run: python init_db.py
"""

import os
from sqlalchemy import create_engine, text

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "clg_vermoegenschutz.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"


def initialize_database():
    print(f"Initializing database at: {DB_PATH}")
    
     # Import models and create engine/session all in one place
    from app.models import ContentSections, Users, Webhooks,         WebhookEvents, Leads, AuditLog, ContactAttempts
    from sqlalchemy.orm import Session
    from sqlalchemy.dialects.sqlite import JSON
    
      # Create engine FIRST
    engine = create_engine(DATABASE_URL)
    
       # Import Base and create tables BEFORE any operations
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    print("[DB] All 7 tables created!")
    
        # Now set WAL mode via the engine's raw connection
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL"))
        print("[OK] WAL mode enabled")
        conn.execute(text("PRAGMA synchronous=NORMAL"))
        print("[OK] Synchronous NORMAL set")
        conn.commit()

       # Create session for seeding (uses SAME engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
       # Seed initial content sections  
    existing = session.query(ContentSections).count()
    if existing == 0:
        print("[SEED] Creating default content sections...")
        for item in [
              {"section_key": "hero_main", "section_name": "Hero Main",
               "content_type": "heading",
               "field_data": {"text": "Vermögenerschutz durch UK CLG"},
               "order_index": 1},
          ]:
            session.add(ContentSections(**item))
        print("[OK] Seed data created")
    
    session.commit()
    session.close()
    
    print("")
    print("=== Database initialization complete! ===")


from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    initialize_database()
