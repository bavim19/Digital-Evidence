import os
import httpx
from pathlib import Path

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8005")
SAMPLE_DIR = Path("sample_evidence")

def seed_demo_data():
    print("Seeding realistic forensic evidence cases for demonstration...")
    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    # 1. Login as Investigator
    login_resp = client.post("/api/auth/login", json={
        "email": "investigator@forensics.lab",
        "password": "investigator123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[OK] Authenticated as Lead Investigator (Agent J. Miller)")

    # Sample Items to Register & Verify
    items = [
        {
            "file": SAMPLE_DIR / "sample_crime_scene_photo.jpg",
            "case": "CASE-2026-X01",
            "desc": "Primary crime scene digital photo seized from victim workstation.",
            "device": "Target Camera / Workstation (Drive D:)",
            "tamper": None # Clean
        },
        {
            "file": SAMPLE_DIR / "financial_transfer_audit_log.txt",
            "case": "CASE-2026-X02",
            "desc": "Financial server wire transfer transaction audit log.",
            "device": "Core Banking Server TX-09",
            "tamper": "BYTE_FLIP" # Bitstream tampered
        },
        {
            "file": SAMPLE_DIR / "forensic_incident_case_notes.docx",
            "case": "CASE-2026-X03",
            "desc": "Confidential investigative incident interview notes.",
            "device": "Field Laptop NVMe",
            "tamper": "METADATA_ALTER" # Software tag injected
        },
        {
            "file": SAMPLE_DIR / "confidential_custody_report.pdf",
            "case": "CASE-2026-X04",
            "desc": "Official digital evidence intake and seizure affidavit.",
            "device": "Secure Vault Terminal",
            "tamper": "CUSTODY_GAP" # Custody gap injected
        }
    ]

    for itm in items:
        if not itm["file"].exists():
            continue
            
        with open(itm["file"], "rb") as f:
            upload_resp = client.post(
                "/api/evidence/upload",
                files={"file": (itm["file"].name, f, "application/octet-stream")},
                data={
                    "case_number": itm["case"],
                    "description": itm["desc"],
                    "source_device": itm["device"]
                },
                headers=headers
            )
        
        ev_data = upload_resp.json()["evidence"]
        ev_id = ev_data["evidence_id"]
        print(f"[OK] Registered: {ev_id} ({itm['file'].name}) - Baseline SHA-256: {ev_data['original_hash_sha256'][:16]}...")

        # Add secondary custody events for realism
        client.post(
            f"/api/evidence/{ev_id}/custody",
            data={
                "action": "Transferred to Lab",
                "previous_holder": "Agent J. Miller",
                "new_holder": "Dr. S. Chen",
                "location": "Forensics Center Room 102",
                "notes": "Delivered for deep-factor integrity audit"
            },
            headers=headers
        )

        # Inject controlled tamper if specified for demo case
        if itm["tamper"]:
            client.post(
                f"/api/evidence/{ev_id}/simulate-tamper",
                data={"tamper_type": itm["tamper"]},
                headers=headers
            )
            print(f"  [TAMPER] Injected demo anomaly scenario: {itm['tamper']}")

        # Run verification & XAI
        verify_resp = client.post(f"/api/evidence/{ev_id}/verify", headers=headers)
        v_res = verify_resp.json()
        score = v_res["operational_risk_score"]["score"]
        level = v_res["operational_risk_score"]["risk_level"]
        print(f"  [OK] Verified: Risk Score = {score:.1f}/100 [{level} RISK] - AI: {v_res['ai_anomaly_detection']['prediction_label']}")

        # Generate official PDF report
        client.post(f"/api/evidence/{ev_id}/report", headers=headers)
        print(f"  [OK] Generated PDF Verification Report for {ev_id}")

    print("\nDemonstration dataset seeded successfully! Dashboard and all charts are live.")

if __name__ == "__main__":
    seed_demo_data()
