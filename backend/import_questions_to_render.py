#!/usr/bin/env python3
"""
Import only questions data to existing Render database
"""

import psycopg2
import csv
from datetime import datetime

# Render database connection
DATABASE_URL = "postgresql://mwms_teen_poll_user:CTF1UxZpzk4E2vhevF5GE3NEAuFBxPiF@dpg-d2gfof75r7bs73f1uc0g-a.oregon-postgres.render.com/mwms_teen_poll"

def clean_csv_value(value):
    """Clean CSV values and handle multi-line content"""
    if value is None:
        return None
    # Remove BOM and strip whitespace
    value = str(value).strip().replace('\ufeff', '')
    # Handle multi-line content
    if '\n' in value:
        value = value.replace('\n', ' ')
    return value

def import_questions_to_render():
    """Import only questions data to existing Render database"""
    
    try:
        # Connect to Render database
        print("🔌 Connecting to Render database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connected to Render database")
        
        # Check if questions table exists and has data
        cursor.execute("SELECT COUNT(*) FROM questions")
        existing_count = cursor.fetchone()[0]
        print(f"📋 Questions table exists with {existing_count} records")
        
        # Clear existing questions data (optional - comment out if you want to keep existing)
        print("🗑️ Clearing existing questions data...")
        cursor.execute("DELETE FROM questions")
        print("    ✅ Existing questions cleared")
        
        # Import questions from CSV
        print("📁 Importing questions from CSV...")
        with open('../data/questions.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            imported_count = 0
            for row in reader:
                # Skip completely empty rows (where all values are empty or whitespace)
                if all(not value or str(value).strip() == '' for value in row.values()):
                    print(f"    ⚠️ Skipping empty row {imported_count + 1}")
                    continue
                
                # Skip rows with empty category_id
                if not row['category_id'] or row['category_id'].strip() == '':
                    print(f"    ⚠️ Skipping row {imported_count + 1}: empty category_id")
                    continue
                
                cursor.execute("""
                    INSERT INTO questions (category_id, question_code, question_number, question_text, check_box, max_select, block_number, block_text, is_start_question, parent_question_id, color_code, version, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(row['category_id']),
                    clean_csv_value(row['question_code']),
                    int(row['question_number']),
                    clean_csv_value(row['question_text']),
                    row.get('check_box', 'false').lower() == 'true',
                    int(row.get('max_select', 10)) if row.get('max_select') and row.get('max_select').strip() and row.get('max_select') != '' else (10 if row.get('max_select', 'false').lower() == 'true' else 1),
                    int(row['block_number']),
                    clean_csv_value(row.get('block_text', '')),
                    row.get('is_start_question', 'false').lower() == 'true',
                    int(row['parent_question_id']) if row.get('parent_question_id') and row.get('parent_question_id').strip() else None,
                    clean_csv_value(row.get('color_code', '')),
                    clean_csv_value(row.get('version', '')),
                    datetime.now()
                ))
                imported_count += 1
                
                # Show progress every 100 questions
                if imported_count % 100 == 0:
                    print(f"    📝 Imported {imported_count} questions...")
        
        print(f"    ✅ {imported_count} questions imported")
        
        # Commit changes
        conn.commit()
        print("🎉 Questions import completed successfully!")
        
        # Show final count
        cursor.execute("SELECT COUNT(*) FROM questions")
        final_count = cursor.fetchone()[0]
        print(f"📊 Final questions count: {final_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import_questions_to_render()
