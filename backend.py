# backend.py
import cv2
import pytesseract
import spacy
import re
import numpy as np
from ultralytics import YOLO

# -----------------------------
# Load SpaCy & YOLO Models
# -----------------------------
nlp = spacy.load("en_core_web_sm")
yolo_model = YOLO("runs/detect/train2/weights/best.pt")  # your trained YOLO model for signatures

# -----------------------------
# Detect PII with OCR + NLP
# -----------------------------
def detect_pii_word(word):
    """Detect PII category for a single word (Name / Date)."""
    date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|" \
                   r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b|" \
                   r"\d{4})"
    if re.search(date_pattern, word):
        return "DATE"

    # Name detection with SpaCy
    doc = nlp(word)
    if any(ent.label_ == "PERSON" for ent in doc.ents):
        return "NAME"

    return None


# -----------------------------
# Redaction Function
# -----------------------------
def redact_image(image, pad=10):
    """Redact Names, Dates (OCR+NLP) and Signatures (YOLO)."""
    redacted = image.copy()

    # Step 1: OCR detection (Names, Dates)
    results = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    n_boxes = len(results["level"])

    for i in range(n_boxes):
        word = results["text"][i].strip()
        if not word:
            continue

        pii_type = detect_pii_word(word)

        if pii_type in ["NAME", "DATE"]:
            x, y, w, h = (
                results["left"][i],
                results["top"][i],
                results["width"][i],
                results["height"][i],
            )
            cv2.rectangle(redacted, (x - pad, y - pad), (x + w + pad, y + h + pad),
                          (0, 0, 0), -1)

    # Step 2: YOLO detection (Signature)
    yolo_results = yolo_model.predict(image, conf=0.4)
    for r in yolo_results:
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box.tolist())
            cv2.rectangle(redacted, (x1 - pad, y1 - pad), (x2 + pad, y2 + pad),
                          (0, 0, 0), -1)

    return redacted
