#!/usr/bin/env python3
"""
Test script to upload just a few responses and identify the issue.
"""

import os
import csv
import pg8000
from urllib.parse import urlparse

def get_db_connection():
    """Get database connection"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL environment variable is not set!")
    
    parsed = urlparse(database_url)
    conn = pg8000.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        ssl_context=True
    )
    return conn

def test_single_upload():
    """Test uploading just one response"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("🧪 Testing single response upload...")
    
    # Read first row from CSV
    responses_file = 'fake_users_data/fake_responses.csv'
    with open(responses_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        first_row = next(reader)
    
    print(f"📝 First row data:")
    print(f"   Question: {first_row['question_code']}")
    print(f"   User: {first_row['user_uuid'][:8]}...")
    print(f"   Option: {first_row['option_select']}")
    
    try:
        # Get question_number and option_id from database
        print("🔍 Looking up question_number...")
        cursor.execute("SELECT question_number FROM questions WHERE question_code = %s", (first_row['question_code'],))
        question_number_result = cursor.fetchone()
        question_number = question_number_result[0] if question_number_result else None
        print(f"   Question number: {question_number}")
        
        print("🔍 Looking up option_id...")
        cursor.execute("SELECT id FROM options WHERE question_code = %s AND option_select = %s", (first_row['question_code'], first_row['option_select']))
        option_id_result = cursor.fetchone()
        option_id = option_id_result[0] if option_id_result else None
        print(f"   Option ID: {option_id}")
        
        print("📤 Inserting response...")
        cursor.execute("""
            INSERT INTO responses (
                user_uuid, question_code, question_text, question_number,
                category_id, category_name, option_id, option_select,
                option_code, option_text, block_number, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            first_row['user_uuid'], first_row['question_code'], first_row['question_text'],
            question_number, int(first_row['category_id']), first_row['category_name'],
            option_id, first_row['option_select'], first_row['option_code'],
            first_row['option_text'], int(first_row['block_number']), first_row['created_at']
        ))
        
        conn.commit()
        print("✅ Single response uploaded successfully!")
        
        # Check new count
        cursor.execute("SELECT COUNT(*) FROM responses")
        new_count = cursor.fetchone()[0]
        print(f"📊 New response count: {new_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
    
    cursor.close()
    conn.close()

def main():
    """Main test function"""
    print("🚀 Starting upload test...")
    test_single_upload()

if __name__ == "__main__":
    main()
