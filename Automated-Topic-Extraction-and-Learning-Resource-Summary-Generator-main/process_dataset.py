import os

import pandas as pd
from src.file_loader import load_file
from src.preprocessor import TextPreprocessor

RAW_DATA_DIR = "data/raw_lectures"
PROCESSED_DATA_DIR = "data/processed"
OUTPUT_FILE = "cleaned_dataset.csv"

def main():
    if not os.path.exists(RAW_DATA_DIR):
        print(f"Error: Directory '{RAW_DATA_DIR}' not found.")
        print("Please create it and put your PDF/PPTX files inside.")
        return

    if not os.path.exists(PROCESSED_DATA_DIR):
        os.makedirs(PROCESSED_DATA_DIR)

    processor = TextPreprocessor()
    data_records = []

    print(f"--- Scanning {RAW_DATA_DIR} ---")

    for filename in os.listdir(RAW_DATA_DIR):
        file_path = os.path.join(RAW_DATA_DIR, filename)

        if not os.path.isfile(file_path):
            continue

        print(f"Processing: {filename}...")

        raw_text = load_file(file_path)

        if raw_text:
            cleaned_text = processor.clean_and_process(raw_text)
            data_records.append({
                "filename": filename,
                "raw_text_length": len(raw_text),
                "cleaned_text": cleaned_text
            })
        else:
            print("  -> Skipped (Empty or unsupported format)")

    if data_records:
        df = pd.DataFrame(data_records)
        output_path = os.path.join(PROCESSED_DATA_DIR, OUTPUT_FILE)
        df.to_csv(output_path, index=False)
        print(f"\nSuccess! Processed {len(df)} files.")
        print(f"Saved cleaned data to: {output_path}")
        print("Preview of cleaned data:")
        print(df[['filename', 'cleaned_text']].head())
    else:
        print("\nNo valid files found to process.")

if __name__ == "__main__":
    main()
