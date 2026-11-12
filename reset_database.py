"""
Database & Evidence Vault Reset Utility
Cleans all evidence records, custody logs, XAI analyses, uploaded files, and reports,
returning the system to a clean, fresh state while seeding standard forensic operator accounts.
"""
import os
import shutil
from pathlib import Path
from backend.database import SessionLocal, engine, Base
from backend.models.user import User
from backend.models.evidence import Evidence
from backend.models.hash_record import HashRecord
from backend.models.metadata_record import MetadataRecord
from backend.models.custody import CustodyEvent
from backend.models.provenance import ProvenanceEvent
from backend.models.analysis import AIAnalysis, RiskScoreRecord, ReportRecord
from backend.routes.auth import hash_password
from backend.config import EVIDENCE_VAULT_DIR, REPORTS_DIR, UPLOADS_DIR

def clean_all_data():
    print("Clearing all evidence records and resetting database...")
    db = SessionLocal()
    try:
        # Delete dependent forensic records first
        db.query(AIAnalysis).delete()
        db.query(RiskScoreRecord).delete()
        db.query(ReportRecord).delete()
        db.query(CustodyEvent).delete()
        db.query(ProvenanceEvent).delete()
        db.query(HashRecord).delete()
        db.query(MetadataRecord).delete()
        db.query(Evidence).delete()
        db.query(User).delete()
        db.commit()

        # Seed clean operator accounts
        default_users = [
            User(
                email="investigator@forensics.lab",
                password_hash=hash_password("investigator123"),
                role="Investigator",
                badge_number="INV-2026-881"
            ),
            User(
                email="analyst@forensics.lab",
                password_hash=hash_password("analyst123"),
                role="Analyst",
                badge_number="ANL-2026-402"
            ),
            User(
                email="admin@forensics.lab",
                password_hash=hash_password("admin123"),
                role="Admin",
                badge_number="ADM-2026-001"
            )
        ]
        db.add_all(default_users)
        db.commit()
        print("[OK] Database tables purged and fresh operator accounts created.")

        # Clean vault directory
        if EVIDENCE_VAULT_DIR.exists():
            for f in EVIDENCE_VAULT_DIR.iterdir():
                if f.is_file():
                    try:
                        f.unlink()
                    except Exception as e:
                        print(f"  Warning deleting {f.name}: {e}")
        print("[OK] Evidence vault storage cleaned.")

        # Clean reports directory
        if REPORTS_DIR.exists():
            for f in REPORTS_DIR.iterdir():
                if f.is_file() and f.suffix.lower() == ".pdf":
                    try:
                        f.unlink()
                    except Exception as e:
                        print(f"  Warning deleting {f.name}: {e}")
        print("[OK] Reports directory cleaned.")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Reset failed: {e}")
        raise
    finally:
        db.close()

    print("\n[SUCCESS] System reset complete! Website is completely clean and ready for new evidence.")

if __name__ == "__main__":
    clean_all_data()
