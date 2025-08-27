import os
import random
import uuid
from datetime import datetime, timedelta
import pg8000
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Get database connection using DATABASE_URL from environment"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Parse the DATABASE_URL
    parsed = urlparse(database_url)
    
    # Extract connection parameters for pg8000
    db_params = {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path[1:],  # Remove leading slash
        'user': parsed.username,
        'password': parsed.password,
        'ssl_context': True  # pg8000 uses ssl_context instead of sslmode
    }
    
    # Connect to the database using pg8000
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

def get_all_questions(conn):
    """Get all questions from the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT question_code FROM questions ORDER BY question_code")
    questions = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return questions

def get_question_options(conn, question_code):
    """Get options for a specific question"""
    cursor = conn.cursor()
    cursor.execute("SELECT option_select FROM options WHERE question_code = %s ORDER BY option_select", (question_code,))
    options = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return options

def generate_random_responses(conn, user_uuid, questions):
    """Generate random responses for a user"""
    responses = []
    checkbox_responses = []
    other_responses = []
    
    for question_code in questions:
        # Get options for this question
        options = get_question_options(conn, question_code)
        
        if not options:
            continue
            
        # Randomly decide response type
        response_type = random.choice(['single', 'checkbox', 'other'])
        
        if response_type == 'single':
            # Single choice response
            option = random.choice(options)
            responses.append({
                'user_uuid': user_uuid,
                'question_code': question_code,
                'option_select': option,
                'created_at': datetime.now()
            })
            
        elif response_type == 'checkbox':
            # Checkbox response (multi-select)
            num_selected = random.randint(1, min(3, len(options)))
            selected_options = random.sample(options, num_selected)
            
            for option in selected_options:
                # Calculate weight: 1 / number of selected options
                weight = 1.0 / len(selected_options)
                checkbox_responses.append({
                    'user_uuid': user_uuid,
                    'question_code': question_code,
                    'option_select': option,
                    'weight': weight,
                    'created_at': datetime.now()
                })
                
        else:  # other
            # Other response (free text)
            fake_texts = [
                "I'm not sure about this one",
                "This is interesting",
                "I have mixed feelings",
                "It depends on the situation",
                "I need to think about this more",
                "This resonates with me",
                "I'm still figuring this out",
                "This is complicated",
                "I have a different perspective",
                "I'm learning about this"
            ]
            other_text = random.choice(fake_texts)
            other_responses.append({
                'user_uuid': user_uuid,
                'question_code': question_code,
                'other_text': other_text,
                'created_at': datetime.now()
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
    print(f"Inserted {len(users)} users")

def insert_responses(conn, responses, checkbox_responses, other_responses):
    """Insert all responses into the database"""
    cursor = conn.cursor()
    
    # Insert single choice responses
    if responses:
        for response in responses:
            cursor.execute("""
                INSERT INTO responses (user_uuid, question_code, option_select, created_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_uuid, question_code) DO NOTHING
            """, (response['user_uuid'], response['question_code'], 
                  response['option_select'], response['created_at']))
    
    # Insert checkbox responses
    if checkbox_responses:
        for response in checkbox_responses:
            cursor.execute("""
                INSERT INTO checkbox_responses (user_uuid, question_code, option_select, weight, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_uuid, question_code, option_select) DO NOTHING
            """, (response['user_uuid'], response['question_code'], 
                  response['option_select'], response['weight'], response['created_at']))
    
    # Insert other responses
    if other_responses:
        for response in other_responses:
            cursor.execute("""
                INSERT INTO other_responses (user_uuid, question_code, other_text, created_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_uuid, question_code) DO NOTHING
            """, (response['user_uuid'], response['question_code'], 
                  response['other_text'], response['created_at']))
    
    conn.commit()
    cursor.close()
    
    print(f"Inserted {len(responses)} single responses")
    print(f"Inserted {len(checkbox_responses)} checkbox responses")
    print(f"Inserted {len(other_responses)} other responses")

def main():
    """Main function to generate and insert fake data"""
    try:
        print("Connecting to database...")
        conn = get_db_connection()
        
        print("Generating 20 fake users...")
        users = generate_fake_users(20)
        
        print("Getting all questions...")
        questions = get_all_questions(conn)
        print(f"Found {len(questions)} questions")
        
        print("Inserting users...")
        insert_users(conn, users)
        
        print("Generating and inserting responses...")
        all_responses = []
        all_checkbox_responses = []
        all_other_responses = []
        
        for user in users:
            print(f"Generating responses for user {user['user_uuid'][:8]}...")
            responses, checkbox_responses, other_responses = generate_random_responses(conn, user['user_uuid'], questions)
            
            all_responses.extend(responses)
            all_checkbox_responses.extend(checkbox_responses)
            all_other_responses.extend(other_responses)
        
        print("Inserting all responses...")
        insert_responses(conn, all_responses, all_checkbox_responses, all_other_responses)
        
        print("\n✅ Successfully generated fake data!")
        print(f"📊 Users: {len(users)}")
        print(f"📝 Single responses: {len(all_responses)}")
        print(f"☑️ Checkbox responses: {len(all_checkbox_responses)}")
        print(f"💬 Other responses: {len(all_other_responses)}")
        print(f"🎯 Total responses: {len(all_responses) + len(all_checkbox_responses) + len(all_other_responses)}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
