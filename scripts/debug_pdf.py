import pdfplumber

# Point this to one of your failing files
FILE_PATH = "data/raw/curriculum_pdfs/CS_CSST 101_1ST SEM 2025-2026.pdf"

print(f"Checking file: {FILE_PATH}")

with pdfplumber.open(FILE_PATH) as pdf:
    if len(pdf.pages) > 0:
        first_page_text = pdf.pages[0].extract_text()
        
        if first_page_text:
            print("\n✅ SUCCESS: Text found on Page 1!")
            print("--- PREVIEW ---")
            print(first_page_text[:200]) # Print first 200 characters
        else:
            print("\n❌ FAILURE: No text found. This PDF is a scanned image.")
            print("   Solution: You must use an OCR tool to convert it to text.")
    else:
        print("❌ Error: PDF appears to be empty.")