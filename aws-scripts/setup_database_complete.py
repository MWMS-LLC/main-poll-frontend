#!/usr/bin/env python3
"""
Complete AWS RDS Database Setup Script
This script creates all tables and imports CSV data for the Teen Poll application.
"""

import psycopg2
import csv
import os
from datetime import datetime

# Database connection details
DB_CONFIG = {
    'host': 'database-1.c320aqgmywbc.us-east-2.rds.amazonaws.com',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'NBem0YTOfN94yKqFSw5F',
    'connect_timeout': 10
}

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

def create_setup_tables(cursor):
    """Create the setup tables (categories, blocks, questions, options)"""
    print("📊 Creating setup tables...")
    
    # Drop existing tables
    cursor.execute('''
        DROP TABLE IF EXISTS options CASCADE;
        DROP TABLE IF EXISTS questions CASCADE;
        DROP TABLE IF EXISTS blocks CASCADE;
        DROP TABLE IF EXISTS categories CASCADE;
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE categories (
            id SERIAL PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL,
            category_text TEXT,
            day_of_week INTEGER[],
            day_of_week_text TEXT,
            description TEXT,
            category_text_long TEXT,
            version VARCHAR(20),
            uuid TEXT UNIQUE,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create blocks table
    cursor.execute('''
        CREATE TABLE blocks (
            id SERIAL PRIMARY KEY,
            category_id INTEGER REFERENCES categories(id),
            block_number INTEGER,
            block_code VARCHAR(50),
            block_text TEXT,
            version VARCHAR(20),
            uuid TEXT UNIQUE,
            category_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create questions table
    cursor.execute('''
        CREATE TABLE questions (
            id SERIAL PRIMARY KEY,
            category_id INTEGER REFERENCES categories(id),
            question_code VARCHAR(50),
            question_number INTEGER,
            question_text TEXT,
            check_box BOOLEAN DEFAULT FALSE,
            max_select INTEGER DEFAULT 1,
            block_number INTEGER,
            block_text TEXT,
            is_start_question BOOLEAN DEFAULT FALSE,
            parent_question_id INTEGER,
            color_code VARCHAR(20),
            version VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create options table
    cursor.execute('''
        CREATE TABLE options (
            id SERIAL PRIMARY KEY,
            category_id INTEGER REFERENCES categories(id),
            question_code VARCHAR(50),
            question_number INTEGER,
            question_text TEXT,
            check_box BOOLEAN DEFAULT FALSE,
            block_number INTEGER,
            block_text TEXT,
            option_select VARCHAR(50),
            option_code VARCHAR(50),
            option_text TEXT,
            response_message TEXT,
            companion_advice TEXT,
            tone_tag VARCHAR(50),
            next_question_id INTEGER,
            version VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    print("✅ Setup tables created successfully!")

def create_results_tables(cursor):
    """Create the results tables (users, responses, etc.)"""
    print("📊 Creating results tables...")
    
    # Drop existing tables
    cursor.execute('''
        DROP TABLE IF EXISTS other_responses CASCADE;
        DROP TABLE IF EXISTS checkbox_responses CASCADE;
        DROP TABLE IF EXISTS responses CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            user_uuid TEXT UNIQUE NOT NULL,
            year_of_birth INTEGER NOT NULL CHECK (year_of_birth >= 1900 AND year_of_birth <= 2024),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create responses table
    cursor.execute('''
        CREATE TABLE responses (
            id SERIAL PRIMARY KEY,
            user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
            question_code VARCHAR(50) NOT NULL,
            question_text TEXT NOT NULL,
            question_number INTEGER,
            category_id INTEGER,
            category_name VARCHAR(100) NOT NULL,
            category_text TEXT,
            option_id INTEGER,
            option_select VARCHAR(10) NOT NULL,
            option_code VARCHAR(50) NOT NULL,
            option_text TEXT NOT NULL,
            block_number INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            setup_question_code VARCHAR(50),
            setup_option_id INTEGER
        );
    ''')
    
    # Create checkbox_responses table
    cursor.execute('''
        CREATE TABLE checkbox_responses (
            id SERIAL PRIMARY KEY,
            user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
            question_code VARCHAR(50) NOT NULL,
            question_text TEXT NOT NULL,
            question_number INTEGER,
            category_id INTEGER,
            category_name VARCHAR(100) NOT NULL,
            category_text TEXT,
            option_id INTEGER,
            option_select VARCHAR(10) NOT NULL,
            option_code VARCHAR(50) NOT NULL,
            option_text TEXT NOT NULL,
            block_number INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            weight REAL DEFAULT 1.0,
            setup_question_code VARCHAR(50),
            setup_option_id INTEGER,
            UNIQUE(user_uuid, question_code, option_select, created_at)
        );
    ''')
    
    # Create other_responses table
    cursor.execute('''
        CREATE TABLE other_responses (
            id SERIAL PRIMARY KEY,
            user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
            question_code VARCHAR(50) NOT NULL,
            question_text TEXT NOT NULL,
            question_number INTEGER,
            category_id INTEGER,
            category_name VARCHAR(100) NOT NULL,
            category_text TEXT,
            block_number INTEGER,
            other_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            setup_question_code VARCHAR(50)
        );
    ''')
    
    # Create indexes
    indexes = [
        'CREATE INDEX idx_responses_user ON responses(user_uuid);',
        'CREATE INDEX idx_responses_question ON responses(question_code);',
        'CREATE INDEX idx_responses_category ON responses(category_name);',
        'CREATE INDEX idx_responses_created ON responses(created_at);',
        'CREATE INDEX idx_checkbox_responses_user ON checkbox_responses(user_uuid);',
        'CREATE INDEX idx_checkbox_responses_question ON checkbox_responses(question_code);',
        'CREATE INDEX idx_checkbox_responses_category ON checkbox_responses(category_name);',
        'CREATE INDEX idx_checkbox_responses_created ON checkbox_responses(created_at);',
        'CREATE INDEX idx_other_responses_user ON other_responses(user_uuid);',
        'CREATE INDEX idx_other_responses_question ON other_responses(question_code);',
        'CREATE INDEX idx_other_responses_category ON other_responses(category_name);',
        'CREATE INDEX idx_other_responses_created ON other_responses(created_at);',
        'CREATE INDEX idx_users_uuid ON users(user_uuid);',
        'CREATE INDEX idx_users_year ON users(year_of_birth);'
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    print("✅ Results tables created successfully!")

def import_csv_data(cursor, data_dir='data'):
    """Import CSV data into the database"""
    print("📊 Importing CSV data...")
    
    # Import categories
    print("  📁 Importing categories...")
    with open(f'{data_dir}/categories.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            day_of_week_str = clean_csv_value(row.get('day_of_week', ''))
            day_of_week_array = None
            if day_of_week_str and day_of_week_str.startswith('{') and day_of_week_str.endswith('}'):
                content = day_of_week_str[1:-1]
                day_of_week_array = [int(day.strip()) for day in content.split(',') if day.strip()]
            
            cursor.execute("""
                INSERT INTO categories (category_name, category_text, day_of_week, day_of_week_text, description, category_text_long, version, uuid, sort_order, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                clean_csv_value(row['category_name']),
                clean_csv_value(row.get('category_text', '')),
                day_of_week_array,
                clean_csv_value(row.get('day_of_week_text', '')),
                clean_csv_value(row.get('description', '')),
                clean_csv_value(row.get('category_text_long', '')),
                clean_csv_value(row.get('version', '')),
                clean_csv_value(row.get('uuid', '')),
                int(row.get('sort_order', 0)),
                datetime.now()
            ))
    print("    ✅ Categories imported")
    
    # Import blocks
    print("  📁 Importing blocks...")
    with open(f'{data_dir}/blocks.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO blocks (category_id, block_number, block_code, block_text, version, uuid, category_name, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
    with open(f'{data_dir}/questions.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO questions (category_id, question_code, question_number, question_text, check_box, max_select, block_number, block_text, is_start_question, parent_question_id, color_code, version, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    with open(f'{data_dir}/options.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO options (category_id, question_code, question_number, question_text, check_box, block_number, block_text, option_select, option_code, option_text, response_message, companion_advice, tone_tag, next_question_id, version, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

def show_database_summary(cursor):
    """Show summary of database contents"""
    print("\n📊 Database Summary:")
    
    tables = ['categories', 'blocks', 'questions', 'options', 'users', 'responses', 'checkbox_responses', 'other_responses']
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table.capitalize()}: {count}")
        except:
            print(f"  {table.capitalize()}: 0 (table not found)")

def main():
    """Main function to set up the complete database"""
    print("🚀 Starting complete database setup...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Connected to AWS RDS PostgreSQL database")
        
        # Create all tables
        create_setup_tables(cursor)
        create_results_tables(cursor)
        
        # Import CSV data
        import_csv_data(cursor)
        
        # Commit all changes
        conn.commit()
        print("✅ All data imported successfully!")
        
        # Show summary
        show_database_summary(cursor)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
