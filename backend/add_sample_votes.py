#!/usr/bin/env python3
"""
Script to add sample votes to all questions to prevent blank pages on first votes.
This ensures every question has some initial data to display.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import random

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres@localhost:5432/teen_poll')

def get_db_connection():
    """Get a database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

def execute_query(query, params=None, fetch=True):
    """Execute a database query"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            return [dict(row) for row in result]
        else:
            conn.commit()
            return cursor.rowcount
            
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Database operation failed: {e}")
        raise
    finally:
        if conn:
            conn.close()

def add_sample_votes():
    """Add sample votes to all questions"""
    
    # Get all questions
    questions_query = "SELECT question_code, check_box FROM questions ORDER BY question_code"
    questions = execute_query(questions_query)
    
    print(f"Found {len(questions)} questions to process")
    
    # Create sample users for sample votes
    sample_users = [
        "sample-user-001",
        "sample-user-002", 
        "sample-user-003",
        "sample-user-004",
        "sample-user-005"
    ]
    
    # Create sample users in the users table first
    print("Creating sample users...")
    for user_uuid in sample_users:
        try:
            # Check if user already exists
            check_query = "SELECT COUNT(*) FROM users WHERE user_uuid = %s"
            user_exists = execute_query(check_query, (user_uuid,))
            
            if user_exists[0]['count'] == 0:
                # Create user with a random birth year between 2007-2012
                birth_year = random.randint(2007, 2012)
                create_user_query = """
                    INSERT INTO users (user_uuid, year_of_birth, created_at)
                    VALUES (%s, %s, %s)
                """
                execute_query(create_user_query, (user_uuid, birth_year, datetime.now()), fetch=False)
                print(f"  Created user: {user_uuid}")
            else:
                print(f"  User already exists: {user_uuid}")
        except Exception as e:
            print(f"  Error creating user {user_uuid}: {e}")
    
    print("Sample users created successfully!")
    
    total_votes_added = 0
    
    for question in questions:
        question_code = question['question_code']
        is_checkbox = question['check_box']
        
        print(f"Processing question {question_code} (checkbox: {is_checkbox})")
        
        # Get options for this question
        options_query = "SELECT option_select FROM options WHERE question_code = %s ORDER BY option_select"
        options = execute_query(options_query, (question_code,))
        
        if not options:
            print(f"  No options found for {question_code}, skipping")
            continue
        
        # Calculate votes per option to total 100 per question
        non_other_options = [opt for opt in options if opt['option_select'] != 'OTHER']
        total_options = len(non_other_options)
        
        if total_options > 0:
            # Distribute 100 votes across all non-OTHER options
            votes_per_option = 100 // total_options
            remaining_votes = 100 % total_options
            
            # Add sample votes for each option
            for i, option in enumerate(non_other_options):
                option_select = option['option_select']
                
                # Add base votes per option, plus distribute remaining votes
                num_votes = votes_per_option + (1 if i < remaining_votes else 0)
            
            if is_checkbox:
                # For checkbox questions, add weighted votes
                for i in range(num_votes):
                    user_uuid = random.choice(sample_users)
                    weight = 1.0 / random.randint(1, 3)  # Random weight between 0.33 and 1.0
                    
                    # Get question and category details for denormalization
                    question_info_query = """
                        SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
                        FROM questions q
                        JOIN categories c ON q.category_id = c.id
                        WHERE q.question_code = %s
                    """
                    question_info = execute_query(question_info_query, (question_code,))
                    
                    if question_info:
                        question_data = question_info[0]
                        
                        # Get option details
                        option_info_query = """
                            SELECT option_text, option_code
                            FROM options
                            WHERE question_code = %s AND option_select = %s
                        """
                        option_info = execute_query(option_info_query, (question_code, option_select))
                        
                        if option_info:
                            option_data = option_info[0]
                            
                            # Insert sample checkbox vote
                            insert_query = """
                                INSERT INTO checkbox_responses (
                                    question_code, option_select, option_code, option_text, user_uuid,
                                    question_text, question_number, category_name, category_id, block_number, weight, created_at
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            execute_query(insert_query, (
                                question_code, option_select, option_data['option_code'], option_data['option_text'],
                                user_uuid, question_data['question_text'], question_data['question_number'],
                                question_data['category_name'], question_data['category_id'], question_data['block_number'], 
                                weight, datetime.now()
                            ), fetch=False)
                            
                            total_votes_added += 1
            else:
                # For single-choice questions, add regular votes
                for i in range(num_votes):
                    user_uuid = random.choice(sample_users)
                    
                    # Get question and category details for denormalization
                    question_info_query = """
                        SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
                        FROM questions q
                        JOIN categories c ON q.category_id = c.id
                        WHERE q.question_code = %s
                    """
                    question_info = execute_query(question_info_query, (question_code,))
                    
                    if question_info:
                        question_data = question_info[0]
                        
                        # Get option details
                        option_info_query = """
                            SELECT option_text, option_code
                            FROM options
                            WHERE question_code = %s AND option_select = %s
                        """
                        option_info = execute_query(option_info_query, (question_code, option_select))
                        
                        if option_info:
                            option_data = option_info[0]
                            
                            # Insert sample vote
                            insert_query = """
                                INSERT INTO responses (
                                    question_code, option_select, option_code, option_text, user_uuid,
                                    question_text, question_number, category_name, category_id, block_number, created_at
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            execute_query(insert_query, (
                                question_code, option_select, option_data['option_code'], option_data['option_text'],
                                user_uuid, question_data['question_text'], question_data['question_number'],
                                question_data['category_name'], question_data['category_id'], question_data['block_number'], 
                                datetime.now()
                            ), fetch=False)
                            
                            total_votes_added += 1
        
        # Add sample OTHER responses (part of the 100 total)
        other_options = [opt for opt in options if opt['option_select'] == 'OTHER']
        if other_options:
            # Calculate how many votes we've already added
            votes_added_so_far = sum(votes_per_option + (1 if i < remaining_votes else 0) for i in range(total_options))
            other_votes_needed = 100 - votes_added_so_far
            
            # Add the remaining votes as OTHER responses
            for i in range(other_votes_needed):
                user_uuid = random.choice(sample_users)
                
                # Get question and category details for denormalization
                question_info_query = """
                    SELECT q.question_text, q.question_number, c.category_name, c.id as category_id, q.block_number
                    FROM questions q
                    JOIN categories c ON q.category_id = c.id
                    WHERE q.question_code = %s
                """
                question_info = execute_query(question_info_query, (question_code,))
                
                if question_info:
                    question_data = question_info[0]
                    
                    # Insert sample OTHER response
                    insert_query = """
                        INSERT INTO other_responses (
                            question_code, user_uuid, other_text, question_text, question_number,
                            category_name, category_id, block_number, created_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    execute_query(insert_query, (
                        question_code, user_uuid, f"Sample response {i+1}",
                        question_data['question_text'], question_data['question_number'], 
                        question_data['category_name'], question_data['category_id'], 
                        question_data['block_number'], datetime.now()
                    ), fetch=False)
                    
                    total_votes_added += 1
    
    print(f"\n✅ Successfully added {total_votes_added} sample votes!")
    print("All questions now have exactly 100 initial votes to display.")
    print("\n📊 Vote distribution summary:")
    print("- Each question gets exactly 100 total votes")
    print("- Votes are distributed evenly across all options")
    print("- Remaining votes go to OTHER option if available")
    print("- Easy to remove: just delete the first 100 votes per question when you get real data")

if __name__ == "__main__":
    try:
        add_sample_votes()
        print("\n🎉 Sample votes added successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
