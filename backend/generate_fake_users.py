import random
import csv
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_fake_users_sql():
    """Generate SQL file with fake users and responses"""
    
    # Set random seed for deterministic generation
    random.seed(42)
    
    # Generate 20 fake users
    fake_users = []
    for i in range(20):
        # Generate random year of birth between 2007-2012
        year_of_birth = random.randint(2007, 2012)
        
        # Generate deterministic UUID (same every time)
        user_uuid = f"fake-user-{i+1:02d}-{random.randint(1000, 9999)}"
        
        fake_users.append({
            'user_uuid': user_uuid,
            'year_of_birth': year_of_birth,
            'created_at': datetime.now() - timedelta(days=random.randint(0, 30))
        })
    
    # Read questions and options from CSV files
    questions = []
    options = []
    
    try:
        # Read questions
        with open('../data/questions.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                questions.append({
                    'question_code': row['question_code'],
                    'check_box': row.get('check_box', 'false').lower() == 'true',
                    'max_select': int(row.get('max_select', 3)) if row.get('max_select') and row.get('max_select').strip() and row.get('max_select') != '' else (3 if row.get('check_box', 'false').lower() == 'true' else 1)
                })
        
        # Read options
        with open('../data/options.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                options.append({
                    'question_code': row['question_code'],
                    'option_select': row['option_select'],
                    'option_text': row['option_text']
                })
        
        # Read categories for denormalization
        categories = {}
        with open('../data/categories.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                categories[int(row['id'])] = row['category_name']
        
        # Read blocks for denormalization
        blocks = {}
        with open('../data/blocks.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                blocks[row['block_code']] = {
                    'block_number': int(row['block_number']),
                    'category_id': int(row['category_id']),
                    'category_name': categories.get(int(row['category_id']), 'Unknown')
                }
        
    except FileNotFoundError as e:
        print(f"❌ CSV file not found: {e}")
        return
    
    # Generate SQL file
    sql_content = []
    sql_content.append("-- Fake Users and Responses SQL File")
    sql_content.append("-- Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_content.append("-- This file contains 20 fake users with responses to all questions")
    sql_content.append("")
    
    # Add users
    sql_content.append("-- Insert fake users")
    for user in fake_users:
        sql_content.append(f"INSERT INTO users (user_uuid, year_of_birth, created_at) VALUES ('{user['user_uuid']}', {user['year_of_birth']}, '{user['created_at']}');")
    
    sql_content.append("")
    
    # Add responses for each user and question
    sql_content.append("-- Insert responses for each user")
    
    for user in fake_users:
        for question in questions:
            if question['check_box']:
                # Checkbox question - select 1 to max_select options
                num_selections = random.randint(1, min(question['max_select'], 3))  # Cap at 3 for demo
                selected_options = random.sample([opt for opt in options if opt['question_code'] == question['question_code']], num_selections)
                
                for option in selected_options:
                    weight = 1.0 / len(selected_options)
                    sql_content.append(f"INSERT INTO checkbox_responses (user_uuid, question_code, question_text, question_number, category_id, category_name, option_id, option_select, option_code, option_text, block_number, weight, created_at) VALUES ('{user['user_uuid']}', '{question['question_code']}', 'Question Text', 1, 1, 'Category', 1, '{option['option_select']}', '{option['option_select']}', '{option['option_text']}', 1, {weight}, '{datetime.now()}');")
            else:
                # Single choice question
                option = random.choice([opt for opt in options if opt['question_code'] == question['question_code']])
                sql_content.append(f"INSERT INTO responses (user_uuid, question_code, question_text, question_number, category_id, category_name, option_id, option_select, option_code, option_text, block_number, created_at) VALUES ('{user['user_uuid']}', '{question['question_code']}', 'Question Text', 1, 1, 'Category', 1, '{option['option_select']}', '{option['option_select']}', '{option['option_text']}', 1, '{datetime.now()}');")
    
    # Write SQL file
    sql_filename = f"fake_users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    with open(sql_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_content))
    
    print(f"✅ SQL file generated: {sql_filename}")
    print(f"📊 Contains {len(fake_users)} fake users with responses to {len(questions)} questions")
    print(f"💡 You can now run this SQL file in your database to populate it with test data")

if __name__ == "__main__":
    generate_fake_users_sql()
