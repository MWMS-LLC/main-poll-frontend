#!/usr/bin/env python3
"""
Simple script to add sample data for bar chart experiments.
Adds sample responses directly to results tables without user creation.
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

def add_sample_data():
    """Add sample data directly to results tables"""
    
    # Get all questions
    questions_query = "SELECT question_code, check_box FROM questions ORDER BY question_code"
    questions = execute_query(questions_query)
    
    print(f"Found {len(questions)} questions to process")
    
    # Use an existing user from the database
    existing_users_query = "SELECT user_uuid FROM users LIMIT 1"
    existing_users = execute_query(existing_users_query)
    
    if not existing_users:
        print("❌ No users found in database. Please create a user first.")
        return
    
    sample_user_uuid = existing_users[0]['user_uuid']
    print(f"Using existing user: {sample_user_uuid}")
    
    total_responses_added = 0
    
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
            
            # Add sample responses for each option
            for i, option in enumerate(non_other_options):
                option_select = option['option_select']
                
                # Add base votes per option, plus distribute remaining votes
                num_votes = votes_per_option + (1 if i < remaining_votes else 0)
                
                if is_checkbox:
                    # For checkbox questions, add weighted responses
                    for _ in range(num_votes):
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
                                weight = 1.0 / random.randint(1, 3)  # Random weight between 0.33 and 1.0
                                
                                # Insert sample checkbox response
                                insert_query = """
                                    INSERT INTO checkbox_responses (
                                        question_code, option_select, option_code, option_text, user_uuid,
                                        question_text, question_number, category_name, category_id, block_number, weight, created_at
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                                execute_query(insert_query, (
                                    question_code, option_select, option_data['option_code'], option_data['option_text'],
                                    sample_user_uuid, question_data['question_text'], question_data['question_number'],
                                    question_data['category_name'], question_data['category_id'], question_data['block_number'], 
                                    weight, datetime.now()
                                ), fetch=False)
                                
                                total_responses_added += 1
                else:
                    # For single-choice questions, add regular responses
                    for _ in range(num_votes):
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
                                
                                # Insert sample response
                                insert_query = """
                                    INSERT INTO responses (
                                        question_code, option_select, option_code, option_text, user_uuid,
                                        question_text, question_number, category_name, category_id, block_number, created_at
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                                execute_query(insert_query, (
                                    question_code, option_select, option_data['option_code'], option_data['option_text'],
                                    sample_user_uuid, question_data['question_text'], question_data['question_number'],
                                    question_data['category_name'], question_data['category_id'], question_data['block_number'], 
                                    datetime.now()
                                ), fetch=False)
                                
                                total_responses_added += 1
        
        # Add sample OTHER responses (part of the 100 total)
        other_options = [opt for opt in options if opt['option_select'] == 'OTHER']
        if other_options:
            # Calculate how many responses we've already added
            responses_added_so_far = sum(votes_per_option + (1 if i < remaining_votes else 0) for i in range(total_options))
            other_responses_needed = 100 - responses_added_so_far
            
            # Add the remaining responses as OTHER responses
            for i in range(other_responses_needed):
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
                        question_code, sample_user_uuid, f"Sample response {i+1}",
                        question_data['question_text'], question_data['question_number'], 
                        question_data['category_name'], question_data['category_id'], 
                        question_data['block_number'], datetime.now()
                    ), fetch=False)
                    
                    total_responses_added += 1
    
    print(f"\n✅ Successfully added {total_responses_added} sample responses!")
    print("All questions now have exactly 100 initial responses to display.")
    print("\n📊 Response distribution summary:")
    print("- Each question gets exactly 100 total responses")
    print("- Responses are distributed evenly across all options")
    print("- Remaining responses go to OTHER option if available")
    print(f"- Easy to remove: just delete responses with user_uuid = '{sample_user_uuid}' when you get real data")

if __name__ == "__main__":
    try:
        add_sample_data()
        print("\n🎉 Sample data added successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
