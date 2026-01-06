import pdfplumber
import spacy
from spacy.matcher import PhraseMatcher
import json
import glob
import os
import sys
from tqdm import tqdm

def clean_text(text):
    """
    Cleans extracted text by removing noise specific to LSPU documents.
    Removes lines containing keys like 'LSPU-ACAD-SF', dates, or other footer noise.
    """
    if not text:
        return ""
        
    lines = text.split('\n')
    cleaned_lines = []
    
    # Define noise indicators (case-insensitive checks can be added if needed)
    noise_markers = ["LSPU-ACAD-SF", "Rev 1", "Rev 2", "Rev.", "Effectivity Date"]
    
    for line in lines:
        # Check for noise markers
        is_noisy = any(marker in line for marker in noise_markers)
        
        # We can also filter out very short lines or just page numbers if needed
        # For now, we follow the specific requirement to remove LSPU specific markers
        if not is_noisy:
            cleaned_lines.append(line)
            
    return "\n".join(cleaned_lines)

def main():
    # Paths
    skills_path = os.path.join("data", "processed", "skills_taxonomy.json")
    # PDFs are expected in data/raw/curriculum_pdfs/
    pdf_dir = os.path.join("data", "raw", "curriculum_pdfs_ocr")
    output_path = os.path.join("data", "processed", "curriculum_data.json")

    # 1. Load Skill Dictionary
    print(f"Loading skills from {skills_path}...")
    if not os.path.exists(skills_path):
        print("Error: Skills taxonomy file not found.")
        sys.exit(1)
        
    with open(skills_path, 'r') as f:
        skills_list = json.load(f)

    # 2. Setup NLP
    print("Loading spaCy model (en_core_web_sm)...")
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Error: en_core_web_sm model not found. Run 'python -m spacy download en_core_web_sm'")
        sys.exit(1)

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    # Create patterns from the skill list (efficiently)
    # We use nlp.make_doc because we just need simple tokenization for the patterns
    patterns = [nlp.make_doc(text) for text in skills_list]
    matcher.add("SKILLS", patterns)
    
    print(f"PhraseMatcher initialized with {len(skills_list)} patterns.")

    # 3. Batch Process PDFs
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"Warning: No PDF files found in {pdf_dir}")
        # We proceed anyway to generate an empty JSON or just exit? 
        # Requirement says "scan 43... files", if missing we should just warn.
    else:
        print(f"Found {len(pdf_files)} PDF files to process.")

    results = {}

    # Loop with progress bar
    for pdf_file in tqdm(pdf_files, desc="Scanning PDFs", unit="file"):
        filename = os.path.basename(pdf_file)
        file_text = ""
        found_skills = set()

        try:
            # 4. Extract & Clean
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        cleaned = clean_text(text)
                        file_text += cleaned + "\n"
            
            # 5. Match Skills
            # We process the text with nlp() to get a Doc, then match
            # For very large docs, we might want to split, but curriculum files are usually manageable
            doc = nlp(file_text)
            matches = matcher(doc)
            
            for match_id, start, end in matches:
                span = doc[start:end]
                # Store the actual text found (or we could store the canonical pattern from taxonomy if valid)
                # Using span.text preserves how it appeared, but we might want the standardized version.
                # Since we used attr="LOWER" for matching, span.text gives the text from the doc.
                # To map back to the 'canonical' skill name is harder with PhraseMatcher unless we map it back.
                # However, usually for skills, exact match (case-insensitive) is fine. 
                # Let's standardize by Title Case or just keep the span text if it looks good.
                # The user requirement: "Store unique found skills". 
                # Let's clean it up slightly to match the taxonomy style if possible, 
                # but simple string extraction is usually required.
                found_skills.add(span.text)

        except Exception as e:
            # Error Handling: Warning but do not stop
            print(f"\nError processing {filename}: {e}")
            continue

        results[filename] = sorted(list(found_skills))

    # 6. Save Results
    # ensure processed dir exists (already should)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\nProcessing complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()
