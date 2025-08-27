#!/usr/bin/env python3
"""
Import script for Render database - imports categories, blocks, questions, and options
"""

import psycopg2
import csv
import os
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

def import_to_render():
    """Import CSV data to Render database"""
    
    try:
        # Connect to Render database
        print("🔌 Connecting to Render database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connected to Render database")
        
        # First, let's check what tables exist
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name IN ('categories', 'blocks', 'questions', 'options')
            ORDER BY table_name
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Existing tables: {existing_tables}")
        
        # Create tables if they don't exist
        if 'categories' not in existing_tables:
            print("📋 Creating categories table...")
            cursor.execute("""
                CREATE TABLE categories (
                    id SERIAL PRIMARY KEY,
                    category_name VARCHAR(100) NOT NULL,
                    category_text TEXT,
                    sort_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        if 'blocks' not in existing_tables:
            print("📋 Creating blocks table...")
            cursor.execute("""
                CREATE TABLE blocks (
                    id SERIAL PRIMARY KEY,
                    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
                    block_number INTEGER NOT NULL,
                    block_code VARCHAR(50) UNIQUE NOT NULL,
                    block_text TEXT NOT NULL,
                    version VARCHAR(20),
                    uuid TEXT UNIQUE,
                    category_name VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_block_per_category UNIQUE (category_id, block_number)
                )
            """)
        
        if 'questions' not in existing_tables:
            print("📋 Creating questions table...")
            cursor.execute("""
                CREATE TABLE questions (
                    id SERIAL PRIMARY KEY,
                    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
                    question_code VARCHAR(50) UNIQUE NOT NULL,
                    question_number INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    check_box BOOLEAN DEFAULT FALSE,
                    max_select INTEGER DEFAULT 1,
                    block_number INTEGER NOT NULL,
                    block_text TEXT,
                    is_start_question BOOLEAN DEFAULT FALSE,
                    parent_question_id INTEGER,
                    color_code TEXT,
                    version VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_question_per_block UNIQUE (category_id, block_number, question_number)
                )
            """)
        
        if 'options' not in existing_tables:
            print("📋 Creating options table...")
            cursor.execute("""
                CREATE TABLE options (
                    id SERIAL PRIMARY KEY,
                    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
                    question_code VARCHAR(50) NOT NULL,
                    question_number INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    check_box BOOLEAN DEFAULT FALSE,
                    block_number INTEGER NOT NULL,
                    block_text TEXT NOT NULL,
                    option_select VARCHAR(10) NOT NULL,
                    option_code VARCHAR(50) NOT NULL,
                    option_text TEXT NOT NULL,
                    response_message TEXT,
                    companion_advice TEXT,
                    tone_tag TEXT,
                    next_question_id INTEGER,
                    version VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_option_per_question UNIQUE (question_code, option_select)
                )
            """)
        
        conn.commit()
        print("✅ Tables created/verified")
        
        # Import data
        print("📊 Importing CSV data...")
        
        # Import categories
        print("  📁 Importing categories...")
        with open('../data/categories.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO categories (category_name, category_text, sort_order, created_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (category_name) DO NOTHING
                """, (
                    clean_csv_value(row['category_name']),
                    clean_csv_value(row.get('category_text', '')),
                    int(row.get('sort_order', 0)),
                    datetime.now()
                ))
        print("    ✅ Categories imported")
        
        # Import blocks
        print("  📁 Importing blocks...")
        with open('../data/blocks.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO blocks (category_id, block_number, block_code, block_text, version, uuid, category_name, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (block_code) DO NOTHING
                """, (
                    int(row['category_id']),
                    int(row['block_number']),
                    clean_csv_value(row['block_code']),
                    clean_csv_value(row['block_text']),
                    clean_csv_value(row.get('version', '')),
                    clean_csv_value(row.get('uuid', '')),
                    clean_csv_value(row.get('category_name', '')),
                    datetime.now()
                ))
        print("    ✅ Blocks imported")
        
        # Import questions
        print("  📁 Importing questions...")
        with open('../data/questions.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO questions (category_id, question_code, question_number, question_text, check_box, max_select, block_number, block_text, is_start_question, parent_question_id, color_code, version, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (question_code) DO NOTHING
                """, (
                    int(row['category_id']),
                    clean_csv_value(row['question_code']),
                    int(row['question_number']),
                    clean_csv_value(row['question_text']),
                    row.get('check_box', 'false').lower() == 'true',
                    int(row.get('max_select', 10)) if row.get('max_select') and row.get('max_select').strip() and row.get('max_select') != '' else (10 if row.get('check_box', 'false').lower() == 'true' else 1),
                    int(row['block_number']),
                    clean_csv_value(row.get('block_text', '')),
                    row.get('is_start_question', 'false').lower() == 'true',
                    int(row['parent_question_id']) if row.get('parent_question_id') and row.get('parent_question_id').strip() else None,
                    clean_csv_value(row.get('color_code', '')),
                    clean_csv_value(row.get('version', '')),
                    datetime.now()
                ))
        print("    ✅ Questions imported")
        
        # Import options
        print("  📁 Importing options...")
        with open('../data/options.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO options (category_id, question_code, question_number, question_text, check_box, block_number, block_text, option_select, option_code, option_text, response_message, companion_advice, tone_tag, next_question_id, version, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (question_code, option_select) DO NOTHING
                """, (
                    int(row['category_id']),
                    clean_csv_value(row['question_code']),
                    int(row['question_number']),
                    clean_csv_value(row['question_text']),
                    row.get('check_box', 'false').lower() == 'true',
                    int(row['block_number']),
                    clean_csv_value(row['block_text']),
                    clean_csv_value(row['option_select']),
                    clean_csv_value(row['option_code']),
                    clean_csv_value(row['option_text']),
                    clean_csv_value(row.get('response_message', '')),
                    clean_csv_value(row.get('companion_advice', '')),
                    clean_csv_value(row.get('tone_tag', '')),
                    int(row['next_question_id']) if row.get('next_question_id') and row.get('next_question_id').strip() else None,
                    clean_csv_value(row.get('version', '')),
                    datetime.now()
                ))
        print("    ✅ Options imported")
        
        # Commit all changes
        conn.commit()
        print("🎉 All data imported successfully!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM blocks")
        blocks_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM questions")
        questions_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM options")
        options_count = cursor.fetchone()[0]
        
        print(f"\n📊 Database Summary:")
        print(f"  Categories: {categories_count}")
        print(f"  Blocks: {blocks_count}")
        print(f"  Questions: {questions_count}")
        print(f"  Options: {options_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import_to_render()
