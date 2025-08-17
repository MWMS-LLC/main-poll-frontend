#!/usr/bin/env python3
"""
Script to clean up duplicate prefixes in options CSV data.
Removes duplicate A., B., C., D. prefixes from option_text.
"""

import csv
import os

def clean_option_text(text):
    """Remove duplicate prefixes like 'A. A.' -> 'A.'"""
    if not text:
        return text
    
    # Remove duplicate prefixes (e.g., "A. A." -> "A.")
    import re
    # Pattern to match duplicate prefixes: A. A., B. B., etc.
    pattern = r'^([A-Z])\.\s*\1\.\s*'
    cleaned = re.sub(pattern, r'\1. ', text)
    
    return cleaned

def clean_csv_file(input_file, output_file):
    """Clean the CSV file by removing duplicate prefixes"""
    
    cleaned_rows = []
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Keep the header
        cleaned_rows.append(reader.fieldnames)
        
        for row in reader:
            # Clean the option_text field
            if 'option_text' in row and row['option_text']:
                row['option_text'] = clean_option_text(row['option_text'])
            
            # Add the cleaned row
            cleaned_rows.append([row[field] for field in reader.fieldnames])
    
    # Write the cleaned data
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)
    
    print(f"Cleaned CSV saved to: {output_file}")

def main():
    # File paths
    input_file = "../data/options.csv"
    output_file = "../data/options_cleaned.csv"
    
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return
    
    print("Cleaning option prefixes...")
    clean_csv_file(input_file, output_file)
    
    # Show some examples of what was cleaned
    print("\nExamples of cleaned options:")
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        count = 0
        for row in reader:
            if count >= 5:  # Show first 5 examples
                break
            if 'option_text' in row and row['option_text']:
                original = row['option_text']
                cleaned = clean_option_text(original)
                if original != cleaned:
                    print(f"  '{original}' -> '{cleaned}'")
                count += 1
    
    print(f"\nCleaning complete! Check {output_file} for the cleaned data.")

if __name__ == "__main__":
    main()
