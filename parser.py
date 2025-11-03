import pdfplumber, re, os, pandas as pd
from dateutil import parser as dateparser
from tqdm import tqdm
import pytesseract
from pdf2image import convert_from_path

# -----------------------------
# PDF Text Extractor
# -----------------------------
def extract_text_from_pdf(path):
    try:
        with pdfplumber.open(path) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
            return "\n".join(pages)
    except Exception:
        return None

# -----------------------------
# OCR Extractor (fallback)
# -----------------------------
def ocr_pdf(path):
    try:
        images = convert_from_path(path, dpi=200)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text
    except Exception:
        return ""

# -----------------------------
# Patterns for key data fields
# -----------------------------
PATTERNS = {
    "card_last4": r"(?:XXXX|xxxx|x{4}|\*)(\d{4})",
    "billing_cycle": r"Billing Period[:\s]*(.*?\d{4})",
    "due_date": r"Due Date[:\s]*(.*?\d{4})",
    "total_due": r"Total Amount Due[:\s]*₹?([0-9,]+\.\d+|[0-9,]+)",
    "variant": r"(Platinum|Signature|Prime|Millennia|Regalia|Infinia|Titanium|Coral)"
}

SUPPORTED_BANKS = ["HDFC", "Axis", "SBI", "ICICI", "HSBC"]

# -----------------------------
# Extract fields from text
# -----------------------------
def extract_fields(text):
    data = {}
    for label, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        data[label] = match.group(1).strip() if match else "NOT FOUND"

    # Normalize dates
    for date_key in ["billing_cycle", "due_date"]:
        try:
            data[date_key] = str(dateparser.parse(data[date_key]).date())
        except Exception:
            pass

    return data

# -----------------------------
# Parse Folder of PDFs
# -----------------------------
def parse_pdfs(folder, output_file="results.csv"):
    rows = []

    for file in tqdm(os.listdir(folder)):
        if file.lower().endswith(".pdf"):
            path = os.path.join(folder, file)

            text = extract_text_from_pdf(path)
            if not text or len(text.strip()) < 50:
                text = ocr_pdf(path)

            result = extract_fields(text)
            result["file"] = file
            rows.append(result)

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    print(f"\nDone. Results saved to: {output_file}")

# -----------------------------
# CLI Handler
# -----------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Folder containing PDF statements")
    parser.add_argument("--output", default="results.csv", help="Output CSV file name")
    args = parser.parse_args()

    parse_pdfs(args.input, args.output)
