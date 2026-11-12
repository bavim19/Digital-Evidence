import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import docx
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_samples():
    sample_dir = Path("sample_evidence")
    sample_dir.mkdir(parents=True, exist_ok=True)

    # 1. Sample JPEG Image
    img_path = sample_dir / "sample_crime_scene_photo.jpg"
    img = Image.new("RGB", (640, 480), color=(28, 45, 78))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 600, 440], outline=(72, 202, 228), width=3)
    draw.text((60, 60), "DIGITAL EVIDENCE VAULT - SEIZED ASSET #8812", fill=(241, 245, 249))
    draw.text((60, 90), "Location: Target Drive Extraction | Date: 2026-03-15", fill=(148, 163, 184))
    img.save(img_path, "JPEG", quality=95)

    # 2. Sample Log / Text File
    log_path = sample_dir / "financial_transfer_audit_log.txt"
    log_content = """# SYSTEM AUDIT LOG - TRANSACTION SUBSYSTEM
2026-03-15 08:22:11 [AUTH] Operator Agent Miller authenticated from terminal SEC-01
2026-03-15 08:30:45 [TX] Wire transfer request initiated: TXN-882910 ($250,000.00 USD)
2026-03-15 08:35:10 [VALIDATION] Multi-factor cryptographic verification verified
2026-03-15 08:40:00 [VAULT] Audit checksum snapshot archived to secure ledger
2026-03-15 08:45:22 [DISCONNECT] Session terminated normally
"""
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(log_content)

    # 3. Sample Word Document
    doc_path = sample_dir / "forensic_incident_case_notes.docx"
    doc = docx.Document()
    doc.add_heading("Digital Forensics Incident Case Notes", level=1)
    doc.add_paragraph("Case Reference: CASE-2026-X01 | Lead Examiner: Agent J. Miller")
    doc.add_paragraph("Target device storage image acquired via write-blocker forensic hardware interface.")
    doc.save(doc_path)

    # 4. Sample PDF Document
    pdf_path = sample_dir / "confidential_custody_report.pdf"
    pdf_doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>CONFIDENTIAL FORENSIC INTAKE RECORD</b>", styles["Heading1"]),
        Spacer(1, 10),
        Paragraph("Item Seized: High-capacity NVMe drive from primary server chassis.", styles["Normal"]),
        Paragraph("Integrity Baseline: SHA-256 fingerprint generated at point of seizure.", styles["Normal"])
    ]
    pdf_doc.build(story)

    print(f"Generated 4 realistic test digital evidence files in {sample_dir.resolve()}")

if __name__ == "__main__":
    generate_samples()
