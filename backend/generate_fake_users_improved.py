import os
import random
import uuid
from datetime import datetime, timedelta
import pg8000

def get_db_connection():
    """Get database connection for local development"""
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'teen_poll',
        'user': 'postgres',
        'password': ''
    }
    
    conn = pg8000.connect(**db_params)
    return conn

def generate_fake_users(num_users=20):
    """Generate fake user data"""
    users = []
    for i in range(num_users):
        # Generate random birth year between 2007-2012
        birth_year = random.randint(2007, 2012)
        
        # Generate random creation date within last 30 days
        days_ago = random.randint(0, 30)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        user = {
            'user_uuid': str(uuid.uuid4()),
            'year_of_birth': birth_year,
            'created_at': created_at
        }
        users.append(user)
    
    return users

def get_questions_with_options(conn):
    """Get all questions with their options and metadata"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            q.question_code,
            q.question_text,
            q.check_box,
            q.max_select,
            q.category_id,
            c.category_name,
            q.block_number,
            q.block_text,
            q.color_code,
            q.version
        FROM questions q
        JOIN categories c ON q.category_id = c.id
        ORDER BY q.category_id, q.block_number, q.question_number
    """)
    
    questions = []
    for row in cursor.fetchall():
        question = {
            'question_code': row[0],
            'question_text': row[1],
            'check_box': row[2],
            'max_select': row[3],
            'category_id': row[4],
            'category_name': row[5],
            'block_number': row[6],
            'block_text': row[7],
            'color_code': row[8],
            'version': row[9]
        }
        
        # Get options for this question
        cursor.execute("""
            SELECT 
                option_select,
                option_code,
                option_text,
                response_message,
                companion_advice,
                tone_tag
            FROM options 
            WHERE question_code = %s 
            ORDER BY option_select
        """, (question['question_code'],))
        
        question['options'] = []
        for opt_row in cursor.fetchall():
            option = {
                'option_select': opt_row[0],
                'option_code': opt_row[1],
                'option_text': opt_row[2],
                'response_message': opt_row[3],
                'companion_advice': opt_row[4],
                'tone_tag': opt_row[5]
            }
            question['options'].append(option)
        
        questions.append(question)
    
    cursor.close()
    return questions

def generate_realistic_responses(conn, user_uuid, questions):
    """Generate realistic responses for a user based on question types"""
    responses = []
    checkbox_responses = []
    other_responses = []
    
    for question in questions:
        if not question['options']:
            continue
            
        # Generate random timestamp within last 7 days
        days_ago = random.randint(0, 7)
        response_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        if question['check_box'] and question['max_select'] > 1:
            # Checkbox question - select multiple options
            num_to_select = random.randint(1, min(question['max_select'], len(question['options'])))
            selected_options = random.sample(question['options'], num_to_select)
            
            for option in selected_options:
                checkbox_responses.append({
                    'user_uuid': user_uuid,
                    'question_code': question['question_code'],
                    'question_text': question['question_text'],
                    'question_number': None,  # Will be filled from question data
                    'category_id': question['category_id'],
                    'category_name': question['category_name'],
                    'option_id': None,  # Will be filled from option data
                    'option_select': option['option_select'],
                    'option_code': option['option_code'],
                    'option_text': option['option_text'],
                    'block_number': question['block_number'],
                    'weight': 1.0 / len(selected_options),
                    'created_at': response_time
                })
                
        else:
            # Single choice question
            option = random.choice(question['options'])
            responses.append({
                'user_uuid': user_uuid,
                'question_code': question['question_code'],
                'question_text': question['question_text'],
                'question_number': None,  # Will be filled from question data
                'category_id': question['category_id'],
                'category_name': question['category_name'],
                'option_id': None,  # Will be filled from option data
                'option_select': option['option_select'],
                'option_code': option['option_code'],
                'option_text': option['option_text'],
                'block_number': question['block_number'],
                'created_at': response_time
            })
    
    return responses, checkbox_responses, other_responses

def insert_users(conn, users):
    """Insert users into the database"""
    cursor = conn.cursor()
    
    for user in users:
        cursor.execute("""
            INSERT INTO users (user_uuid, year_of_birth, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_uuid) DO NOTHING
        """, (user['user_uuid'], user['year_of_birth'], user['created_at']))
    
    conn.commit()
    cursor.close()
    print(f"✅ Inserted {len(users)} users")

def insert_responses(conn, responses, checkbox_responses, other_responses):
    """Insert all responses into the database"""
    cursor = conn.cursor()
    
    # Insert single choice responses
    if responses:
        for response in responses:
            cursor.execute("""
                INSERT INTO responses (
                    user_uuid, question_code, question_text, question_number,
                    category_id, category_name, option_id, option_select,
                    option_code, option_text, block_number, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                response['user_uuid'], response['question_code'], response['question_text'],
                response['question_number'], response['category_id'], response['category_name'],
                response['option_id'], response['option_select'], response['option_code'],
                response['option_text'], response['block_number'], response['created_at']
            ))
    
    # Insert checkbox responses
    if checkbox_responses:
        for response in checkbox_responses:
            cursor.execute("""
                INSERT INTO checkbox_responses (
                    user_uuid, question_code, question_text, question_number,
                    category_id, category_name, option_id, option_select,
                    option_code, option_text, block_number, weight, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                response['user_uuid'], response['question_code'], response['question_text'],
                response['question_number'], response['category_id'], response['category_name'],
                response['option_id'], response['option_select'], response['option_code'],
                response['option_text'], response['block_number'], response['weight'], response['created_at']
            ))
    
    conn.commit()
    cursor.close()
    
    print(f"✅ Single responses: {len(responses)}")
    print(f"✅ Checkbox responses: {len(checkbox_responses)}")
    print(f"✅ Other responses: {len(other_responses)}")

def main():
    """Main function to generate and insert fake data"""
    try:
        print("🚀 Starting fake data generation...")
        print("Connecting to database...")
        conn = get_db_connection()
        
        print("Generating 20 fake users...")
        users = generate_fake_users(20)
        
        print("Getting all questions with options...")
        questions = get_questions_with_options(conn)
        print(f"📝 Found {len(questions)} questions")
        
        print("Inserting users...")
        insert_users(conn, users)
        
        print("Generating and inserting responses...")
        all_responses = []
        all_checkbox_responses = []
        all_other_responses = []
        
        for i, user in enumerate(users, 1):
            print(f"👤 Generating responses for user {i}/20 ({user['user_uuid'][:8]}...)")
            responses, checkbox_responses, other_responses = generate_realistic_responses(conn, user['user_uuid'], questions)
            
            all_responses.extend(responses)
            all_checkbox_responses.extend(checkbox_responses)
            all_other_responses.extend(other_responses)
        
        print("Inserting all responses...")
        insert_responses(conn, all_responses, all_checkbox_responses, all_other_responses)
        
        print("\n🎉 Successfully generated fake data!")
        print(f"📊 Users: {len(users)}")
        print(f"📝 Single responses: {len(all_responses)}")
        print(f"☑️ Checkbox responses: {len(all_checkbox_responses)}")
        print(f"💬 Other responses: {len(all_other_responses)}")
        print(f"🎯 Total responses: {len(all_responses) + len(all_checkbox_responses) + len(all_other_responses)}")
        print(f"📈 Average responses per user: {(len(all_responses) + len(all_checkbox_responses) + len(all_other_responses)) / len(users):.1f}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
