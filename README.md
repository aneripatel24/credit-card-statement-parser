Credit Card Statement Parser (India)

This project extracts key information from Indian credit card PDF statements. It supports both digital PDFs and scanned image-based statements using OCR, ensuring reliable parsing across bank formats.

Supported Banks

HDFC Bank

ICICI Bank

Axis Bank

State Bank of India (SBI)

HSBC

Extracted Data Fields

Last 4 digits of card

Card variant

Billing cycle

Payment due date

Total amount due

Technologies Used

Python

pdfplumber (PDF text extraction)

pytesseract + pdf2image (OCR for scanned PDFs)

pandas (structured output)

dateutil (date parsing)

Regular Expressions (data extraction)

Features

Works with real bank statement formats

OCR fallback for scanned statements

Regex-based field extraction and validation

Batch processing for multiple statements

Exports parsed data into CSV format

Folder Structure
credit-card-parser/
 ├── parser.py
 ├── sample_statements/
 ├── results.csv
 └── README.md

Usage

Run the parser on a folder of PDF statements:

python parser.py --input sample_statements --output results.csv

Output

A CSV file containing:

file	last4	variant	billing_cycle	due_date	total_due
Privacy Note

This tool is for personal finance automation and learning. Do not upload or share personal credit card statements publicly.

Future Enhancements

Bank auto-detection

Web UI / dashboard

Spend categorization

Excel / Google Sheets export
